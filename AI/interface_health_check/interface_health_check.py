#!/usr/bin/env python3
import os
import json
import logging
from pyats.topology import loader
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pyats-ai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY first (see steps below).")

client = OpenAI(api_key=OPENAI_API_KEY)

TESTBED_FILE = "testbed.yaml"
testbed = loader.load(TESTBED_FILE)


def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def summarize_int_brief(parsed):
    """
    Reduce the parsed output to only what the AI needs.
    Genie schema can vary a bit; we defensively extract fields.
    """
    rows = []

    # Common structure: parsed["interface"] -> dict of interfaces
    iface_dict = parsed.get("interface", {})
    for ifname, info in iface_dict.items():
        rows.append({
            "interface": ifname,
            "ip_address": info.get("ip_address"),
            "status": info.get("status"),
            "protocol": info.get("protocol"),
        })

    # If parser structure differs, fall back to raw object (last resort)
    if not rows:
        return {"raw": parsed}

    return {"interfaces": rows}

def analyze_with_ai(device_name, payload):
    prompt = f"""
You are a Cisco network troubleshooting assistant.
Analyze the following structured output from "show ip interface brief" for device {device_name}.
1) List any interfaces that look unhealthy (down/down, administratively down, protocol down, missing IP where expected).
2) Give likely causes and quick checks/commands.
3) Provide a short "overall health" summary.
Return the answer in clear bullet points.
Data:
{json.dumps(payload, ensure_ascii=False)}
""".strip()

    # Responses API (recommended)
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )
    return resp.output_text

for device_name, device in testbed.devices.items():
    log.info(f"Connecting to {device_name} ({device.connections.cli.ip}) ...")
    try:
        device.connect(
            log_stdout=False,
            init_exec_commands=[],
            init_config_commands=[],
        )
    except Exception as e:
        log.error(f"[{device_name}] connect failed: {e}")
        continue

    try:
        log.info(f"[{device_name}] parsing: show ip interface brief")
        parsed = device.parse("show ip interface brief")
        save_json(parsed, f"{device_name}_show_ip_int_brief_full.json")

        compact = summarize_int_brief(parsed)
        save_json(compact, f"{device_name}_show_ip_int_brief_compact.json")

        log.info(f"[{device_name}] sending to AI...")
        ai_text = analyze_with_ai(device_name, compact)
        print("\n" + "=" * 70)
        print(f"AI analysis for {device_name}\n")
        print(ai_text)
        print("=" * 70 + "\n")

    except Exception as e:
        log.error(f"[{device_name}] error: {e}")
    finally:
        device.disconnect()

log.info("Done.")
