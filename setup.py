from setuptools import setup, find_packages

setup(
    # Application name
    name="carskit_api",
    # Version number
    version="0.0.7",
    description="An API for the CARSKit engine",
    # Application author details
    author="WagnoLeaoSergio",
    author_email="wagnoleao@gmail.com",
    # Dependencies
    install_requires=["cliff", "pickleDB", "pymongo", "dnspython", "cryptography"],
    # Packages
    packages=find_packages(),
    python_requires=">=3.6",
    # Details
    # url  = ""
    include_package_data=True,
    # License
    license="LICENSE.txt",
    # ReadMe
    long_description=open("README.md").read(),
    # Package console entry points
    entry_points={
        "console_scripts": ["capi = carskit_api.cli.main:main"],
        "capi": [
            "run = carskit_api.cli.run:RunEngine",
            "settings = carskit_api.cli.settings:Settings",
            "database = carskit_api.cli.database:Database",
        ],
    },
)
