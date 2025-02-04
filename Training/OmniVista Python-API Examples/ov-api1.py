########  Example of Alcatel-Lucent Enterprise OV API , using /api
########  Version 1.0
########  Author: Kaveh Majidi , SE Team
######## Forked from ov-api example from Jorge Arasanz  @ ALE
######## An Example to show how to connect to OV and pull all VLANs in OV

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
print("An Example to show how to connect to OV and pull all VLANs in OV")

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
    # Get all available VLANs from OV
    api_domain="/vlanservice/vlans/view"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    #print(api_response_json)
    response_code=api_response_json['statusCode']
    if response_code != 200:
            print("")
            print("Error in getting requested data, please check your query. Response Code: " + response_code)
            print("")
    else:
        for vlan in api_response_json['response']['data']:
            print ("VLan : " + str(vlan['number']) + " Description  -->  " + vlan['description'] )
        print("--------------------------------------------------------------------------------")

# Logout of Omnivista
api_domain="/logout"
api_request=requests.Request('GET', api_url + api_domain, headers=headers)
api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
api_response_json=api_response.json()
