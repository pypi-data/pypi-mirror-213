from setuptools import setup, find_packages
import os

VERSION = '0.0.7'
DESCRIPTION = 'Some Kits'

setup(
    name="tj_kits_winds",
    version=VERSION,
    author="tjno-1",
    author_email="tjno-1@qq.com",
    description=DESCRIPTION,
    # long_description=open("README.md", encoding="UTF-8").read(),
    packages=find_packages(),
    requires=[],
    keywords=['python', 'build-in-module kits'],
    license="MIT",
    url="https://github.com/TJNo-1/tj_kits_wind.git",
    python_requires='>=3.8',
)
