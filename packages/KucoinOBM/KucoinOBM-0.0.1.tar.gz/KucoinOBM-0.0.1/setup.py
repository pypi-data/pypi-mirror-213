from distutils.core import setup

setup(
    name="KucoinOBM",
    version="0.0.1",
    description="A reliable and fast kucoin orderbook maintainer and manager.",
    author="Parth Mittal",
    author_email="parth@privatepanda.co",
    url="https://www.github.com/PrivatePandaCO/KucoinOBM",
    license="GNU GENERAL PUBLIC LICENSE Version 2",
    packages=["KucoinOBM"],
    install_requires=["orjson", "requests", "pyloggor", "KucoinWrapper"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://github.com/PrivatePandaCO/KucoinOBM/blob/master/README.md",
        "Github": "https://github.com/PrivatePandaCO/KucoinOBM",
    },
)
