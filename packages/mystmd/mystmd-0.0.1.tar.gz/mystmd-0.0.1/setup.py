import sys
import os
import setuptools

sys.path[0:0] = ["mystmd"]
from version import __version__

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="mystmd",
    description="MyST Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing :: Markup",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
    ],
    url="https://myst-tools.org",
    version=__version__,
    author="Steve Purves",
    author_email="stevejpurves@gmail.com",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.9",
)
