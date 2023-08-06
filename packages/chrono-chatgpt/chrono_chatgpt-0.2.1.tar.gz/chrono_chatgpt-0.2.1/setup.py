import setuptools
from setuptools import version

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chrono_chatgpt',
    version='0.2.1',
    author="ChronoWalker",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liaoyuzh/chrono-chatgpt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)