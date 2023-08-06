from setuptools import setup
with open("README.md","r")as fh:
    long_description= fh.read()
setup(
    name = 'fayadateconverter',
    version = '0.0.1',
    description = 'Calendar_gregorian_hijri_jalali',
    author = 'Fatemeh Yahyapour',
    packages=['fayadateconverter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )
