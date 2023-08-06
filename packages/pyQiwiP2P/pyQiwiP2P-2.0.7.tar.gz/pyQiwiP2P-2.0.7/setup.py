from io import open
from os import environ

from setuptools import setup


def read(filename):
    with open(filename, encoding="utf-8") as file:
        return file.read()


def requirements():
    with open("requirements.txt", "r") as req:
        return [r for r in req.read().split("\n") if r]


setup(
    name="pyQiwiP2P",
    version=environ.get("TAG_VERSION").replace("v", ""),
    packages=["pyqiwip2p", "pyqiwip2p.p2p_types", "pyqiwip2p.notify"],
    url="https://github.com/WhiteApfel/pyQiwiP2P",
    license="Mozilla Public License 2.0",
    author="WhiteApfel",
    author_email="white@pfel.ru",
    description="pyQiwiP2P",
    install_requires=requirements(),
    project_urls={
        "Документальное чтиво": "https://pyqiwip2p.readthedocs.io/ru/latest/",
        "Донатик": "https://pfel.cc/donate",
        "Исходнички": "https://github.com/WhiteApfel/pyQiwiP2P",
        "Тележка для вопросов": "https://t.me/apfel",
    },
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="qiwip2p api qiwi p2p payments bill tools sdk wrapper",
)
