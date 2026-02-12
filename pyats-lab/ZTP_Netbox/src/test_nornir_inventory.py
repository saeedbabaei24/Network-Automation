from nornir import InitNornir

nr = InitNornir(config_file="config/nornir.yaml")
print("Hosts:", list(nr.inventory.hosts.keys()))

for name, h in nr.inventory.hosts.items():
    print("\n==", name)
    print("hostname:", h.hostname)
    print("platform:", h.platform)
    print("serial:", h.data.get("serial"))
    print("device_type:", h.data.get("device_type"))
    cc = h.data.get("config_context") or {}
    print("config_context keys:", list(cc.keys()))
