#! /usr/bin/env python

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
                manufacturer = "Cisco"
                netbox_manufacturer(manufacturer)
                print(netbox_manufacturer(manufacturer))
                print('Sucees: netbox_manufacturer')
            except:
                print('Failed: netbox_manufacturer')
                pass

            try:
                hostname = "nwtm-i9318-zlfc2011"
                #role = "本番勘定_疎通確認"
                role = ""
                netbox_device(manufacturer, hostname, role)
                print('Sucees: netbox_device')
            except:
                print('Failed: netbox_device')
                print(netbox_device(manufacturer, hostname, role))








