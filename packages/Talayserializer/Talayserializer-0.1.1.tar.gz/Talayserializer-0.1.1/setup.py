# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="Talayserializer",
    version="0.1.1",
    description="JSON&XML serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Talay Artem",
    author_email="arteeemka.31@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["Talayserializer"],
    include_package_data=True,
    install_requires=["regex"]
)