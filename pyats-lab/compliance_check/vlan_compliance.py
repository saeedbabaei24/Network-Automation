#!/usr/bin/env python3

import re
from collections import defaultdict
from pyats.topology import loader
from genie.metaparser.util.exceptions import SchemaEmptyParserError


def extract_vlans_from_parsed(parsed):
    vlans = {}
    for vlan_id, data in (parsed or {}).get("vlans", {}).items():
        try:
            vid = int(vlan_id)
        except Exception:
            continue
        vlans[vid] = (data.get("name") or "").strip()
    return vlans


def extract_vlans_from_text(output: str):
    """
    Fallback parser for 'show vlan brief' output.
    Returns: { vlan_id(int): vlan_name(str) }
    """
    vlans = {}
    # Example line: "10   USERS   active   Gi1/0/1,Gi1/0/2"
    pattern = re.compile(r"^\s*(\d+)\s+(\S+)\s+(active|act/unsup|suspend)\b", re.IGNORECASE)
    for line in output.splitlines():
        m = pattern.search(line)
        if m:
            vid = int(m.group(1))
            name = m.group(2).strip()
            vlans[vid] = name
    return vlans


def get_vlans(device, debug=False):
    device.connect(log_stdout=False)
    try:
        raw = device.execute("show vlan brief")

        if debug:
            head = "\n".join(raw.splitlines()[:25])
            print(f"[DEBUG] {device.name} show vlan brief (first lines):\n{head}\n")

        vlans = {}

        try:
            parsed = device.parse("show vlan brief")
            vlans = extract_vlans_from_parsed(parsed)
        except SchemaEmptyParserError:
            vlans = {}

        if not vlans:
            vlans = extract_vlans_from_text(raw)
            if debug:
                print(f"[DEBUG] {device.name} parsed VLANs empty, fallback VLAN count = {len(vlans)}")
        else:
            if debug:
                print(f"[DEBUG] {device.name} genie parsed VLAN count = {len(vlans)}")

        return vlans
    finally:
        device.disconnect()


def compare(baseline_vlans, device_vlans):
    b_ids = set(baseline_vlans.keys())
    d_ids = set(device_vlans.keys())

    missing = sorted(b_ids - d_ids)
    extra = sorted(d_ids - b_ids)

    mismatched_names = []
    for vid in sorted(b_ids & d_ids):
        if (baseline_vlans.get(vid) or "") != (device_vlans.get(vid) or ""):
            mismatched_names.append((vid, baseline_vlans.get(vid), device_vlans.get(vid)))

    return missing, extra, mismatched_names


def main():
    tb = loader.load("devices.yaml")

    devices_by_site = defaultdict(list)
    baseline_by_site = {}

    for dev in tb.devices.values():
        site = dev.custom.get("site")
        if not site:
            continue
        devices_by_site[site].append(dev)
        if dev.custom.get("is_site_baseline") is True:
            baseline_by_site[site] = dev

    debug = True

    for site, devices in devices_by_site.items():
        baseline = baseline_by_site.get(site)
        if not baseline:
            print(f"\n[WARN] No baseline for site '{site}'")
            continue

        print(f"\n===== SITE: {site} | BASELINE: {baseline.name} =====")
        baseline_vlans = get_vlans(baseline, debug=debug)

        if not baseline_vlans:
            print(f"[ERROR] Baseline VLAN list is empty on {baseline.name}.")
            print("[ERROR] This usually means the command returned unexpected output or VLANs are not configured.")
            continue

        for dev in devices:
            if dev.name == baseline.name:
                continue

            dev_vlans = get_vlans(dev, debug=debug)
            missing, extra, mismatched = compare(baseline_vlans, dev_vlans)

            print(f"\n--- {dev.name} vs baseline ---")
            if not missing and not extra and not mismatched:
                print("OK - no differences found")
                continue

            if missing:
                print("Missing VLANs:")
                for vid in missing:
                    print(f"  - {vid} ({baseline_vlans.get(vid)})")

            if extra:
                print("Extra VLANs:")
                for vid in extra:
                    print(f"  + {vid} ({dev_vlans.get(vid)})")

            if mismatched:
                print("VLAN name mismatches:")
                for vid, bname, dname in mismatched:
                    print(f"  * {vid}: baseline='{bname}' device='{dname}'")


if __name__ == "__main__":
    main()
