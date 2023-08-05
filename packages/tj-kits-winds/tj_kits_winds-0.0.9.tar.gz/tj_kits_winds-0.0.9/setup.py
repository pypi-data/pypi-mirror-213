import setuptools
from setuptools import setup, find_packages
import os

VERSION = '0.0.9'
DESCRIPTION = 'Some Kits'

# with open("README.md", "r+") as f:
#     long_description = f.read()

setup(
    name="tj_kits_winds",
    version=VERSION,
    author="tjno-1",
    author_email="tjno-1@qq.com",
    description=DESCRIPTION,
    long_description="long_description",
    packages=find_packages(),
    install_requires=[
        'pydantic >= 1.10.7',
    ],
    keywords=['python', 'build-in-module kits'],
    license="MIT",
    url="https://github.com/TJNo-1/tj_kits_wind.git",
    python_requires='>=3.8',
)
