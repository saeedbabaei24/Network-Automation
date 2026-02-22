# Cisco 1921 – Jinja2 + YAML + Netmiko Config Push

This project generates Cisco IOS configuration from **Jinja2 templates** and **YAML data**, then pushes the config to **Cisco 1921** routers using **Netmiko**.


## How It Works

1. Loads router IPs from `Hosts.yaml`
2. Loads variables from `Router_Data.yaml`
   - `common:` shared config variables
   - `routers:` per-router config (keyed by IP)
3. Renders `Config_Template.j2` with Jinja2
4. Splits rendered output into CLI commands
5. Connects to each router via SSH and pushes the config with Netmiko
6. Saves configuration (`write memory` / `copy run start` depending on platform)

---

## Requirements

```bash
pip install jinja2 pyyaml netmiko
