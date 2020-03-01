import pynetbox

APIENDPOINT = 'http://localhost:32768'
NETBOXURL = 'http://localhost:32768'
NETBOXTOKEN = '0123456789abcdef0123456789abcdef01234567'

# Create netbox API object
netbox = pynetbox.api(url=NETBOXURL, token=NETBOXTOKEN)

nb_device = netbox.dcim.devices.get(name="nwt")
if nb_device is None:
  r = netbox.dcim.device_roles.get(name="core")
  print(r.id)
  netbox.dcim.devices.create(
    name="nwt",
    device_type=1,
    device_role=r.id,
    site="shinjyuku"
    )

nb_manufacturer = netbox.dcim.manufacturers.get(name="Cisco")
print(nb_device)
print(nb_manufacturer.id)