import requests
import json
import time

#settings
DIRECTOR_IP = "192.168.198.161"
USERNAME = "versa"
PASSWORD = "Versa123!"
CLIENT_ID = "70449E85B7FD23110D030F5AF51D0EB1"
CLIENT_SECRET = "****"

VERIFY_SSL = False

#get token
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

    print("TOKEN status:", r.status_code)
    print("TOKEN response:", r.text)

    r.raise_for_status()
    data = r.json()

    if "access_token" not in data:
        raise RuntimeError(f"Token response missing access_token. Keys: {list(data.keys())}")

    return data["access_token"]



# read the jason file
with open("berlin01.json") as f:
    device = json.load(f)

# get token
token = get_token()

#make the payload
payload = {
    "versanms.sdwan-device-workflow": {
        "deviceName": device["deviceName"],
        "siteId": str(device["siteId"]),
        "orgName": device["orgName"],
        "serialNumber": device["serialNumber"],
        "deviceGroup": device["deviceGroup"],
        "locationInfo": {
            "country": device["country"],
            "latitude": str(device["latitude"]),
            "longitude": str(device["longitude"])
        }
    }
}

#send to director
url = f"https://{DIRECTOR_IP}:9183/vnms/sdwan/workflow/devices/device"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

r = requests.post(url, headers=headers, json=payload, verify=VERIFY_SSL)

print("Status Code:", r.status_code)
print("Response:", r.text)
