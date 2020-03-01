import unittest

from netbox_utils import *

name = "Arista"

class netbox_utils_test(unittest.TestCase):
  """test module to test search function in `netbox_utils.py` """

  def netbox_manufacturer(self):
    ## 登録されているデバイスの製造メーカの情報を取得
    nb_manufacturer = netbox.dcim.manufacturers.get(name=name)
    print(nb_manufacturer)
    
    return nb_manufacturer

  def test_netbox_manufacturer(self):
    """key should be found, return list should not be empty because specified key is exist"""
    assert netbox_manufacturer(self) == None
    print(netbox_manufacturer(name))

  #def test_netbox_device(self):
  #  assert netbox_device(manufacturer, hostname, role) == raise RequestError

if __name__ == '__main__':
    unittest.main()
    