from genie.testbed import load
import yaml
import ipaddress
from jinja2 import Environment, FileSystemLoader

COMMON_FILE = "common.yaml"
ROUTERS_FILE = "devices_data.yaml"
TEMPLATE_FILE = "base.j2"   # templates/base.j2


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def ask_ip():
    while True:
        ip = input("Enter device IP: ").strip()
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            print("Invalid IP address, please try again.")


def get_serial(dev):
    serial = None
    try:
        parsed = dev.parse("show version")
        serial = parsed.get("version", {}).get("chassis_sn")
    except Exception:
        pass

    if not serial:
        raw = dev.execute("show version | i serial|Processor board ID")
        for line in raw.splitlines():
            if "Processor board ID" in line:
                serial = line.split("Processor board ID")[-1].strip()
                break
            if ":" in line and "serial" in line.lower():
                serial = line.split(":")[-1].strip()
                break

    if not serial:
        raise RuntimeError(f"Serial not found for {dev.name}")

    return serial


def render_config(common, router):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
    tpl = env.get_template(TEMPLATE_FILE)
    return tpl.render(common=common, router=router)


def push_config(dev, cfg_text):
    lines = []
    for line in cfg_text.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        if line.strip().lower() == "end":
            continue
        lines.append(line)

    dev.configure(lines)
    dev.execute("write memory")


def main():
    tb = load("testbed.yaml")
    dev = tb.devices["ztp-device"]

    #  ask user for IP
    device_ip = ask_ip()
    dev.connections["cli"]["ip"] = device_ip

    common = load_yaml(COMMON_FILE)["common"]
    routers = load_yaml(ROUTERS_FILE)["routers"]

    print(f"\n=== Connecting to {device_ip} ===")

    try:
        dev.connect(log_stdout=True, learn_hostname=True)

        serial = get_serial(dev)
        print(f"Serial: {serial}")

        if serial not in routers:
            raise RuntimeError("Serial not found in devices_data.yaml")

        router = routers[serial]
        cfg = render_config(common, router)

        print("\n--- Generated Config ---")
        print(cfg)

        push_config(dev, cfg)
        print("Config pushed successfully")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        try:
            dev.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()

