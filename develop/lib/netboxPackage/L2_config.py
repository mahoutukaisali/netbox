"""This script posts L1 configration into netbox."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
## Import from pyats example: 
## https://github.com/CiscoDevNet/pyats-ios-sample/blob/master/pyats_ios_example.py

import argparse
from ats.topology import loader
from genie.testbed import load
import json

def platform_info(device):  
  """Collect device information before regist hosts"""
  #for device in device_list:
  #  testbed.devices[device].connect()
  return testbed.devices[device].parse('show version')

def interfaces_current(device):
  """detect all of interfaces from device"""
  interfaces = device.learn("interface")
  return interfaces.info

def parse_device_types(data, device):
  return data['platform']['hardware']['model']

def interface_post_netbox(device, learn):
  """Post all of device's interfaces."""
  interfaces = interfaces_current(learn).keys()
  for ints in interfaces: 
    netbox_utils.create_netbox_interface(device, ints, 'LAG')

def collect_interface_only_up_status(device):
  """Collect only the up status interfaces if others are not neccesary."""
  interface_list = []
  interface = testbed.devices[device].parse('show interface brief')
  for value in interface["interface"].values():
    for eth, v in value.items():
      if eth == "mgmt0":
        pass
        if v["status"] == 'up':
          interface_list.append(eth)
  return interface_list

def collect_cdp_neighbors(device):
  show_cdp_neighbors_detail = testbed.devices[device].parse('show cdp neighbors detail')
  return show_cdp_neighbors_detail

def post_cdp_neighbors(device):
  """post cdp neighbors.
  - hostname_a -> local host
  - hostname_b -> remote host
  """
  for value in collect_cdp_neighbors(device)['index'].values():
    if value.get('local_interface') != "mgmt0":
      local_interface_name = value.get('local_interface')
      remote_device_name = value.get("system_name")
      remote_interface_name = value.get('port_id')
      netbox_utils.create_netbox_cable(device, remote_device_name, local_interface_name, remote_interface_name)


