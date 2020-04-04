#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Lisa Oh
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
import unittest

from netbox_utils import *
import pynetbox

login_info = credentials.credentials()
APIENDPOINT = login_info.get('APIENDPOINT')
NETBOXURL = login_info.get('NETBOXURL')
NETBOXTOKEN = login_info.get('NETBOXTOKEN')

# Create netbox API object
netbox = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)

name = "Cisco"

class netbox_utils_test(unittest.TestCase):
  """test module to test search function in `netbox_utils.py` """

  def netbox_manufacturer(name):
    ## 登録されているデバイスの製造メーカの情報を取得
    nb_manufacturer = netbox.dcim.manufacturers.get(name=name)
    
    return nb_manufacturer


  #def test_netbox_manufacturer(self):
  #  """key should be found, return list should not be empty because specified key is exist"""
  #  assert netbox_manufacturer(self) == None
  #  print(netbox_manufacturer(name))

  #def test_netbox_device(self):
  #  assert netbox_device(manufacturer, hostname, role) == raise RequestError

if __name__ == '__main__':
    #unittest.main()
    #model = netbox.dcim.device_types.get(model='Catalyst')
    #model = netbox.dcim.device_types.all()
    #nb_device = netbox.dcim.devices.get(name='cat1')
    #print(nb_device)
    #print(model)

    #tenant_site_slug = (
    #        ## tenant and site slug have common roles
    #        str('Tokyo').lower()
    #        .replace(" ", "-")
    #        .replace(",", "-")
    #        .replace(".", "_")
    #        .replace("(", "_")
    #        .replace(")", "_")
    #        .replace("ー", "-")
    #    )
    #print(netbox.tenancy.tenants.get(slug='tenant_site_slug', name='Tokyo'))

    #site = netbox.dcim.sites.get(name='Shinjyuku')
    #site = netbox.dcim.sites.get(name='site_test', slug=tenant_site_slug)
    #print(site)

    #tenant = netbox.tenancy.tenants.get(name='test_tenant')
    #print(tenant)

    #hostname = 'test_host'

    #nb_device_data = netbox.dcim.devices.create(
    #        name = hostname,
    #        tenant = tenant.id,
    #        site = site.id,
    #        device_role = 'test_role',
    #        device_type = 'test_type'
    #        #slug = device_slug
    #    )
    #print(nb_device_data)

    #model = netbox.dcim.device_types.get(model='Nexus')
    nb_device = netbox.dcim.devices.get(name='r4')
    #nb_device_id = nb_device.id
    nb_interfaces = netbox.dcim.interfaces.all()
    #nb_interfaces = netbox.dcim.interfaces.get(
    #        #device=nb_device,
    #        name='ge-0/0/0'
    #        #type='virtual'
    #        #description='mgmt_only'
    #    )
    
    #nb_interfaces = netbox.dcim.interfaces.all()
    
    print(nb_interfaces)