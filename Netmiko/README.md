# Netmiko Cisco Config Push + Running-Config Backup

This repository contains a simple Python automation script that uses Netmiko to:

- Connect to a Cisco IOS device over SSH  
- Enter enable mode  
- Push configuration commands from a local file (`config.txt`)  
- Retrieve the device running-config and save it as a backup  
- Save logs for troubleshooting and auditing

bash:
pip install netmiko
