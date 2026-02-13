from fastapi import FastAPI, Request
import requests
import urllib3

app = FastAPI()

# ========== SETTINGS ==========
DIRECTOR_IP = "192.168.198.161"
USERNAME = "versa"
PASSWORD = "***"
CLIENT_ID = "70449E85B7FD23110D030F5AF51D0EB1"
CLIENT_SECRET = "***"

VERIFY_SSL = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ==============================


def get_token():
    url = f"https://{DIRECTOR_IP}:9183/auth/token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD,
        "grant_type": "password"
    }

    r = requests.post(url, json=payload, verify=VERIFY_SSL)
    r.raise_for_status()
    return r.json()["access_token"]


@app.post("/netbox-webhook")
async def receive_webhook(request: Request):

    payload = await request.json()

    event = payload.get("event")
    data = payload.get("data", {})

    manufacturer = (data.get("device_type") or {}).get("manufacturer", {}).get("name")

   
    if event != "created" or manufacturer != "Versa Networks":
        return {"status": "ignored"}

    print("Triggering Versa onboarding...")

    name = data.get("name")
    serial = data.get("serial") or ""
    site_id = (data.get("custom_fields") or {}).get("versa_site_id")
    device_group = (data.get("custom_fields") or {}).get("versa_device_group")

    token = get_token()

    versa_payload = {
        "versanms.sdwan-device-workflow": {
            "deviceName": name,
            "siteId": str(site_id),
            "orgName": "Newyorker",   
            "serialNumber": serial,
            "deviceGroup": device_group,
            "locationInfo": {
                "country": "DE",
                "latitude": "52.52",
                "longitude": "13.40"
            }
        }
    }

    url = f"https://{DIRECTOR_IP}:9183/vnms/sdwan/workflow/devices/device"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    r = requests.post(url, headers=headers, json=versa_payload, verify=VERIFY_SSL)

    print("Versa Status:", r.status_code)
    print("Versa Response:", r.text)

    return {"status": "processed"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
