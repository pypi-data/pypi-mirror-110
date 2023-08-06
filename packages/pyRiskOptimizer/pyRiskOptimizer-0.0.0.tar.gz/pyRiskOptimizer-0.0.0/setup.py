from setuptools import setup, find_packages

#
# How to install:
#
#    python3 setup.py sdist
#    twine upload dist/*
#

setup(
    name="pyRiskOptimizer",
    version="0.0.0",
    author="Juan D. Velasquez",
    author_email="jdvelasq@unal.edu.co",
    license="MIT",
    url="http://github.com/jdvelasq/pyRiskOptimizer",
    description="Risk Optimizer for Prescriptive Analytics",
    long_description="Risk Optimizer for Prescriptive Analytics",
    keywords="analytics",
    platforms="any",
    provides=["pyRiskOptimizer"],
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    packages=find_packages(),
    package_dir={"pyRiskOptimizer": "pyRiskOptimizer"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
