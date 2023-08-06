from setuptools import find_packages, setup

setup(
    name='deviceID',
    packages=find_packages(include=['deviceID']),
    version='0.1.1',
    description='deviceID python client',
    author='deviceID',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
