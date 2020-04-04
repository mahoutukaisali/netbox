#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from genie.testbed import load


#
# Connection Setup Section
#

#class connection_setup(object):
'''
Connection setup to DevNet sandbox
'''

def establish_connections(testbed, device_list):
  if isinstance(device_list, list):
      #load our testbed yaml
      testbed = load(testbed)
      # connect to the device
      for device in device_list:
          testbed.devices[device].connect()
          output = testbed.devices[device].parse('show version')
          print(output)

## Import from pyats example: 
## https://github.com/CiscoDevNet/pyats-ios-sample/blob/master/pyats_ios_example.py
if __name__ == '__main__':

    # local imports
    import argparse
    from ats.topology import loader

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)
    # parse args
    args, unknown = parser.parse_known_args()

    # and pass all arguments to aetest.main() as kwargs
    #aetest.main(**vars(args))
    device_list = ['dist3', 'dist4']
    establish_connections(args.testbed, device_list)