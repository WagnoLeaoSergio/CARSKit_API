from setuptools import setup, find_packages

setup(
    name="CARSKit_Interface",
    version="0.0.1",
    description="An API for the CARSKit engine",
    author="me",
    author_email="me@gmai.com",
    install_requires=["cliff"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["capi = capi_proto.capi_cli.main:main"],
        "capi": [
            "run = capi_proto.capi_cli.run:RunEngine",
            "settings = capi_proto.capi_cli.settings:Settings",
        ],
    },
)
