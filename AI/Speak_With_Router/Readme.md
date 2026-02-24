# AI-Powered Read-Only Network Assistant (Telegram + Cisco IOS)

## Overview

This project implements an AI-driven Network Assistant that connects to a Cisco IOS router via SSH and analyzes the device using GPT-4o-mini.

The assistant:

- Receives questions from Telegram
- Decides which diagnostic commands are required
- Executes read-only CLI commands on the router
- Analyzes the output using AI
- Returns structured findings and recommendations

The assistant is strictly **read-only**.  
It cannot enter configuration mode or modify the device.

---

## Architecture

User (Telegram)
→ GPT (decides required command)
→ Tool Call
→ SSH to Router (Netmiko)
→ CLI Output
→ GPT Analysis
→ Telegram Response
---

## Allowed Command Patterns

The assistant may generate only commands matching:

- `show ip interface brief`
- `show interface <name>`
- `show ip route`
- `show running-config | include <keyword>`
- `show running-config | section <section>`
- `show aaa`
- `show tacacs`
- `show logging`
- `ping <ip>`
- `traceroute <ip>`

All commands are validated before execution.

---

## Features

- AI-driven troubleshooting
- Automatic command selection
- Cisco IOS-aware reasoning
- Structured output:
  - Findings
  - Conclusion
  - Recommendations
- Telegram bot interface
- Loop prevention and execution limits
- Invalid CLI detection handling

---

## Example Questions

- Is BGP healthy?
- Why is GigabitEthernet0/1 down?
- Any routing issues?
- Can the router reach 8.8.8.8?

---
Install dependencies

```bash
pip install python-telegram-bot openai netmiko
```

Set environment variables

```bash
export TELEGRAM_BOT_TOKEN="your_telegram_token"
export OPENAI_API_KEY="your_openai_api_key"
```
