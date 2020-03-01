import pynetbox

APIENDPOINT = 'http://localhost:32768'
NETBOXURL = 'http://localhost:32768'
NETBOXTOKEN = '0123456789abcdef0123456789abcdef01234567'

# Create netbox API object
netbox = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)

nb_device = netbox.dcim.devices.get(name="cat1")
nb_manufacturer = netbox.dcim.manufacturers.get(name="Cisco")
print(nb_device)
print(nb_manufacturer.id)