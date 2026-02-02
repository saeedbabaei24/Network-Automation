import yaml
import getpass
from jinja2 import Template
from netmiko import ConnectHandler

HOSTS_FILE = "hosts.yaml"
DATA_FILE = "router_data.yaml"
TEMPLATE_FILE = "Router_Template.j2"

DEVICE_TYPE = "cisco_ios"

with open(Hosts, "r") as f:
    hosts = yaml.safe_load(f)["hosts"]

with open(DATA_FILE, "r") as f:
    data = yaml.safe_load(f)

with open(Config_Template, "r") as f:
    template_text = f.read()

username = input("Username: ").strip()
password = getpass.getpass("Password: ")

for ip in hosts:
    if ip not in data["routers"]:
        print(f" Skipping {ip} (no data in routers: section)")
        continue

    render_vars = {
        "common": data["common"],
        "router": data["routers"][ip],
    }

    config_text = Template(template_text).render(**render_vars)
    commands = [line for line in config_text.splitlines() if line.strip()]

    print(f"\n=== Rendered Config for {ip} ({data['routers'][ip].get('hostname','')}) ===")
    print(config_text)

    try:
        conn = ConnectHandler(
            device_type=DEVICE_TYPE,
            host=ip,
            username=username,
            password=password
        )

        conn.send_config_set(commands)
        conn.save_config()
        conn.disconnect()

        print(f" Done: {ip}")

    except Exception as e:
        print(f" Failed: {ip} -> {e}")
