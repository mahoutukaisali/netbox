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
import netboxPackage.get_pyats as pyats
import netboxPackage.netbox_utils as netbox
import json

# Create netbox API object
NETBOXURL = os.environ["NETBOXURL"]
NETBOXTOKEN = os.environ["NETBOXTOKEN"]
login_info = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)
netbox = netbox.Netbox(login_info)

parser = argparse.ArgumentParser(description = "standalone parser")
parser.add_argument('testbed', type = loader.load)
args, unknown = parser.parse_known_args()

'''
Connection setup to DevNet sandbox
'''

testbed_file = args.testbed
testbed = load(testbed_file)
device_list = testbed.devices.keys()

pyats = pyats.PyATS(testbed)

for device in device_list:
  testbed.devices[device].connect()
  platform_data = pyats.platform_info(device)
  model = pyats.parse_device_types(device)
  netbox.create_netbox_device_types('Cisco', 'core', model)
  netbox.create_netbox_device(device, 'core', 'US', 'San Francisco', model)

  for inter in pyats.collect_interface_only_up_status(device):
    netbox.create_netbox_interface(device, inter, "100base-tx")

print("######Complete registering interface information! ######")

for device in device_list:
  testbed.devices[device].connect()
  for value in pyats.collect_cdp_neighbors(device)['index'].values():
    ## If cdp config has mgmt0 and it has multiple connection with others, Netbox
    # cannot manage it so excludes mgmt0 for now.
    if value.get('local_interface') != "mgmt0":
      local_interface_name = value.get('local_interface')
      remote_device_name = value.get("system_name")
      remote_interface_name = value.get('port_id')
      netbox.create_netbox_cable(device, remote_device_name, local_interface_name, remote_interface_name)

print("######Complete registering CDP information! ######")