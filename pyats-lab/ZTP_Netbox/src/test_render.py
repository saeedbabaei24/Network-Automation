import yaml
from nornir import InitNornir
from jinja2 import Environment, FileSystemLoader
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

nr = InitNornir(config_file="config/nornir.yaml")
h = nr.inventory.hosts["R1"]

cc = h.data.get("config_context") or {}
device_type = h.data.get("device_type") or {}
dt_slug = (device_type.get("slug") or "").strip()

template_map = load_yaml("datas/template_map.yaml")
template_path = (
    (template_map.get("device_type_slug_map") or {}).get(dt_slug)
    or template_map.get("default")
    or "templates/base_router.j2"
)

common_cfg = load_yaml("datas/common.yaml")  # MUST contain {"common": {...}}


print("DEBUG dt_slug:", dt_slug)
print("DEBUG template_path:", template_path)
print("DEBUG common_cfg keys:", list(common_cfg.keys()))
print("DEBUG netbox cc keys:", list(cc.keys()))

context = {
    "device": {"name": h.name, "serial": h.data.get("serial")},
    **common_cfg,  # provides "common"
    **cc           # provides "router", "dns", "ntp", ...
}
print("DEBUG context keys:", list(context.keys()))

env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
tpl = env.get_template(template_path)

rendered = tpl.render(**context)

print("\n---- RENDERED CONFIG ----\n")
print(rendered)
