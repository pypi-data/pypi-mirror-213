from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.4"
DESCRIPTION = "Samay"
LONG_DESCRIPTION = """Samay is a powerful Python module designed to help you effectively measure the 
                      execution time of your functions, compare them side by side, and optimize their
                      performance. With Samay, you can gain valuable insights into the efficiency of 
                      your code and make informed decisions to improve its speed and effectiveness."""

# Setting up
setup(
    name="Samay",
    version=VERSION,
    author="Saurav Sharma",
    author_email="sv19projects@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["matplotlib"],
    keywords=["Samay","samay","timeit","time","execution","execution time","run time","runtime","function runtime","function execution time","compare function"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)