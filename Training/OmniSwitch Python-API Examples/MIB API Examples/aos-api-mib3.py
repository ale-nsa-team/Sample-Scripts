########  Example of Alcatel-Lucent Enterprise AOS API , Domain = MIB , Craete a VLAN and Verify##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using MIB API and create a VLAN with Descriptions
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
print("Example of connecting to switch using MIB API and create a VLAN with Descriptions")
for switch in switch_list:
    ip=switch_list[switch]['ip']
    username=switch_list[switch]['username']
    password=switch_list[switch]['password']
    name=switch_list[switch]['name']

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
##### Push the data to switch  #####
        #####  Create a New VLAN ######
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        parameters={}
        parameters['mibObject1']='vlanNumber:7'
        parameters['mibObject0']='vlanDescription:voice-vlan'
        vlan_create_result=switch_session.post('https://' + ip + '/mib/vlanTable?', data=parameters, headers=headers)

        #####  Read  VLAN Data######
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        parameters = {'mibObject0':'vlanDescription'}
        vlan_read_result=switch_session.get('https://' + ip + '/mib/vlanTable?',params=parameters, headers=headers)
        vlan_read_result_json=vlan_read_result.json()
        print("--------------------------------------------------------------------------------")
        print("")
        print("Switch : "  + switch)
        print(vlan_read_result_json['result']['data']['rows'])
        for x in vlan_read_result_json['result']['data']['rows']:
            print("")
            print ("Vlan : " + x + " Description  -->  " + vlan_read_result_json['result']['data']['rows'][x]['vlanDescription'])
        print("--------------------------------------------------------------------------------")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
