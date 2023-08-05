import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pymeringue",
    version="1.0.0",
    description="A port of Meringue (https://github.com/stiive/meringue) for Python.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stiive/py-meringue",
    author="Beckett Normington",
    author_email="beckett@chatter-social.com",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["meringue"]
)