from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multialias",
    version="1.0.2",
    description="A command line tool to bulk rename files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="itsknk",
    packages=["multialias"],
    install_requires=["requests", "colorama"],
)
