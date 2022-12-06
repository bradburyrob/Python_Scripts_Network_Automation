import requests
import json
hostnames = open('\\DELETE_FROM_CPI.txt').read().split()
USERNAME = ""
PASSWORD = input("Enter Password: ")


for hostname in hostnames:
    print("this is the current router being deleted: " + hostname)
    url = "https://" + USERNAME + ":" + PASSWORD + "@140.194./webacs/api/v2/op//devices/deleteDevices"
    payload = {
    "deviceDeleteCandidates" : {
    "ipAddresses" : {
    "ipAddress" : hostname
    }
    }
    }

    headers = {"Content-Type": "application/json"}


    response = requests.put(url,headers=headers, data=json.dumps(payload), verify=False)
    print(response.text)




