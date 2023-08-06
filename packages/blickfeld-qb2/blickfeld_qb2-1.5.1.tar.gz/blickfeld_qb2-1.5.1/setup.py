from setuptools import find_packages, setup

setup(
    name="blickfeld_qb2",
    version="1.5.1",
    author="Blickfeld GmbH",
    author_email="opensource@blickfeld.com",
    url="https://github.com/Blickfeld/blickfeld-qb2",
    description="Python package to communicate securely with Qb2 LiDAR devices of the Blickfeld GmbH",
    packages=find_packages(),
    install_requires=[
        "grpclib",
        "numpy"
	],
)

