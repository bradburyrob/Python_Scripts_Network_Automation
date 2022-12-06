import requests
import json
hostnames = open('ADD_TO_CPI.txt').read().split()
USERNAME = ""
PASSWORD = input("Enter Password: ")


for hostname in hostnames:
    print("this is the current router being Added: " + hostname)
    url = "https://" + USERNAME + ":" + PASSWORD + "@140.194.x.x/webacs/api/v2/op/devices/bulkImport"
    payload = {
      "devicesImport" : {
        "devices" : {
          "device" : {
            "credentialProfileName" : "RTR-SW-TACACS",
            "ipAddress" : hostname

          }
        }
      }
    }

    headers = {"Content-Type": "application/json"}


    response = requests.put(url,headers=headers, data=json.dumps(payload), verify=False)
    print(response.text)




