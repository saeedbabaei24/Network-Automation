# Nornir + NAPALM Automation Examples
Install dependencies:
pip install nornir nornir-napalm nornir-utils napalm


All scripts use:
config.yaml

# 1. Replace_config.py 
Loads configuration from a file and applies it to devices.

What it does:
- Reads inventory from config.yaml
- Uses napalm_configure
- Loads configuration from running.txt
- Applies it as a merge (replace=False)
- Commits changes (dry_run=False)

# 2. Backup_router.py 
Creates a backup of the running configuration.

What it does:
- Uses napalm_get with getter 'config'
- Extracts the running configuration
- Saves it to running.txt

# 3. Config_router.py 
Pushes inline configuration directly from Python.

What it does:
- Uses napalm_configure
- Sends configuration as a string
- Applies it to devices in the inventory


# 4. Napalm_configure.py 
Custom implementation of the napalm_configure task.

What it does internally:
1. Loads candidate configuration (merge or replace)
2. Compares candidate with running config
3. Generates configuration diff
4. Commits changes if differences exist
5. Discards changes if no diff or dry run

# 5. Nornir NAPALM get interfaces.py

Purpose:  
Retrieves structured interface IP information.

What it does:
- Uses napalm_get
- Calls getter 'interfaces_ip'
- Returns structured interface data

# 6. Nornir.py

Purpose:  
Runs CLI commands across multiple devices.

What it does:
- Uses napalm_cli
- Executes "show ip int brief"
- Prints results


# Automation Workflow 

Inventory → Nornir → NAPALM → Device  
                     ↓  
                 Compare Config  
                     ↓  
               Commit / Discard   
Network Automation Lab
