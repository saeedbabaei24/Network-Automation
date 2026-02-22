# ZTP NetBox Automation (pyATS + Nornir + Jinja2)

This project is a **ZTP-style automation workflow** that uses **NetBox as the source of truth**, renders device configuration using **Jinja2**, and pushes the final config to network devices using **Nornir/Netmiko**.

---

## Folder Structure

ZTP_Netbox/
├── config/                 # inventory / runtime config (if used)
├── datas/                  # YAML data files (source of truth helpers)
│   ├── common.yaml         # shared variables (DNS/NTP/SNMP/logging/...)
│   └── template_map.yaml   # maps device/site/role → template name
├── src/                    # Python workflow
│   ├── main.py             # main entry point (orchestrates the workflow)
│   ├── get_serial_pyats.py # get device serial via pyATS
│   ├── template_select.py  # selects proper Jinja2 template
│   ├── render.py           # renders configuration using Jinja2 + YAML/NetBox data
│   ├── push.py             # pushes rendered config using Nornir/Netmiko + basic verification
│   ├── test_netbox_api.py  # NetBox API test helper
│   ├── test_nornir_inventory.py # Nornir inventory test helper
│   └── test_render.py      # rendering test helper
└── templates/
    └── base_router.j2      # base Jinja2 config template

---

## Workflow Summary

1. **Discover / identify device** (e.g., read serial with pyATS)
2. **Pull data from NetBox** (device/site/role/custom fields)
3. **Select template** based on `datas/template_map.yaml`
4. **Render config** using Jinja2 (`templates/*.j2`) + `datas/common.yaml` + NetBox data
5. **Push config** to the device using Nornir/Netmiko (`src/push.py`)
6. **Verify** with a few “show” commands (hostname, BGP section, and common lines)

---

## Push & Verify (Example)

`src/push.py` cleans the rendered config and pushes it, then verifies:
- hostname line
- BGP section
- common items (domain-name, name-server, ntp, logging, snmp)

---

## Requirements

```bash
pip install jinja2 pyyaml requests nornir nornir_netmiko pyats genie
