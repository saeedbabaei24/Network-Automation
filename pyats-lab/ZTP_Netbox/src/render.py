import yaml
from jinja2 import Environment, FileSystemLoader


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_config(nr, device_name: str, debug: bool = False) -> tuple[str, str]:
    """
    Render config for a device using:
      - NetBox config_context from Nornir inventory
      - common YAML (datas/common.yaml)
      - template_map (datas/template_map.yaml)

    Returns:
      (template_path, rendered_config)
    """
    if device_name not in nr.inventory.hosts:
        raise ValueError(f"Device '{device_name}' not found in Nornir inventory.")

    h = nr.inventory.hosts[device_name]

    cc = h.data.get("config_context") or {}
    device_type = h.data.get("device_type") or {}
    dt_slug = (device_type.get("slug") or "").strip()

    template_map = load_yaml("datas/template_map.yaml")
    template_path = (
        (template_map.get("device_type_slug_map") or {}).get(dt_slug)
        or template_map.get("default")
        or "templates/base_router.j2"
    )

    common_cfg = load_yaml("datas/common.yaml")  # expects {"common": {...}}

    context = {
        "device": {"name": h.name, "serial": h.data.get("serial")},
        **common_cfg,  # provides "common"
        **cc,          # provides "router", "dns", "ntp", ...
    }

    if debug:
        print("DEBUG dt_slug:", dt_slug)
        print("DEBUG template_path:", template_path)
        print("DEBUG common_cfg keys:", list(common_cfg.keys()))
        print("DEBUG netbox cc keys:", list(cc.keys()))
        print("DEBUG context keys:", list(context.keys()))

    env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
    tpl = env.get_template(template_path)
    rendered = tpl.render(**context)

    return template_path, rendered
