from setuptools import setup, find_packages

setup(
    name="carskit_api",
    version="0.0.1",
    description="An API for the CARSKit engine",
    author="WagnoLeaoSergio",
    author_email="wagnoleao@gmail.com",
    install_requires=["cliff"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["capi = carskit_api.cli.main:main"],
        "capi": [
            "run = carskit_api.cli.run:RunEngine",
            "settings = carskit_api.cli.settings:Settings",
        ],
    },
)
