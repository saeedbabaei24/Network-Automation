import requests

url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces"

payload = "{\n  \"ietf-interfaces:interface\": {\n    \"name\": \"Loopback33\",\n    \"type\": \"softwareLoopback\",\n    \"enabled\": true,\n    \"ietf-ip:ipv4\": {\n      \"address\": [\n        {\n          \"ip\": \"33.33.33.33\",\n          \"netmask\": \"255.255.255.0\"\n        }\n      ]\n    }\n  }\n}\n"
headers = {
    'Content-Type': "application/yang-data+json",
    'Accept': "application/yang-data+json",
    'Authorization': "Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU=",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "7e140768-e78e-40b0-aa4f-29216376fd40,041e05bd-d4da-4d31-8cef-253b78d6ff61",
    'Host': "10.10.20.48",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "263",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)