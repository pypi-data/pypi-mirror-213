import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "texta-lexicon-matcher",
    version = read("VERSION"),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("texta-lexicon-matcher"),
    license = "GPLv3",
    packages = [
        "texta_lexicon_matcher"
    ],
    data_files = ["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description = read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-lexicon-matcher-python",
    install_requires = read("requirements.txt").split("\n"),
    include_package_data = True
)
