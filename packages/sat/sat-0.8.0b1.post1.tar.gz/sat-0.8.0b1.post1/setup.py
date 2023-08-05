from setuptools import setup

OLD_PKG = "sat"
NEW_PKG = "libervia-backend"
NEW_NAME = "Libervia Backend"
VERSION = "0.8.0b1.post1"

setup(name = OLD_PKG,
      version=VERSION,
      description=f"Legacy package for {NEW_NAME}",
      author="Association « Salut à Toi »",
      author_email="contact@goffi.org",
      url="https://salut-a-toi.org",
      long_description=
        "this package is deprecated, please use "
        f" `{NEW_PKG} <https://pypi.org/project/{NEW_PKG}/>`_ instead.",
      install_requires=[f"{NEW_PKG} == {VERSION}"],
)
