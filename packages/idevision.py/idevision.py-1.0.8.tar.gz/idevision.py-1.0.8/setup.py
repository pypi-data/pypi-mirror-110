from setuptools import setup

REQUIREMENTS = []
with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

README = ""
with open("README.md", "r") as f:
    README = f.read()

setup(
    name="idevision.py",
    version="v1.0.8",
    description="A python wrapper for the IDevision api",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/isaa-ctaylor/idevision.py",
    author="isaa_ctaylor",
    author_email="isaacjontaylor@gmail.com",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["idevision"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
)