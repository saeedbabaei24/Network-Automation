import requests

url = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"

headers = {
    'Accept': "application/yang-data+json",
    'Content-Type': "application/yang-data+json",
    'Authorization': "Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU=",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "bc52320f-8578-487b-a99f-ee0127cbf3ad,871af06e-ea88-4ec2-8dd0-caaea6562bbf",
    'Host': "10.10.20.48",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, headers=headers)

print(response.text)