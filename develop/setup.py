# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
import re

#package_name = "my_netbox_module"

#root_dir = path.abspath(path.dirname(__file__))
#
#def _requirements():
#    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

setup(
    name="netboxPackage",
    version="1.0",
    packages=find_packages("lib"),
    package_dir={"": "lib"},
    include_package_data=True,
    #install_requires=_requirements(),
)