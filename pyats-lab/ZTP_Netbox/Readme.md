# ZTP NetBox Automation (pyATS + Nornir + Jinja2)

This project is a **ZTP-style automation workflow** that uses **NetBox as the source of truth**, renders device configuration using **Jinja2**, and pushes the final config to network devices using **Nornir/Netmiko**.


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
