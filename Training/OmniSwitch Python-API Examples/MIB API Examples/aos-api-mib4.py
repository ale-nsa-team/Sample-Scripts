########  Example of Alcatel-Lucent Enterprise AOS API , Domain = MIB , Craete a VLAN and Verify##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using MIB API pull IP interface information
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
print(" Example of connecting to switch using MIB API pull IP interface information")
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
        #####  Read  Interface Data######
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        interface_read_result=switch_session.get('https://' + ip + '/mib/alaIpInterfaceTable?&mibObject0=alaIpInterfaceName&mibObject1=alaIpInterfaceAddress', headers=headers)
        interface_read_result_json=interface_read_result.json()
        #print(interface_read_result_json)
        print("--------------------------------------------------------------------------------")
        print("")
        print("Switch : "  + switch)
        #print(vlan_read_result_json['result']['data']['rows'])
        for x in interface_read_result_json['result']['data']['rows']:
             print("")
             print ("IP interface : " + x + " Name  -->  " + interface_read_result_json['result']['data']['rows'][x]['alaIpInterfaceName'] + " IP  -->  " + interface_read_result_json['result']['data']['rows'][x]['alaIpInterfaceAddress'])
        print("--------------------------------------------------------------------------------")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
