from setuptools import find_packages
from setuptools import setup

setup(name='worldnews',
    packages=find_packages(include=['worldnews']),
    version='1.0.1',
    description='News Extractor',
    author='Cod2h3lp',
    license='MIT',
    install_requires=['bs4', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
