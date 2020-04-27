#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

#
# Connection Setup Section
#

import argparse
import os
import pynetbox
from ats.topology import loader
from genie.testbed import load
import netboxPackage.L2_config as l2
import netboxPackage.my_netbox as netbox_utils
import json

# Create netbox API object
NETBOXURL = os.environ["NETBOXURL"]
NETBOXTOKEN = os.environ["NETBOXTOKEN"]
login_info = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)
netbox = netbox_utils.Netbox(login_info)

parser = argparse.ArgumentParser(description = "standalone parser")
parser.add_argument('testbed', type = loader.load)
args, unknown = parser.parse_known_args()

'''
Connection setup to DevNet sandbox
'''

testbed_file = args.testbed
testbed = load(testbed_file)
device_list = testbed.devices.keys()

for device in device_list:
  testbed.devices[device].connect()
  platform_data = l2.platform_info(device)
  model = l2.parse_device_types(platform_data, device)
  netbox.create_netbox_device_types('Cisco', 'core', model)
  netbox.create_netbox_device(device, 'core', 'Tokyo', 'Shinjyuku', model)

  for inter in l2.collect_interface_only_up_status(device):
    netbox.create_netbox_interface(device, inter, "100base-tx")

for device in device_list:  
  testbed.devices[device].connect()
  l2.post_cdp_neighbors(device)