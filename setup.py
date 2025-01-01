from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="mt4bridge",
    version="0.1.0",
    description="A bridge to communicate between Python and MT4 using ZeroMQ.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/slaats/mt4bridge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires="==3.12",
    install_requires=[
        "pyzmq>=22.0.0",
    ],
)
