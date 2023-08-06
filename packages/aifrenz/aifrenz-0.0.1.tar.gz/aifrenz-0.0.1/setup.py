# Copyright 2023. Young-Mook Kang <hi@ymkang.pro>
# License: MIT, hi@ymkang.pro

from setuptools import find_packages, setup

def openReadMeFile():
    with open("README.md", encoding="utf8") as f:
        README = f.read()
    return README

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("requirements-test.txt") as f:
    required_test = f.read().splitlines()

setup(
    name="aifrenz",
    version="0.0.1",
    description="AiFrenz - An open source machine learning library.",
    long_description=openReadMeFile(),
    long_description_content_type="text/markdown",
    url="https://github.com/aifrenz/aifrenz",
    author="Young-Mook Kang",
    author_email="hi@ymkang.pro",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(include=["aifrenz*"]),
    include_package_data=True,
    install_requires=required,
    tests_require=required_test,
    python_requires=">=3.7",
)