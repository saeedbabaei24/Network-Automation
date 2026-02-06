from netmiko import ConnectHandler
import logging

# Netmiko internal debug log (separate file)
logging.basicConfig(filename="netmiko_debug.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

device = {
    "device_type": "cisco_ios",
    "host": "1IP",
    "username": "USER",
    "password": "PASS",
    "session_log": "session_log.txt",   # full SSH transcript
}

conn = ConnectHandler(**device)

# enter enable mode (needed on many Cisco devices for config)
conn.enable()

# 1) Push config from file
output = conn.send_config_from_file("config.txt")
print(output)

# 2) Backup running-config to file
running = conn.send_command("show running-config")
with open("running-config-backup.txt", "w", encoding="utf-8") as f:
    f.write(running)

conn.disconnect()
print("Done. Backup + logs saved.")
