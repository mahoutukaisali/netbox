#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import csv
import os, sys
import pynetbox
import credentials

## 定数は大文字にする
## The publicly netbox Docker info. This is common
login_info = credentials.credentials()
APIENDPOINT = login_info.get('APIENDPOINT')
NETBOXURL = login_info.get('NETBOXURL')
NETBOXTOKEN = login_info.get('NETBOXTOKEN')

# Create netbox API object
netbox = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)

def slug(value):
    value_slug = (
        str(value).lower()
        .replace(" ", "-")
        .replace(",", "-")
        .replace(".", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("ー", "-")
    )

    return value_slug


def create_netbox_manufacturer(name):
    ## 登録されているデバイスの製造メーカの情報を取得
    nb_manufacturer = netbox.dcim.manufacturers.get(name=name)

    ## 意図したメーカーの登録がなければ作成
    if nb_manufacturer is None:
        nb_manufacturer = netbox.dcim.manufacturers.create(
            name=name,
            slug=name
        )

    return nb_manufacturer

def create_netbox_device_types(manufacturer, role, model):
    """Get and Create a device in netbox based on a Parameter Sheet."""

    ## Get device info if it is exist in netbox
    ##　Catalystなどデバイスのモデルタイプの情報が既に存在するかどうか確認sるう
    nb_device = netbox.dcim.device_types.get(model=model)
    
    ## Create device in netbox if it doesn't exist
    if nb_device is None:
        ## device_type does't mean create device. This defines manufacturer and model
        #nb_manufacturer = netbox_manufacturer("Cisco")
        ## device will be associated these three types of data so retrieve first
        nb_manufacturer = netbox.dcim.manufacturers.get(name=manufacturer)
        role = netbox.dcim.device_roles.get(name=role)
        ## name (str) – Name of endpoint passed to App().
        ## model (obj,optional) – Custom model for given app. <- cannot run this script multiple times with it

        device_slug=(slug(model))

        nb_device_type = netbox.dcim.device_types.create(
            #manufacturer=nb_manufacturer.id,
            manufacturer=nb_manufacturer.id,
            ## fix after conforming parameter sheet format
            model=model,
            display_name=model,
            ## this is rack unit parameter. make sure what does mean of later.
            u_height=1,
            slug=device_slug,
            subdevice_role=role.id
        )
    
        return nb_device_type

def create_netbox_device(hostname, device_role, tenant, site, device_type=str):
    nb_device = netbox.dcim.devices.get(name=hostname)
    
    if nb_device == None:
        ## device role and types are already exists by above's functions.
        device_role = netbox.dcim.device_roles.get(name=device_role)
        device_type = netbox.dcim.device_types.get(model=device_type)
        ## ex.) site == NYC
        site_value = netbox.dcim.sites.get(name=site)
        ## ex.) tenant == U.S.
        tenant_value = netbox.tenancy.tenants.get(name=tenant)

        tenant_slug = (slug(tenant))
        site_slug = (slug(site))

        if site_value == None:
            netbox.dcim.sites.create(name=site, slug=site_slug)
            ## redifine to get id
            site_value = netbox.dcim.sites.get(name=site)
        
        ## To slug tenant argument, using variable name as tenant_slug
        if tenant_value == None:
            
            ## tenantが存在してなければslugも存在していないはず
            netbox.tenancy.tenants.create(name=tenant, slug=tenant_slug)
            ## redifine to get id
            tenant_value = netbox.tenancy.tenants.get(name=tenant)
        
        nb_device_data = netbox.dcim.devices.create(
            name = hostname,
            tenant = tenant_value.id,
            site = site_value.id,
            device_role = device_role.id,
            device_type = device_type.id
        )
       
        return nb_device_data


#def netbox_interface(hostname, interface, type, enable, lag, description, mtu, mac_address, 802_1qmode):
## This function is assumed which is executed after device is created
def create_netbox_interface(hostname, interface, interface_type):
    """Get and Create interfaces in netbox based on a Parameter Sheet."""
    nb_device = netbox.dcim.devices.get(name=hostname)
    
    ## To associate with device which is already exists, once retrieve its device
    nb_interface = netbox.dcim.interfaces.get(
            device=nb_device, 
            name=interface
        )
    
    ## create interface if it's not already exists.
    if nb_interface is None:
        
        ## interface type must be either lag or virtual.
        nb_interface = netbox.dcim.interfaces.create(
                device=nb_device.id, 
                name=interface,
                type=interface_type
            )
        
        return nb_interface

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
