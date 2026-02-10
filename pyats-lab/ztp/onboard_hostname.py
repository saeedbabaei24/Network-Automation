from genie.testbed import load
import yaml

DEVICE_DATA_FILE = "device_data.yaml"

def load_device_data():
    with open(DEVICE_DATA_FILE) as f:
        return yaml.safe_load(f)["devices"]

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

def push_hostname(dev, hostname):
    dev.configure([f"hostname {hostname}"])

def main():
    tb = load("testbed.yaml")
    device_data = load_device_data()

    for name, dev in tb.devices.items():
        print(f"\n=== {name} ===")
        try:
            # IMPORTANT: learn hostname from device prompt (ZTP-friendly)
            dev.connect(log_stdout=True, learn_hostname=True)

            serial = get_serial(dev)
            print(f"Serial: {serial}")

            if serial not in device_data:
                raise RuntimeError("Serial not found in device_data.yaml")

            hostname = device_data[serial]["hostname"]
            print(f"Pushing hostname: {hostname}")

            push_hostname(dev, hostname)
            dev.execute("write memory")

            print("Hostname configured successfully")

        except Exception as e:
            print(f"[ERROR] {name}: {e}")

        finally:
            try:
                dev.disconnect()
            except Exception:
                pass

if __name__ == "__main__":
    main()
