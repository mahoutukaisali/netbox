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
            print(netbox_manufacturer(manufacturer))

            print('Sucees: netbox_manufacturer')
        except:
            print('Failed: netbox_manufacturer')
            print(netbox_manufacturer(manufacturer))

        for data in dictData:
            ## あとでパラシから取り込めるようにする
            try:
                manufacturer = "Cisco"
                hostname = "nwtm"
                #role = "本番勘定_疎通確認"
                role = "core"
                model = "NSX"
                print(netbox_device(manufacturer, hostname, role, model))
                print('Sucees: netbox_device')
            except:
                print('Failed: netbox_device')
                #print(netbox_device(hostname, role, model))








