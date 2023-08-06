from setuptools import setup, find_packages
import io
from os import path

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nalyst",
    version="1.1.0",
    author="Hemant Thapa, Kiran Basnet",
    author_email="hemantthapa1998@gmail.com, kiransbasnet@gmail.com",
    description="Packages for quantative analyst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harryworlds/nalyst",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="Proprietary License",
    license_file="LICENSE.txt",
    keywords="pandas, random, numpy, pandas datareader, seaborn, matplotlib",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.16.5",
        "requests>=2.26.0",
        "seaborn>=0.11.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={"test": ["pytest>=6.2.4", "coverage>=5.5"]},
    python_requires=">=3.6",
)
