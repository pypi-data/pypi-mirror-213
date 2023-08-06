from setuptools import setup

from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname('setup.py'))

# Get the long description on pypi from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="american_options",
    version="0.1.1",
    description="library T-28h",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://american_options.readthedocs.io/",
    author="Przemysław Adamski, Katarzyna Hasal, Kacper Toczek",
    author_email="kat.hasal99@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["american_options"],
    include_package_data=True,
    install_requires=["numpy",
                      "scipy",
                      "chaospy",
                      "pandas",
                      "matplotlib",
                      "sklearn",
                      "tqdm"]
)