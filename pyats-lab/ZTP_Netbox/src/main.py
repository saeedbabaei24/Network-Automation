import urllib3 #for disabling the SSL errors if we want to use netbox API
from nornir import InitNornir  #to creat an object for nornir and load inventory (from netbox in this case)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from get_serial_pyats import get_serial
from render import render_config
from push import push_rendered_config


def find_device_by_serial(nr, serial: str) -> str:
    serial = serial.strip()
    matches = []
    for name, h in nr.inventory.hosts.items():
        if (h.data.get("serial") or "").strip() == serial:
            matches.append(name)

    if not matches:
        raise RuntimeError(f"No NetBox device found with serial '{serial}'.")
    if len(matches) > 1:
        raise RuntimeError(f"Multiple devices matched serial '{serial}': {matches}")

    return matches[0]


def main():
    ip = input("Enter initial device IP (SSH enabled): ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    print("\n[1] Reading serial via pyATS...")
    serial = get_serial(ip=ip, username=username, password=password, os="iosxe")
    print("Serial:", serial)

    print("\n[2] Loading NetBox inventory via Nornir...")
    nr = InitNornir(config_file="config/nornir.yaml")

    print("\n[3] Matching serial to NetBox device...")
    device_name = find_device_by_serial(nr, serial)
    print("Matched NetBox device:", device_name)

    print("\n[4] Rendering config...")
    template_path, rendered = render_config(nr, device_name=device_name, debug=True)

    print("\nTemplate:", template_path)
    print("\n---- RENDERED CONFIG ----\n")
    print(rendered)



    from nornir.core.inventory import ConnectionOptions

    h = nr.inventory.hosts[device_name]
    h.hostname = ip
    h.username = username
    h.password = password
    h.platform = "cisco_ios"   # IOSv uses cisco_ios in Netmiko

    # Netmiko enable secret must be here (not in h.data)
    if "netmiko" not in h.connection_options:
        h.connection_options["netmiko"] = ConnectionOptions(extras={})

    h.connection_options["netmiko"].extras["secret"] = password


    ans = input("\nPush this config to device? (yes/no): ").strip().lower()
    if ans == "yes":
        print("\n[5] Pushing config...")
        result = push_rendered_config(nr, device_name=device_name, rendered_cfg=rendered)
        print(result)
        # Print detailed outputs from Nornir results
        mr = result[device_name]
        print("\n===== DETAILED OUTPUTS =====")
        for r in mr:
            print(f"\n--- {r.name} (failed={r.failed}) ---\n")
            print(r.result)


        print("Done.")
    else:
        print("Skipped push.")


if __name__ == "__main__":
    main()
