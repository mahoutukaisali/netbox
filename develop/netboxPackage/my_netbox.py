#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import csv
import os, sys
import pynetbox

class Netbox(object):
    def __init__(self, netbox):
        self.netbox = netbox

    def slug(self, value):
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


    def create_netbox_manufacturer(self, name):
        """Get and Create a device manufacturer in netbox based on a Parameter Sheet."""
        ## 登録されているデバイスの製造メーカの情報を取得
        nb_manufacturer = self.netbox.dcim.manufacturers.get(name=name)
    
        ## 意図したメーカーの登録がなければ作成
        if nb_manufacturer is None:
            nb_manufacturer = self.netbox.dcim.manufacturers.create(
                name=name,
                slug=name
            )
    
        return nb_manufacturer

    def create_netbox_device_types(self, manufacturer, role, model):
        """Get and Create a device in netbox based on a Parameter Sheet.
        Create data of device model such as catalyst, F5 etc.
        """
    
        ## Get device model if it has already exists in netbox
        nb_device = self.netbox.dcim.device_types.get(model=model)
        
        ## Create device in netbox if it doesn't exist
        if nb_device is None:
            ## device_type does't mean create device. This defines manufacturer and model
            #nb_manufacturer = netbox_manufacturer("Cisco")
            ## device will be associated these three types of data so retrieve first
            nb_manufacturer = self.netbox.dcim.manufacturers.get(name=manufacturer)
            role = self.netbox.dcim.device_roles.get(name=role)
            ## name (str) – Name of endpoint passed to App().
            ## model (obj,optional) – Custom model for given app. <- cannot run this script multiple times with it
    
            device_slug=(self.slug(model))
    
            nb_device_type = self.netbox.dcim.device_types.create(
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

    def create_netbox_device(self, hostname, device_role, tenant, site, device_type=str):
        nb_device = self.netbox.dcim.devices.get(name=hostname)
        
        if nb_device == None:
            ## device role and types are already exists by above's functions.
            device_role = self.netbox.dcim.device_roles.get(name=device_role)
            device_type = self.netbox.dcim.device_types.get(model=device_type)
            ## ex.) site == NYC
            site_value = self.netbox.dcim.sites.get(name=site)
            ## ex.) tenant == U.S.
            tenant_value = self.netbox.tenancy.tenants.get(name=tenant)
    
            tenant_slug = (self.slug(tenant))
            site_slug = (self.slug(site))
    
            if site_value == None:
                self.netbox.dcim.sites.create(name=site, slug=site_slug)
                ## redifine to get id
                site_value = self.netbox.dcim.sites.get(name=site)
            
            ## To slug tenant argument, using variable name as tenant_slug
            if tenant_value == None:
                
                ## if tenant doesn't exist its slug also doesn't exist. 
                ## So let's create it.
                self.netbox.tenancy.tenants.create(name=tenant, slug=tenant_slug)
                ## redifine to get id
                tenant_value = self.netbox.tenancy.tenants.get(name=tenant)
            
            nb_device_data = self.netbox.dcim.devices.create(
                name = hostname,
                tenant = tenant_value.id,
                site = site_value.id,
                device_role = device_role.id,
                device_type = device_type.id
            )
           
            return nb_device_data


    #def netbox_interface(hostname, interface, type, enable, lag, description, mtu, mac_address, 802_1qmode):
    ## This function is assumed which is executed after device is created
    def create_netbox_interface(self, hostname, interface, interface_type):
        """Get and Create interfaces in netbox based on a Parameter Sheet."""
        nb_device = self.netbox.dcim.devices.get(name=hostname)
        
        ## To associate with device which is already exists, once retrieve its device
        nb_interface = self.netbox.dcim.interfaces.get(
                device=nb_device, 
                name=interface
            )
        
        ## create interface if it's not already exists.
        if nb_interface is None:
            
            ## interface type must be either lag or virtual.
            nb_interface = self.netbox.dcim.interfaces.create(
                    device=nb_device.id, 
                    name=interface,
                    type=interface_type
                )
            
            return nb_interface

    def create_netbox_cable(self, hostname_a, hostname_b, interface_a, interface_b):
        """Posts cable"""
        get_cable = self.netbox.dcim.cables.get(name=interface_a, device=hostname_a)
        if get_cable == None:
          nb_interface_id_a = self.netbox.dcim.interfaces.get(name=interface_a, device=hostname_a).id
          nb_interface_id_b = self.netbox.dcim.interfaces.get(name=interface_b, device=hostname_b).id
          
          self.netbox.dcim.cables.create(
                termination_a_id=nb_interface_id_a, 
                termination_a_type="dcim.interface", 
                termination_b_id=nb_interface_id_b,
                termination_b_type="dcim.interface"
           )
