import requests
import json
import re
requests.packages.urllib3.disable_warnings() 

OV_IP = "192.168.2.194"
OV_USERNAME = "admin"
OV_PASSWORD = "switch"
SEARCHED_MAC = "14:7d:da:74:d1:7c"

switch_session = requests.Session()
headers = {
  'Content-Type': 'application/json'
}

#AUTH
url = f"https://{OV_IP}/rest-api/login"
payload = json.dumps({
  "userName": OV_USERNAME,
  "password": OV_PASSWORD
})
auth_response = switch_session.post(url, headers=headers, data=payload, verify=False)

#Formating the MAC address
mac = re.sub(r'[^a-fA-F0-9]', '', SEARCHED_MAC).lower()
formatted_mac = f"{mac[:6]}:{mac[6:]}"

#GET
url = f"https://{OV_IP}/api/locator/devices?mac={formatted_mac}&mode=historical"
get_mac_location = switch_session.get(url, headers=headers, verify=False)

#Parse the output to extract the second dictionary
get_mac_location_str = get_mac_location.text
get_mac_location_str = get_mac_location_str[get_mac_location_str.find("}{")+1:]
get_mac_location_str = get_mac_location_str[:get_mac_location_str.find("}{")+1]

#Output to JSON
get_mac_location_output = json.loads(get_mac_location_str)
get_mac_location_info = get_mac_location_output["response"]["ovResponseObject"][0]

#Extract the values
device_ip = get_mac_location_info["switchIpAddress"]
device_name = get_mac_location_info["switchSysName"]
port_id = get_mac_location_info["slotPortStr"]
port_status = get_mac_location_info["portStatusStr"]
port_description = get_mac_location_info["portAlias"]
client_ip = get_mac_location_info["endstationName"]


print(f"Information about the location of the MAC address '{SEARCHED_MAC}':\nDevice Name: {device_name}\nDevice IP Address: {device_ip}\nPort ID: {port_id}\nPort Status: {port_status}\nPort Description: {port_description}\nClient IP Address: {client_ip}")
