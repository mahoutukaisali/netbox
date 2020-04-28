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

class PyATS(object):
  def __init__(self, testbed):
    self.testbed = testbed

  def platform_info(self, device):  
    """Collect device information before regist hosts"""
    #for device in device_list:
    #  testbed.devices[device].connect()
    return self.testbed.devices[device].parse('show version')

  def interfaces_learn(self, device):
    """Detect all of interfaces from device and learn them."""
    interfaces = device.learn("interface")
    return interfaces.info

  def parse_device_types(self, device):
    """Parse device type from show version command"""
    return self.platform_info(device)['platform']['hardware']['model']


  def collect_interface_only_up_status(self, device):
    """Collect only up status interfaces except mgmt0."""
    interface_list = []
    print(interface_list)
    interface = self.testbed.devices[device].parse('show interface brief')
    for value in interface["interface"].values():
      for eth, v in value.items():
        if eth == "mgmt0":
          pass
        else:
          if v["status"] == 'up':
            interface_list.append(eth)
    return interface_list

  def collect_cdp_neighbors(self, device):
    """collect cdp neighbors information"""
    show_cdp_neighbors_detail = self.testbed.devices[device].parse('show cdp neighbors detail')
    return show_cdp_neighbors_detail
