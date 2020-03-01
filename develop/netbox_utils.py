#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os, sys
import pynetbox

## 定数は大文字にする
## The publicly netbox Docker info. This is common
APIENDPOINT = 'http://localhost:32768'
NETBOXURL = 'http://localhost:32768'
NETBOXTOKEN = '0123456789abcdef0123456789abcdef01234567'

# Create netbox API object
netbox = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)

def netbox_manufacturer(name):
    ## 登録されているデバイスの製造メーカの情報を取得
    nb_manufacturer = netbox.dcim.manufacturers.get(name=name)
    
    ## 意図したメーカーの登録がなければ作成
    if nb_manufacturer is None:
        nb_manufacturer = netbox.dcim.manufacturers.create(
            name=name
        )
    else:
        pass
    
    return nb_manufacturer

def netbox_device(hostname, role, model):
    """Get and Create a device in netbox based on a Parameter Sheet."""

    ## Get device info if it is exist in netbox
    ##　全く同じ名前で複数登録できてしまうのでこの工程は必要
    nb_device = netbox.dcim.devices.get(name=hostname)
   
    ## Device manufacturer must be associated with created device
    #if nb_device is None:
        #

        ## Create device in netbox if it doesn't exist
    if nb_device is None:
        nb_manufacturer = netbox_manufacturer("Cisco")
        device_slug=(
            str(hostname).lower()
            .replace(" ", "-")
            .replace(",", "-")
            .replace(".", "_")
            .replace("(", "_")
            .replace(")", "_")
            .replace("ー", "-")
        )

        nb_device_type = netbox.dcim.device_types.create(
            #manufacturer=nb_manufacturer.id,
            manufacturer=nb_manufacturer.id,
            ## fix after conforming parameter sheet format
            model=model,
            display_name=hostname,
            ## this is rack unit parameter. make sure what does mean of later.
            u_height=1,
            slug=device_slug,
            subdevice_role=role
        )

    return nb_device_type

#all_prefixes = nb.dcim.devices.all()
#
#print(all_prefixes)
#
### siteには番号が振られているのでそれを指定すると自動で指定される
#nb.dcim.devices.create(
#    name='fujitsu-device1',
#    device_role=1,
#    site=1,
#    device_type=1,
#    status=1
#)
#
#print(nb.dcim.devices.filter(role='core'))
#
##with open('config.csv', 'r') as f:
##    dictData = csv.DictReader(f)
##    for data in dictData:
##        cable_data = nb.dcim.cables.create(
##            side_a_device=data.get('side_a_device'),
##            side_a_type=data.get('side_a_type'),
##            side_a_name=data.get('side_a_name'),
##            side_b_device=data.get('side_b_device'),
##            side_b_type=data.get('side_b_type'),
##            side_b_name=data.get('side_b_name'),
##            type=data.get('type'),
##            status=data.get('status')
##        )
#
##print(cable_data)
#
##"cables": {"endpoint": netbox.dcim.cables}
#print(nb.dcim.cables.filter(device='cat2'))
#print(nb.dcim.cables.all())
### returning json if it's fail to create
#try:
#    nb.dcim.dvices.create(name="destined-for-failure")
#except pynetbox.RequestError as e:
#    print(e.error)
