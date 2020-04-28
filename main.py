#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import argparse

parser = argparse.ArgumentParser(description='Process post parameters in netbox.')
parser.add_argument('arg1', 
                    help='Please specify the path of parameter csv file.')
parser.add_argument('--arg2', 
                    choices=['manufacturer', 'device_type', 'device', 'interface'],
                    help='''which one would you want to post config ? 
                            choose from: manufacturer, device type, device, interface. default => all
                         '''
                  )

args = parser.parse_args()

if __name__ == "__main__":
    import csv
    import os
    import sys
    from my_netbox_module import netbox_utils

    ## specify path of parameter_sheet which is csv file
    csv_parameter_sheet = args.arg1
    
    with open(csv_parameter_sheet, 'r') as f:
        dictData = csv.DictReader(f)

        if args.arg2 == None:
          print('Start posting all of configurations.')
          for data in dictData:
            manufacturer = data.get('manufacturer')
            device_role = data.get('role')
            model = data.get('model')
            site = data.get('site')
            tenant = data.get('Tenant')
            hostname = data.get('hostname')
            interface = data.get('interface')
            description = data.get("interface_desctiption")
            interface_type = data.get('interface_type')

            if netbox_utils.create_netbox_manufacturer(manufacturer) == None:
              print('Success: create_netbox_manufacturer')
            else:
              print('Failed: create_netbox_manufacturer')
          
            if netbox_utils.create_netbox_device_types(manufacturer, device_role, model) == None:
              print('Success: create_netbox_device_types')
            else:
              print('Failed: create_netbox_device_types')

            if netbox_utils.create_netbox_device(hostname, device_role, tenant, site, device_type=model) == None:
              print('Success: create_netbox_device')
            else:
              print('Failed: create_netbox_device')
            
            if netbox_utils.create_netbox_interface(hostname, interface, interface_type) == None:
              print('Success: create_netbox_interface')
            else:
              print('Failed: create_netbox_interface')
          sys.exit(1)

        elif args.arg2 == 'manufacturer':
          for data in dictData:
            manufacturer = data.get('manufacturer')
            #netbox_utils.create_netbox_manufacturer(manufacturer)
            if netbox_utils.create_netbox_manufacturer(manufacturer) == None:
              print('Success: create_netbox_manufacturer')
            else:
              print('Failed: create_netbox_manufacturer')
          sys.exit(1)

        elif args.arg2 == 'device_type':
          for data in dictData:
            manufacturer = data.get('manufacturer')
            device_role = data.get('role')
            model = data.get('model')
            #netbox_utils.create_netbox_device_types(manufacturer, device_role, model)
            if netbox_utils.create_netbox_device_types(manufacturer, device_role, model) == None:
              print('Success. The function name: create_netbox_device_types')
            else:
              print('Failed. The fuction name: create_netbox_device_types')
          sys.exit(1)

        elif args.arg2 == 'device':
          for data in dictData:
            device_role = data.get('role')
            site = data.get('site')
            tenant = data.get('Tenant')
            hostname = data.get('hostname')
            model = data.get('model')
            #create_netbox_device(hostname, device_role, tenant, site, device_type=model)
            if netbox_utils.create_netbox_device(hostname, device_role, tenant, site, device_type=model) == None:
              print('Success. The function name: create_netbox_device')
            else:
              print('Failed. The fuction name: create_netbox_device')
          sys.exit(1)
               
        elif args.arg2 == 'interface':
          for data in dictData:
            hostname = data.get('hostname')
            interface = data.get('interface')
            description = data.get("interface_desctiption")
            interface_type = data.get('interface_type')
            #create_netbox_interface(hostname, interface, interface_type)
            if netbox_utils.create_netbox_interface(hostname, interface, interface_type) == None:
              print('Success. The fuction name: create_netbox_interface')
              #print(netbox_utils.create_netbox_interface(hostname, interface, interface_type))
            else:
              print('Failed. The fuction name: create_netbox_interface')
              #print(netbox_utils.create_netbox_interface(hostname, interface, interface_type))

          sys.exit(1)