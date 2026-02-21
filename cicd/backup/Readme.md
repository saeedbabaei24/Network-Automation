# CI/CD Network Config Backup (Nornir + Scrapli)

This folder contains a CI/CD job that automatically connects to network devices and backs up configurations using **Nornir + Scrapli**.  
It is designed to run in an Actions-compatible pipeline (GitHub Actions / Forgejo Actions) and commit the generated backups back into the repository.



## What the Workflow Does (backup.yaml)

This workflow runs on manual start(we can change it):

- `on: workflow_dispatch`

### Steps summary

1. **Checkout repository**
2. **Install Python + venv**
3. **Create virtual environment and install dependencies**
   - `nornir`, `nornir-utils`
   - `nornir-scrapli`, `scrapli`, `scrapli-community`
   - `pyyaml`
4. **Copy SSH legacy config**
   - Places `config/legacy.conf` into `/etc/ssh/ssh_config.d/legacy.conf`
5. **Sanity check for enable secret** (only prints True/False, not the secret)
6. **Run `backup.py`**
7. **Commit and push generated backups** (only if files changed under `./backup/`)

---

## Required Secrets

The pipeline expects these secrets to be configured in your CI platform:

- `DEVICE_USERNAME`
- `DEVICE_PASSWORD`
- `DEVICE_ENABLE_PASSWORD` 

They are injected as environment variables:

- `DEVICE_USERNAME`
- `DEVICE_PASSWORD`
- `DEVICE_ENABLE_PASSWORD`

---

## How Backups Are Stored

The workflow checks for changes under:

- `./backup/`

If any files in `./backup/` changed, it commits and pushes them automatically.

---
