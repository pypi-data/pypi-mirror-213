from setuptools import setup, find_packages
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hosgdSims",
    version="0.7.0",
    description="Hands on SGD",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/prodrig/hosgdsims",
    author="Paul Rodriguez",
    author_email="prodrig@pucp.edu.pe",
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages("hosgdSims", exclude=("docs",)),
    include_package_data=False,
    install_requires=["numpy>=1.19.1", "scipy>=1.5.2", "matplotlib>=3.3.1"],
)
