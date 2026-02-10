from genie.testbed import load

def get_serial(dev):
    serial = None

    # Attempt 1: structured parser
    try:
        parsed = dev.parse("show version")
        serial = parsed.get("version", {}).get("chassis_sn")
    except Exception as e:
        print(f"[WARN] show version parser failed on {dev.name}: {e}")

    # Attempt 2: raw CLI fallback (more reliable)
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
        raise RuntimeError(f"Serial number not found for {dev.name}")

    return serial

def main():
    tb = load("testbed.yaml")

    for name, dev in tb.devices.items():
        print(f"\n=== {name} ({dev.connections.get('cli', {}).get('ip', 'unknown')}) ===")
        try:
            print("Connecting to device ...")
            dev.connect(log_stdout=True)

            serial = get_serial(dev)
            print(f"SERIAL NUMBER: {serial}")

        except Exception as e:
            print(f"[ERROR] {name}: {e}")

        finally:
            try:
                dev.disconnect()
            except Exception:
                pass

if __name__ == "__main__":
    main()
