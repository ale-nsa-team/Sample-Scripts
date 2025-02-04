########  Example of Alcatel-Lucent Enterprise AOS API , Domain = CLI ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using CLI API and pull VLAN table
import requests
import yaml
import urllib3

######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######  Loading the list of switches and their IP/User/Password from yaml file #####
with open('switch_list.yaml') as file:
    switch_list=yaml.load(file)

##### Starting a loop to perform the following on each switch  #####
print("##########        Operation Started.........  #############")
print("Example of connecting to switch using CLI API and pull VLAN table")
for switch in switch_list:
    ip=switch_list[switch]['ip']
    username=switch_list[switch]['username']
    password=switch_list[switch]['password']

##### Creating a Switch Session for switch and check the response  #####
    switch_session=requests.Session()
    headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
    login_response=switch_session.get('https://' + ip + '/auth/?&username=' + username + '&password=' + password, verify=False, headers=headers)
    login_response_json=login_response.json()
    login_status_code=login_response_json['result']['diag']

##### if switch Authentication is successful continue ,else return error  #####
    if login_status_code != 200:
         print("")
         print("Error ! Login/Connection failed for " + switch + " Please check your credentials or verify connection")
         print("")
    else:
##### Pull the vlan table from switch  #####
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        vlan_result=switch_session.get('https://' + ip + '/cli/aos?&cmd=show+vlan', headers=headers)
        vlan_result_json=vlan_result.json()
        print("")
        print("_____________VLAN Table  For "  +  switch  + " ________________________")
        print(vlan_result_json['result']['output'])
        print("____________________________________________________________________")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
