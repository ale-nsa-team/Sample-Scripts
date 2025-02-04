########  Example of Alcatel-Lucent Enterprise OV API , using /api  and /rest-api
########  Version 1.0
########  Author: Kaveh Majidi , SE Team
######## Credit: Brian Witt  @ ALE
######## An Example to show how to connect to OV and pull all Device IDs -using Cookie

import requests
import yaml
import urllib3
######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######  Loading the OV IP/User/Password from yaml file #####
with open('ov_list.yaml') as file:
    ov_list=yaml.load(file)
for ov in ov_list:
    ip=ov_list[ov]['ip']
    username=ov_list[ov]['username']
    password=ov_list[ov]['password']

print("##########        Operation Started.........  #############")
print("An Example to show how to connect to OV and pull all Devices IDs -using Cookie")
print("")
# Defining all API requirements
ov_session=requests.Session()
headers = {"Content-Type":"application/json"}
api_url="https://" + ip + "/api"
api_domain="/login"
credentials={}
credentials['userName']=username
credentials['password']=password

# Make a login API call to OV
api_request=requests.Request('POST', api_url + api_domain, headers=headers, json=credentials)
api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
api_response_json=api_response.json()
login_response=api_response_json['message']

# if login is successful then continue
if login_response != "login.success":
    print("")
    print("Error ! Login/Connection failed for OV @ " + ip + " Please check your credentials or verify connection")
    print("")
else:
    # Get all devices from OV
    api_url="https://" + ip + "/rest-api"
    api_domain="/devices"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    response_status=api_response_json['status']
    #print(response_status)
    #print(api_response_json)
    if response_status != "SUCCESS":
            print("")
            print("Error in getting requested data, please check your query. Response Code: " + response_code)
            print("")
    else:
        for device in api_response_json['response']:
            print ("Device ID -->" + device['deviceId'] + " IP -->  " + device['ipAddress']  + " MAC -->  " + device['macAddress'] )
        print("--------------------------------------------------------------------------------")

# Logout of Omnivista
api_domain="/logout"
api_request=requests.Request('GET', api_url + api_domain, headers=headers)
api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
api_response_json=api_response.json()
