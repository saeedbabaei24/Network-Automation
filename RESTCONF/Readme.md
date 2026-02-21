# RESTCONF Interface Retrieval 

This script connects to a Cisco IOS-XE device and fetches data from the `ietf-interfaces` YANG model.

Install dependency:
pip install requests

The script uses the following RESTCONF path:
https://<device-ip>/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2
