########  Example of Alcatel-Lucent Enterprise AOS API , Domain = MIB , Show Linkaggs
########  Version 1.0
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using MIB API and pull Linkagg information

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
print("Example of connecting to switch using MIB API and pull Linkagg information")
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
        #####  Read Linkagg Data######
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        linkagg_read_result=switch_session.get('https://' + ip + '/mib/alclnkaggAggTable?&mibObject0=alclnkaggAggNumber&mibObject1=alclnkaggAggLacpType&mibObject2=alclnkaggAggAdminState', headers=headers)
        linkagg_read_result_json=linkagg_read_result.json()
        print(linkagg_read_result_json)
        print("--------------------------------------------------------------------------------")
        print("")
        print("Switch : "  + switch)
        for x in linkagg_read_result_json['result']['data']['rows']:
             print("")
             print ("Linkagg ID : "  + linkagg_read_result_json['result']['data']['rows'][x]['alclnkaggAggNumber'] + " Type  -->  " + linkagg_read_result_json['result']['data']['rows'][x]['alclnkaggAggLacpType'])
        print("--------------------------------------------------------------------------------")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")

'''' Available MIB objects
alclnkaggAggTable
    alclnkAggSize
    alclnkaggAggNumber
    alclnkaggAggDescr
    alclnkaggAggName
    alclnkaggAggLacpType
    alclnkaggAggAdminState
    alclnkaggAggOperState
    alclnkaggAggNbrSelectedPorts
    alclnkaggAggNbrAttachedPorts
    alclnkaggPrimaryPortIndex
    alclnkaggAggMACAddress
    alclnkaggAggActorSystemPriority
    alclnkaggAggActorSystemID
    alclnkaggAggPartnerAdminKey
    alclnkaggAggActorAdminKey
    alclnkaggAggActorOperKey
    alclnkAggLocalRangeOperMin
    alclnkAggLocalRangeOperMax
    alclnkAggLocalRangeConfiguredMin
    alclnkAggLocalRangeConfiguredMax
    alclnkAggPeerRangeOperMin
    alclnkAggPeerRangeOperMax
    alclnkaggAggPartnerSystemID
    alclnkaggAggPartnerSystemPriority
    alclnkaggAggPartnerOperKey
'''
