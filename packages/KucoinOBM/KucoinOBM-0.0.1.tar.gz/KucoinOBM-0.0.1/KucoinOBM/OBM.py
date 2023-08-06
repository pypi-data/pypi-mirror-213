import socket
import threading
import time
import traceback

import orjson
import requests
from KucoinWrapper import KucoinWrapper
from pyloggor import pyloggor


class KucoinOBM:
    def __init__(
        self,
        kc_api_key: str,
        kc_api_secret: str,
        kc_api_passphrase: str,
        symbols: list[str],
        id: int,
        response_address: str = None,
        logger: pyloggor = pyloggor(project_root="KucoinOBM"),
    ) -> None:
        self.logger = logger
        self.symbols = symbols
        self._shutdown = False
        self.id = id

        self.response_address = response_address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        self.cache = []
        self.changes = set()
        self.update_subs = []
        self.message_count = {symbol: 0 for symbol in symbols}
        self.last_known_freq = {symbol: 0 for symbol in symbols}

        self.orderbooks = {symbol: {"asks": {}, "bids": {}, "seq": "0"} for symbol in symbols}
        self.curr_prices = {symbol: "0" for symbol in symbols}  # {"market": "price"}

        self.kc = KucoinWrapper(
            kc_api_key,
            kc_api_secret,
            kc_api_passphrase,
            defaults=[],
            second_message_handler=self.message_handler,
            after_ws=self.setup,
            logger=self.logger
        )

        self.logger.log("DEBUG", msg="Initiated KC, now subscribing", extras={"id": self.id})
        self.kc.subscribe(f"/market/level2:{','.join(self.symbols)}", False)
        self.kc.subscribe(f"/market/match:{','.join(self.symbols)}", False)
        self.kc.subscribe(f"/spotMarket/level2Depth50:{','.join(self.symbols)}", False)
        self.logger.log("DEBUG", msg="Subscribed to all channels, now running snapshots", extras={"id": self.id})
        threading.Thread(daemon=True, target=self.wipe_freq).start()
        self.setup()

    def setup(self):
        for symbol in self.symbols:  # fetch ob
            self.refetch_ob(symbol)

        self.logger.log("DEBUG", msg="Got all snapshots, now caching", extras={"id": self.id})
        threading.Thread(daemon=True, target=self.cache_to_ob).start()  # start caching ob

        self.logger.log("DEBUG", msg="Caching current prices", extras={"id": self.id})

        for symbol in self.symbols:
            self.cache_price(symbol)  # cache price

        for symbol in self.symbols:
            self.changes.add(symbol)  # add changes

        if self.response_address:
            threading.Thread(daemon=True, target=self.updates).start()  # start updating socket
        self.logger.log("INFO", msg="Booted up OB maintainer.", extras={"id": self.id})

    def cache_price(self, symbol):
        while True:
            try:
                r = requests.get(f"https://api.kucoin.com/api/v1/market/histories?symbol={symbol}")
                resp_json = r.json()

                self.curr_prices[symbol] = resp_json["data"][-1]["price"]
                return
            except Exception as e:
                resp_json = resp_json or r.text or r.content or "no resp"
                self.logger.log(
                    "WARNING",
                    msg="Unhandled error while getting current price",
                    extras={
                        "symbol": symbol,
                        "id": self.id,
                        "resp": resp_json,
                        "error": e,
                        "traceback": traceback.format_exc(),
                    },
                )

    def refetch_ob(self, symbol):
        while True:
            try:
                s_data = self.kc.get_ob(symbol)
                # bids decreasing, asks increasing, all strings
                break
            except Exception as e:
                self.logger.log(
                    "WARNING",
                    msg="Failed to get snapshot, retrying",
                    extras={
                        "symbol": symbol,
                        "id": self.id,
                        "error": e,
                        "traceback": traceback.format_exc(),
                    },
                )
                continue

        self.apply_snapshot(s_data["asks"], s_data["bids"], s_data["sequence"], symbol)
        self.changes.add(symbol)

    def apply_snapshot(self, asks, bids, seq, symbol):
        if symbol not in self.orderbooks:
            self.orderbooks[symbol] = {"asks": {}, "bids": {}, "seq": "0"}
        self.orderbooks[symbol]["seq"] = seq

        old_asks = list(self.orderbooks[symbol]["asks"].items())
        old_bids = list(self.orderbooks[symbol]["bids"].items())

        old_asks = old_asks + [(0, 0)] * (len(asks) - len(old_asks))
        old_bids = old_bids + [(0, 0)] * (len(bids) - len(old_bids))

        for ind, ask in enumerate(asks):
            old_asks[ind] = (float(ask[0]), float(ask[1]))
        for ind, bid in enumerate(bids):
            old_bids[ind] = (float(bid[0]), float(bid[1]))

        self.orderbooks[symbol]["asks"] = dict(old_asks)
        self.orderbooks[symbol]["bids"] = dict(old_bids)
        self.changes.add(symbol)

    def insert_new(self, price: float, size: float, side: str, symbol: str):
        if side == "asks":  # lowest first
            ind_to_insert_at = 0
            for i, k in enumerate(self.orderbooks[symbol]["asks"]):
                if price < k:
                    ind_to_insert_at = i
                    break

            self.orderbooks[symbol]["asks"] = (
                dict(list(self.orderbooks[symbol]["asks"].items())[:ind_to_insert_at])
                | {price: size}
                | dict(list(self.orderbooks[symbol]["asks"].items())[ind_to_insert_at:])
            )

            if ind_to_insert_at == 0:
                self.changes.add(symbol)

        elif side == "bids":  # highest first
            ind_to_insert_at = 0
            for i, k in enumerate(self.orderbooks[symbol]["bids"]):
                if price > k:
                    ind_to_insert_at = i
                    break

            self.orderbooks[symbol]["bids"] = (
                dict(list(self.orderbooks[symbol]["bids"].items())[:ind_to_insert_at])
                | {price: size}
                | dict(list(self.orderbooks[symbol]["bids"].items())[ind_to_insert_at:])
            )

            if ind_to_insert_at == 0:
                self.changes.add(symbol)

    def cache_to_ob(self):
        while not self._shutdown:
            try:
                entry = self.cache.pop(0)
            except:
                continue

            symbol = entry["symbol"]
            entry = entry["changes"]

            for asks_change in entry["asks"]:
                if asks_change[2] <= self.orderbooks[symbol]["seq"]:  # seq compare; 3 seconds for 100 million iterations
                    continue
                price = float(asks_change[0])
                if asks_change[1] == "0":  # if size is 0
                    if price in self.orderbooks[symbol]["asks"]:
                        del self.orderbooks[symbol]["asks"][price]
                    continue

                size = float(asks_change[1])
                if price in self.orderbooks[symbol]["asks"]:
                    self.orderbooks[symbol]["asks"][price] = size
                else:
                    self.insert_new(price, size, "asks", symbol)

            for bids_change in entry["bids"]:
                if bids_change[2] <= self.orderbooks[symbol]["seq"]:  # seq compare; 3 seconds for 100 million iterations
                    continue
                price = float(bids_change[0])
                if bids_change[1] == "0":
                    if price in self.orderbooks[symbol]["bids"]:
                        del self.orderbooks[symbol]["bids"][price]
                    continue

                size = float(bids_change[1])
                if price in self.orderbooks[symbol]["bids"]:
                    self.orderbooks[symbol]["bids"][price] = size
                else:
                    self.insert_new(price, size, "bids", symbol)

    def message_handler(self, message_json: dict):
        if "subject" not in message_json:
            return
        if message_json["subject"] == "trade.l2update":
            self.message_count[message_json["data"]["symbol"]] += 1
            self.cache.append(message_json["data"])
        elif message_json["subject"] == "trade.l3match":
            symbol = message_json["data"]["symbol"]
            price = message_json["data"]["price"]
            if price != self.curr_prices[symbol]:
                self.curr_prices[symbol] = price
                self.changes.add(symbol)
            self.message_count[symbol] += 1
        elif message_json["subject"] == "level2":
            symbol = message_json["topic"].split(":")[1]
            self.message_count[symbol]
            self.apply_snapshot(
                message_json["data"]["asks"],
                message_json["data"]["bids"],
                "0",
                message_json["topic"].split(":")[1],
            )

    def wipe_freq(self):
        while not self._shutdown:
            time.sleep(60)
            for symbol, freq in self.message_count.items():
                self.sock.sendto(orjson.dumps({"symbol": symbol, "id": self.id, "freq": freq}), self.address)
                self.message_count[symbol] = 0
                self.last_known_freq[symbol] = freq

    def shutdown(self):
        self._shutdown = True
        self.kc.shutdown()
        self.logger.log("INFO", msg="Shutdown", extras={"id": self.id})

    def pause(self):
        self._pause = True
        self.logger.log("INFO", msg="Paused", extras={"id": self.id})

    def sub_to_market(self, symbols):
        s = ",".join(symbols)
        self.kc.subscribe(f"/market/level2:{s}", False)
        self.kc.subscribe(f"/market/match:{s}", False)
        self.kc.subscribe(f"/spotMarket/level2Depth50:{s}", False)
        for symbol in symbols:
            if symbol not in self.message_count:
                self.message_count[symbol] = 0
            self.refetch_ob(symbol)
            self.cache_price(symbol)

    def unsub_from_market(self, symbols):
        s = ",".join(symbols)
        self.kc.unsubscribe(f"/market/level2:{s}", False)
        self.kc.unsubscribe(f"/market/match:{s}", False)
        self.kc.unsubscribe(f"/spotMarket/level2Depth50:{s}", False)
        for symbol in symbols:
            if symbol in self.message_count:
                del self.message_count[symbol]
            if symbol in self.orderbooks:
                del self.orderbooks[symbol]
            if symbol in self.curr_prices:
                del self.curr_prices[symbol]

    def get_dets(self, symbol, depth=10):
        asks = list(self.orderbooks[symbol]["asks"].items())[:depth]
        asks.reverse()  # this is so that when printing, they appear in the right order
        # the asks are sorted from lowest to highest, so we reverse it to get highest to lowest
        # so the first print is the highest then we proceed to lowest
        # as we get closer to best ask and current price
        # this is not required for sorting the asks dict by default, its only used here for printing
        bids = list(self.orderbooks[symbol]["bids"].items())[:depth]
        curr_price = self.curr_prices[symbol]

        delim = "\n--------------------------\n"
        asks_ = "\n".join([f"{a}          {b}" for a, b in asks])
        curr = f"\n{curr_price}\n"
        bids_ = "\n".join([f"{a}          {b}" for a, b in bids])
        return f"{asks_}{delim}{curr}{delim}{bids_}"

    def get_all_for(self, symbol) -> dict[str, str]:
        return {
            "symbol": symbol,
            "id": self.id,
            "curr_price": self.curr_prices[symbol],
            "best_ask": list(self.orderbooks[symbol]["asks"].items())[0],
            "best_bid": list(self.orderbooks[symbol]["bids"].items())[0],
            "message_freq": self.last_known_freq[symbol],
        }

    def add_update_subs(self, symbols):
        self.update_subs += symbols

    def remove_update_subs(self, symbols):
        self.update_subs = [s for s in self.update_subs if s not in symbols]

    def get_update_subs(self):
        return self.update_subs

    def updates(self):
        self.logger.log("INFO", msg="Started updates", extras={"id": self.id})
        while True:
            if len(self.changes) == 0:
                continue
            if self._shutdown:
                return

            if self.kc._shutdown_ws:
                self.logger.log(
                    "ERROR", topic="updated", msg="WS is shutting down, waiting for it to be over", extras={"id": self.id}
                )
                return

            symb = self.changes.pop()
            if symb not in self.update_subs:
                continue

            self.sock.sendto(symb.encode(), self.response_address)
