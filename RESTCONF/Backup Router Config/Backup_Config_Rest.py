#Backup_running_config.py

import getpass
from pathlib import Path

import requests
import yaml

HOSTS_FILE = "hosts.yaml"
OUT_DIR = "backups"

# Cisco IOS XE REST API endpoint for running config (text/plain)
RUNNING_CFG_PATH = "/api/v1/global/running-config"

# If your routers use self-signed certs, set to False
VERIFY_SSL = False


with open(HOSTS_FILE, "r", encoding="utf-8") as f:
    hosts = yaml.safe_load(f)["hosts"]

username = input("Username: ").strip()
password = getpass.getpass("Password: ")

Path(OUT_DIR).mkdir(exist_ok=True)

if not VERIFY_SSL:
    requests.packages.urllib3.disable_warnings()

for ip in hosts:
    try:
        url = f"https://{ip}{RUNNING_CFG_PATH}"
        r = requests.get(
            url,
            auth=(username, password),
            headers={"Accept": "text/plain"},
            verify=VERIFY_SSL,
            timeout=20,
        )

        if r.status_code == 200:
            outfile = Path(OUT_DIR) / f"{ip}_running-config.txt"
            outfile.write_text(r.text, encoding="utf-8")
            print(f"✅ Backed up {ip} -> {outfile}")
        else:
            print(f"❌ {ip} failed ({r.status_code}): {r.text}")

    except Exception as e:
        print(f"❌ {ip} error: {e}")