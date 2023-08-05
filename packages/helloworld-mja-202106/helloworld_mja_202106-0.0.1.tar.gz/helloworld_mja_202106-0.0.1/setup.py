# Copyright (C) 2021 Mina Jamshidi
# <minajamshidi91@gmail.com>

from setuptools import setup

with open('README.md', "r") as fh:
    long_description = fh.read()

setup(
    author='Mina Jamshidi',
    author_email='minajamshidi91@gmail.com',
    url='https://github.com/minajamshidi/helloworld',
    name='helloworld_mja_202106', # this is the name that you pip install, it does not have to be the same as the module name
    version='0.0.1',  # 0.0.x implies that it is still unstable
    description='Say hello!',  # one line usually
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["helloworld"],  # the list of actual python modules
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    #    "numpy>=1.10",
    # ],
    extras_require={
        "dev": [
                "pytest>=3.7",
                "check-manifest>=0.40",
        ],
    },
)

