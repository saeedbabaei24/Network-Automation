from pyats.topology import loader

def get_serial(ip: str, username: str, password: str, os: str = "iosxe") -> str:
    tb = {
        "testbed": {"name": "ztp"},
        "devices": {
            "dut": {
                "os": os,
                "type": "router",
                "credentials": {
                    "default": {"username": username, "password": password},
                   
                    "enable": {"password": password},
                },
                "connections": {
                    "cli": {
                        "protocol": "ssh",
                        "ip": ip,
                        "port": 22,
                        "arguments": {
                            "connection_timeout": 30,
                            "learn_hostname": True,
                            "init_exec_commands": [],   
                            "init_config_commands": [], 
                        },
                    }
                },
            }
        },
    }

    testbed = loader.load(tb)
    dev = testbed.devices["dut"]

    
    dev.connect(log_stdout=True)

    out = dev.execute("show version")
    dev.disconnect()

    serial = None
    for line in out.splitlines():
        if "Processor board ID" in line:
            serial = line.split()[-1].strip()
            break

    if not serial:
        raise RuntimeError("Serial not found (expected 'Processor board ID' in show version).")

    return serial
