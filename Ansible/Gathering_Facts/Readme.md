#  Ansible – Gathering Facts (Cisco IOS)

This lab demonstrates how to use **Ansible** to collect operational data from a Cisco IOS device using the `cisco.ios.ios_facts` module.

The playbook gathers interface-related facts, stores the output as a structured JSON file, and prints selected device information (hostname and version).


##  Objective

- Collect device facts from Cisco IOS
- Limit fact collection to interface-related data
- Store structured output in JSON format
- Extract and display specific device information


