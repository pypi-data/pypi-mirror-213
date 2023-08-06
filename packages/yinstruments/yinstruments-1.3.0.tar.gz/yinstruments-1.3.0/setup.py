from setuptools import setup

setup(
    name="yinstruments",
    packages=["yinstruments"],
    version="1.3.0",
    description="Experiment device control scripts for BYU's Configurable Computing Lab (https://ccl.byu.edu/)",
    author="Jeff Goeders",
    author_email="jeff.goeders@gmail.com",
    url="https://github.com/byuccl/yinstruments",
    install_requires=["pyudev", "pyserial", "pysnmp", "python-vxi11", "pyhubctl"],
)
