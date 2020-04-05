#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from genie.testbed import load
import json

if __name__ == '__main__':
  ## Import from pyats example: 
  ## https://github.com/CiscoDevNet/pyats-ios-sample/blob/master/pyats_ios_example.py

  # local imports
  import argparse
  from ats.topology import loader
  from my_netbox_module import netbox_utils

  #
  # Connection Setup Section
  #

  parser = argparse.ArgumentParser(description = "standalone parser")
  parser.add_argument('--testbed', dest = 'testbed',
                      type = loader.load)
  args, unknown = parser.parse_known_args()
  '''
  Connection setup to DevNet sandbox
  '''
  testbed_file = args.testbed
  testbed = load(testbed_file)
  device_list = testbed.devices.keys()

  def platform_info(device):  
    #for device in device_list:
    #  testbed.devices[device].connect()
    return testbed.devices[device].parse('show version')

  def interfaces_current(device):
    interfaces = device.learn("interface")

    return interfaces.info

  def neighbors():
    show_cdp_neighbors_detail = testbed.devices[device].parse('show cdp neighbors detail')
    return show_cdp_neighbors_detail

  def parse_device_types(data, device):
    return data['platform']['hardware']['model']

  def interface_post_netbox(device, learn):
    interfaces = interfaces_current(learn).keys()
    for ints in interfaces: 
      netbox_utils.create_netbox_interface(device, ints, 'virtual')
  

while True:    
  for device in device_list:
    testbed.devices[device].connect()
    platform_data = platform_info(device)
    model = parse_device_types(platform_data, device)
    netbox_utils.create_netbox_device_types('Cisco', 'core', model)
    netbox_utils.create_netbox_device(device, 'core', 'Tokyo', 'Shinjyuku', model)
    #netbox_utils.create_netbox_interface(device, interfaces_current(device).keys(), interface_type)
    #print(interfaces_current(testbed.devices[device]))
    interface_post_netbox(device, testbed.devices[device])
  break