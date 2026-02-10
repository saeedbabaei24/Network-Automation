# ZTP with pyATS, YAML, and Jinja2

This folder contains a **Zero Touch Provisioning (ZTP)** proof of concept using:

- pyATS / Unicon
- YAML as source of truth
- Jinja2 for configuration rendering

## Workflow
1. Connect to device using default credentials
2. Read device serial number
3. Lookup device data from YAML
4. Render configuration using Jinja2
5. Push configuration to device

## Files
- `testbed.yaml` – minimal testbed definition
- `common.yaml` – shared configuration
- `devices_data.yaml` – per-device data (keyed by serial)
- `onboard_render_push.py` – main ZTP script
- `templates/` – Jinja2 templates

## Usage
```bash
python onboard_render_push.py

┌──────────────┐
│   Start      │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Load testbed.yaml    │
│ Load common.yaml     │
│ Load devices_data    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Ask user for IP      │
│ (runtime input)      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Inject IP into       │
│ testbed device       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Connect via SSH      │
│ (learn_hostname)     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Get Serial Number    │
│ show version         │
└──────┬───────────────┘
       │
       ▼
┌────────────────────────────┐
│ Serial in devices_data ?   │
└──────┬───────────────┬─────┘
       │ YES            │ NO
       ▼                ▼
┌──────────────┐   ┌──────────────┐
│ Render Jinja │   │   ERROR      │
│ Config       │   │   Stop       │
└──────┬───────┘   └──────────────┘
       │
       ▼
┌──────────────────────┐
│ Push Config          │
│ write memory         │
└──────┬───────────────┘
       │
       ▼
┌──────────────┐
│ Disconnect   │
└──────┬───────┘
       ▼
┌──────────────┐
│     End      │
└──────────────┘
