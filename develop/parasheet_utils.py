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
                role = data.get('role')
                model = data.get('model')
                create_netbox_device_types(manufacturer, role, model)
                print('Success. The function name: netbox_device_types')
            except:
                print('Failed. The fuction name: netbox_device_types')
                print(create_netbox_device_types(manufacturer, role, model))

            try:
                site = 'Minato'
                tenant = '_tokyo'
                device_role = 'core'
                #hostname = data.get('hostname') 
                hostname = 'S1'
                create_netbox_device(hostname, device_role, tenant, site, device_type=model)
                print('Success. The function name: create_netbox_device')
            except:
                create_netbox_device(hostname, device_role, tenant, site, device_type=model)
                print('Failed. The fuction name: create_netbox_device')
               
            #try:
            #    hostname = data.get('hostname')
            #    interface = data.get('interface')
            #    description = data.get("mgmt_only")
            #    create_netbox_interface(hostname, interface, description)
            #    print('Success. The fuction name: netbox_device')
            #except:
            #    print('Failed. The fuction name: netbox_interface')
                
                
