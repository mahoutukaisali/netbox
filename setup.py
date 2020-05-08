# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
import re

#package_name = "my_netbox_module"

root_dir = path.abspath(path.dirname(__file__))
filename = path.join(root_dir, 'requirement.txt')

def _requirements(filename):
    return open(filename).read().splitlines()

setup(
    name="netboxPackage",
    version="1.0",
    packages=["netboxPackage"],
    package_dir={"": "lib"},
    include_package_data=True,
    install_requires=_requirements(filename),
)