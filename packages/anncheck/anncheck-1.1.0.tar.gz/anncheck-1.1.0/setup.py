#!/usr/bin/env python

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as f:
    requires = f.read()

setup(
    name="anncheck",
    version="1.1.0",
    description="A tool to find missing annotations in Python files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Folke Ishii",
    author_email="folke.ishii@gmail.com",
    url="https://github.com/Secozzi/anncheck",
    install_requires=requires,
    license="MIT license",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["anncheck"],
    entry_points = {
        "console_scripts": [
            "anncheck=anncheck.__init__:main"
        ]
    }
)
