from setuptools import setup, find_packages

setup(
    name="the_one_lotr_sdk",
    version="0.1.0",
    url="https://github.com/andrewpos/lotr_sdk",
    author="Andrew Pos",
    author_email="andrewmpos@gmail.com",
    description="SDK for The Lord of the Rings API",
    packages=find_packages(),
    install_requires=["requests==2.25.1"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
