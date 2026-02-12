def choose_template(template_map: dict, platform: str, device_type: str) -> str:
    overrides = template_map.get("device_type_overrides") or {}
    if device_type in overrides:
        return overrides[device_type]

    pmap = template_map.get("platform_map") or {}
    if platform in pmap:
        return pmap[platform]

    raise RuntimeError(f"No template found for platform='{platform}', device_type='{device_type}'")
