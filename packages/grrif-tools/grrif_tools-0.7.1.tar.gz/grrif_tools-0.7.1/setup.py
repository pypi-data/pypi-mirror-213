import os
from setuptools import setup, find_packages

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name="grrif_tools",
    description="An unofficial set of tools for Cool Cats™.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Julien 'fetzu' Bono",
    url="https://github.com/fetzu/grrif-tools",
    version="0.7.1",
    download_url="https://github.com/fetzu/grrif-tools/releases/latest",
    packages=find_packages(include=["grrif_tools", "grrif_tools.*"]),
    license="License :: OSI Approved :: MIT License",
    install_requires=[
        "Requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "titlecase==2.4",
        "miniaudio==1.57",
    ],
    entry_points={"console_scripts": ["grrif_tools=grrif_tools.cli:main"]},
)
