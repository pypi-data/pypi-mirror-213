from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="annorest",
    version="0.1.0",
    author="K. H. Chiang",
    author_email="neverleave0916@email.com",
    description="A simple Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neverleave0916/annorest",
    packages=["annorest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)