# Jinja2 Basics – Configuration Rendering Example

This example demonstrates how to use **Jinja2** to generate network device configurations from structured Python data.

The script renders a template (`switch_interfaces.j2`) using interface data and writes the final configuration into an output file.


## What This Example Does

- Defines structured interface data in Python
- Loads a Jinja2 template from the `templates/` directory
- Renders the configuration
- Saves the generated config to `output/SW-BR-01.cfg`

---

## Requirements

Install Jinja2:

```bash
pip install jinja2
```

---



### Python Data Structure

The script defines:

- Hostname
- List of interfaces
- Interface mode (access/trunk)
- VLAN (if applicable)

###  Jinja2 Environment

```python
env = Environment(
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True
)
```

- `trim_blocks=True` → removes extra blank lines  
- `lstrip_blocks=True` → cleans indentation  

###  Rendering

```python
template = env.get_template("switch_interfaces.j2")
rendered = template.render(data)
```

###  Output

The rendered configuration is written to:

```
output/SW-BR-01.cfg
```

---

## Run the Script

```bash
python render_config.py
```

Output:

```
Configuration generated successfully.
```
