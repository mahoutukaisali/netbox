#! /usr/bin/env python

from netbox_utils import *

if __name__ == "__main__":
    import csv
    import os

    ## 読ませるパラシを指定して呼び出す
    csv_parameter_sheet = sys.argv[1]

    with open(csv_parameter_sheet, 'r') as f:
        dictData = csv.DictReader(f)
        try:
            manufacturer = "test"
            netbox_manufacturer(manufacturer)
            print('Success. The function name: netbox_manufacturer')
        except:
            print('Failed: netbox_manufacturer')

        for data in dictData:
            ## あとでパラシから取り込めるようにする
            try:
                manufacturer = "Cisco"
                hostname = "nwtm"
                #role = "本番勘定_疎通確認"
                role = "core"
                model = "NSX"
                netbox_device(manufacturer, hostname, role, model)
                print('Success. The function name: netbox_device')
            except:
                print('Failed. The fuction name: netbox_device')
            
            try:
                interface = 'ge-0/0/0'
                description = "mgmt_only"
                netbox_interface(hostname, interface, description)
                print('Success. The fuction name: netbox_device')
            except:
                print('Failed. The fuction name: netbox_interface')
                print(netbox_interface(hostname, interface, description))








