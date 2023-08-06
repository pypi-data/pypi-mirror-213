from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    # print(long_description)

setup(
    name="hardyweinberg_equilibrium",
    version="0.1.3",
    author="Dellius Alexander",
    author_email="info@hyfisolutions.com",
    maintainer="info@hyfisolutions.com",
    maintainer_email="info@hyfisolutions.com",
    description='Hardy-Weinberg Equilibrium Calculator. '
                'Calculates the expected genotype frequencies '
                'based on the allele frequencies of a population '
                'in Hardy-Weinberg equilibrium.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/dellius-alexander/FastAPI-GraphQL-MongoDB-Demo.git",
    packages=find_packages(where="Hardy-Weinberg/hardyweinberg_equilibrium"),
    # package_dir={"hardyweinberg_equilibrium": "hardyweinberg_equilibrium"},
    license="LICENSE",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
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
    entry_points={"console_scripts": ["hwe = hardyweinberg_equilibrium.main:app"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "sympy",
        "numpy",
        "matplotlib",
        "pandas",
    ],
)
