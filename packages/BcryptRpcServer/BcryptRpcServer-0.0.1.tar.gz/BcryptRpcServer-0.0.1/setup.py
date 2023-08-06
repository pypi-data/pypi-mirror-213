#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import BcryptRpcServer

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="BcryptRpcServer",
    version=BcryptRpcServer.__version__,
    author="cyal1",
    author_email="admin@example.com",
    description="The rpc server api of https://github.com/cyal1/BcryptMontoya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyal1/BcryptRpcServer/tree/main/python",
    py_modules=['BcryptRpcServer'],
    install_requires=[
        "grpc==1.0.0",
        "grpcio==1.54.2",
        "protobuf==4.23.2"
        ],
    classifiers=[
        # "Topic :: Software Development :: Libraries :: Python Modules",
        # "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.5",
        # "Programming Language :: Python :: 3.5",
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: 3.10",
        # 'Programming Language :: Python :: Implementation :: CPython',
    ],
)
