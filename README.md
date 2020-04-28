# Get started managing your inventory by Netbox!
I built this application as a kick start Netbox tool with our network devices.

![GitHub Logo](mynetbox_slide.png)

## Dependencies
This project relies on following packages
- Netbox (including pynetbox version `4.2.5`)
- pyATS - version must be at least `20.1`
- Docker - version must be at least `17.05`<br>

## Project Goals
I have been wanted to manage a bulk of network device's inventories and port connection information by Netbox instead of is too complicated Excel files. So this project aims to register each devices of interface, site location, rack, and neighbors by CDP configuration.<br>
 However the problem was how to register these amount of device's information into Netbox. By manual? That's not practical solution.  
 Fortunatly I have excel files and pyATS awesome powerful tool can convert this excel file to Testbed file so I've decided to use them. Want more learning pyATS & Excel file? You can see: https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html#creation-from-excel-file
 
Specifically this application tackles the following.

    Register device's manufacturer 
    Register device's name, device type(such as Nexus-9000, catalyst-2950 etc.) and interface
    Register device's CDP neighbor (which means register which interfaces and which interfaces are connected by cable)
    Register site location and rack
    
## Running The Demo Yourself
1. Prepare pyATS testbed
- If you Run Using DevNet SandBox
As you can see pyats/The-Open-NX-OS-Sandbox.yaml file, you can use this testbed to connect DevNet SandBox name "Open NX-OS Sandbox"

- Otherwise please prepare testbed.yaml yourself  

2. Prepare Netbox environment
If you'd prepared Netbox by Docker, execute following commands to post api to Netbox.
```
export NETBOXURL='http://localhost:80'
export NETBOXTOKEN='0123456789abcdef0123456789abcdef01234567'
```

3. Run Script
Now you run the script by following command.
```
python main.py pyats/ 
```
**Note**: You'll might see that all of interfaces are **NOT** registered but several interfaces are registered because default main.py uses `collect_interface_only_up_status()` function which only registers up status interfaces.

## Caveats / Known Issues / Later Updates / Note
- Since netbox cannot register more than one cable for a single port, I excluded the cable registration for the management port. So you cannot see mgmt0 with cable status. I'll solve how to register them later.
- Plan to add a function to register the rack information of the device.
- Make it possible to install the python library of this repository with pip install
