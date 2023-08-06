from setuptools import setup

setup(
    name = 'needed-libs',
    packages = ['needed-libs'],
    install_requires = [
        'requests',
        'undetected-chromedriver'
        ],
    version = '0.1'
    )