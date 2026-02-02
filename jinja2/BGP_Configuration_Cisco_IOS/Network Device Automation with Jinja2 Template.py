import yaml
import getpass
from jinja2 import Template
from netmiko import ConnectHandler
 
# files
HOSTS_FILE = "hosts.yaml"
DATA_FILE = "bgp.yaml"
TEMPLATE_FILE = "BGP_Template.j2"
 
DEVICE_TYPE = "cisco_ios"   # change if needed
 
 
# read hosts
with open(HOSTS_FILE, "r") as f:
    hosts = yaml.safe_load(f)["hosts"]
 
# read data
with open(DATA_FILE, "r") as f:
    data = yaml.safe_load(f)
 
# read template
with open(TEMPLATE_FILE, "r") as f:
    template_text = f.read()
 
# render config
config_text = Template(template_text).render(**data)
 
print("\n=== Rendered Config ===")
print(config_text)
 
# credentials
username = input("Username: ").strip()
password = getpass.getpass("Password: ")
 
# push to routers
for ip in hosts:
    try:
        conn = ConnectHandler(
            device_type=DEVICE_TYPE,
            host=ip,
            username=username,
            password=password
        )
 
        commands = [line for line in config_text.splitlines() if line.strip()]
        conn.send_config_set(commands)
        conn.save_config()
        conn.disconnect()
 
        print(f" Done: {ip}")