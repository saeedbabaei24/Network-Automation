# Versa SD-WAN Onboarding Automation  
NetBox → FastAPI → Versa Director

This module automates Versa SD-WAN device onboarding using NetBox webhooks and the Versa Director API.

When a new device is created in NetBox:
- If manufacturer == "Versa Networks"
- FastAPI receives the webhook from Netbox
- Retrieves OAuth token from Director
- Triggers the SD-WAN device workflow automatically

---

## Project Structure

onboard_versa/
├── versa_push.py          # Main webhook service (production)
├── onboard.py             # Manual onboarding script (JSON-based)
├── webhook_receiver.py    # Debug webhook listener
└── berlin01.json          # Sample device input (for manual test)

---

## Requirements
pip install fastapi uvicorn requests

---

## Run Webhook Service

python versa_push.py

or

uvicorn versa_push:app --host 0.0.0.0 --port 8000

Webhook endpoint:
POST http://<server-ip>:8000/netbox-webhook

---

## NetBox Webhook Setup

Content Type: Device  
Event: Created  
Method: POST  
URL: http://<server-ip>:8000/netbox-webhook  
Content Type: application/json  

Custom Fields required in NetBox:
- versa_site_id
- versa_device_group

---

## Versa Director API

Token:
POST https://<DIRECTOR_IP>:9183/auth/token

Workflow:
POST /vnms/sdwan/workflow/devices/device

