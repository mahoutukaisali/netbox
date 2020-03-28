#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

from netbox_utils import *

if __name__ == "__main__":
    import csv
    import os

    ## 読ませるパラシを指定して呼び出す
    csv_parameter_sheet = sys.argv[1]

    with open(csv_parameter_sheet, 'r') as f:
        dictData = csv.DictReader(f)

        for data in dictData:
            ## あとでパラシから取り込めるようにする
            try:
              manufacturer = data.get('manufacturer')
              create_netbox_manufacturer(manufacturer)
              print('Success. The function name: netbox_manufacturer')
            except:
              print('Failed: netbox_manufacturer')
              
            ## Create data of device modle such as catalyst, F5 etc.
            try:
                manufacturer = data.get('manufacturer')
                device_role = data.get('role')
                model = data.get('model')
                create_netbox_device_types(manufacturer, device_role, model)
                print('Success. The function name: netbox_device_types')
            except:
                print('Failed. The fuction name: netbox_device_types')
                #print(create_netbox_device_types(manufacturer, role, model))

            try:
                site = data.get('site')
                tenant = data.get('Tenant')
                hostname = data.get('hostname')
                create_netbox_device(hostname, device_role, tenant, site, device_type=model)
                print('Success. The function name: create_netbox_device')
            except:
                create_netbox_device(hostname, device_role, tenant, site, device_type=model)
                print('Failed. The fuction name: create_netbox_device')
               
            try:
                interface = data.get('interface')
                description = data.get("interface_desctiption")
                interface_type = data.get('interface_type')
                create_netbox_interface(hostname, interface, interface_type)
                print('Success. The fuction name: create_netbox_interface')
            except:
                print('Failed. The fuction name: create_netbox_interface')
                
                
