import requests
import json
import datetime

#VARIABLES
DEVICES = ["POD2","POD1"]
DESIRED_VERSION = "8.9.221.R03"
OMNIVISTA_HOTNAME = "192.168.121.66"
OMNIVISTA_USERNAME = "admin"
OMNIVISTA_PASSWORD = "switch"

#INITIATE SESSION
switch_session = requests.Session()
headers = {
  'Content-Type': 'application/json'
}
 
#AUTH
url = "https://{OMNIVISTA_HOTNAME}/rest-api/login"
payload = json.dumps({
  "userName": OMNIVISTA_USERNAME,
  "password": OMNIVISTA_PASSWORD
})
auth_response = switch_session.post(url, headers=headers, data=payload, verify=False)
#print(auth_response)

#GET DEVICES
url = f"https://{OMNIVISTA_HOTNAME}/api/devices?fieldSetName=discovery"
get_devices = switch_session.get(url, headers=headers, verify=False)
#CREATE A LIST WITH THE DEVICE NAME AND ID
devices_ids = {}
for device in get_devices.json()["response"]:
    if device["friendlyName"] in DEVICES:
        devices_ids[device["instanceid"]] = device["friendlyName"]

#CREATE THE OPERATION ID FOR THE WRITE MEMORY
url = f"https://{OMNIVISTA_HOTNAME}/api/discoverylite/gettriggerid"
get_operation_id = switch_session.get(url, headers=headers, verify=False)
operation_id = get_operation_id.json()["response"]["data"]
#print(operation_id)

#WRITE MEMORY
url = f"https://{OMNIVISTA_HOTNAME}/api/discoverylite/configdeviceoperations/triggeroperation"
payload = json.dumps({
    "TriggerConfigDeviceOperationsRequestObject": {
        "triggerId": operation_id,
        "ipAddresses": [],
        "opCode": 101,
        "loadImageDir": "/flash/working",
        "delay": 0,
        "sessionId": "null",
        "user": "null",
        "deviceMap": devices_ids
    }
})
#print(payload)
write_memory = switch_session.post(url, headers=headers, data=payload, verify=False)
#print(write_memory)

#CREATE THE OPERATION ID FOR THE COPY RUNNING TO CERTIFIED
url = f"https://{OMNIVISTA_HOTNAME}/api/discoverylite/gettriggerid"
get_operation_id = switch_session.get(url, headers=headers, verify=False)
operation_id = get_operation_id.json()["response"]["data"]
#print(operation_id)

#COPY RUNNING CERTIFIED
url = f"https://{OMNIVISTA_HOTNAME}/api/discoverylite/configdeviceoperations/triggeroperation"
payload = json.dumps({
    "TriggerConfigDeviceOperationsRequestObject": {
        "triggerId": operation_id,
        "ipAddresses": [],
        "opCode": 2,
        "loadImageDir": "/flash/working",
        "delay": 0,
        "sessionId": "null",
        "user": "null",
        "deviceMap": devices_ids
    }
})
#print(payload)
copy_running_working = switch_session.post(url, headers=headers, data=payload, verify=False)
print(copy_running_working)

#GET THE AVAILABLE IMAGES ON OMNIVISTA
url = f"https://{OMNIVISTA_HOTNAME}/api/resourcemanager/schedule/swupgrade/supportedfirmwares"
payload = json.dumps({
    "GetSupportedFirmwaresRequest": {
        "deviceIds": list(devices_ids.keys()),
        "apGroupNames": []
    }
})
#print(payload)
available_images = switch_session.post(url, headers=headers, data=payload, verify=False)


#SCHEDULE UPGRADE
url = f"https://{OMNIVISTA_HOTNAME}/api/resourcemanager/schedule/swupgrade"
#MAP THE IMAGE
upgradeDevices = []
for id in devices_ids:
    for avaible_image in available_images.json()["response"]["data"]:
        if id in list(avaible_image["supportedFirmwares"].keys()):
            print(avaible_image["supportedFirmwares"][id])
            for avaible_image_device in avaible_image["supportedFirmwares"][id]:
                if avaible_image_device["firmwareInfo"]["version"] == DESIRED_VERSION:
                    upgradeDevices.append({
    "deviceId": id,
    "friendlyName": devices_ids[id],
    "desiredSwVer": DESIRED_VERSION,
    "installAction": "UPGRADE_IMAGE_FILES",
    "installDirectory": "/flash/working",
    "desiredSwKey": avaible_image_device["firmwareInfo"]["fwKey"]
})
                    
payload = json.dumps({
    "CreateSwUpgradeSchedulerRequest": {
        "name": "AUTOMATED_SCHEDULE_UPGRADE_{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")),
        "cronExpression": "",
        "duration": 0,
        "timeZone": "null",
        "upgradeDevices": upgradeDevices,
        "startDate": 0,
        "endDate": "null",
        "scheduleType": "NOW",
        "devicePicked": "true",
        "recurrenceTimes": ""
    }
})
#print("\n\n\n\n\n")
#print(payload)
url = f"https://{OMNIVISTA_HOTNAME}/api/resourcemanager/schedule/swupgrade"
schedule_upragde = switch_session.post(url, headers=headers, data=payload, verify=False)
#print(schedule_upragde)

if schedule_upragde.status_code == 200:
    print(f"The scheduled upgrade is complete. You can follow the progress here: https://{OMNIVISTA_HOTNAME}/#/discovery/scheduled-upgrade")
