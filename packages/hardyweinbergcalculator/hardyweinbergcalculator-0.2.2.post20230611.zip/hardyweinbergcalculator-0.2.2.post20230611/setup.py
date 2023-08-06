from setuptools import setup, find_packages
from hardyweinbergcalculator import __VERSION__
VERSION = __VERSION__
DESCRIPTION = 'Hardy-Weinberg Equilibrium Calculator. Calculates the expected genotype frequencies based on the ' \
              'allele frequencies of a population in Hardy-Weinberg equilibrium.'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="hardyweinbergcalculator",
    version=VERSION,
    author="Dellius Alexander",
    author_email="info@hyfisolutions.com",
    maintainer="info@hyfisolutions.com",
    maintainer_email="info@hyfisolutions.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dellius-alexander/Hardy-Weinberg.git",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": [
            "hwc = hardyweinbergcalculator.__main__:app"
        ]
    },
    python_requires=">=2.7",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "sympy",
        "numpy",
        "matplotlib",
        "pandas",
    ],
    keywords=[
        "hardy-weinberg-equilibrium",
        "hardy-weinberg-equilibrium-calculator",
        "hardy-weinberg-calculator",
        "chi-square",
        "chi-square-test"
    ]
)
