import requests
import yaml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cfg = yaml.safe_load(open("config/netbox.yaml"))

url = cfg["netbox"]["url"]
token = cfg["netbox"]["token"]

r = requests.get(
    f"{url}/api/",
    headers={"Authorization": f"Token {token}"},
    timeout=10,
    verify=False,   
)

print("HTTP status:", r.status_code)
print("Body snippet:", r.text[:200])
r.raise_for_status()
print("OK: NetBox API reachable")

