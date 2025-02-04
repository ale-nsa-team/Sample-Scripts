########  Example of Alcatel-Lucent Enterprise AOS API , Domain = MIB ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using MIB API and pull NTP information
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
print("Example of connecting to switch using MIB API and pull NTP information")
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
##### Pull the NTP data from switch  #####
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        ntp_result=switch_session.get('https://' + ip + '/mib/alaNtpPeerListTable?mibObject1=alaNtpPeerListAddress&mibObject2=alaNtpPeerListOffset', headers=headers)

        ntp_result_json=ntp_result.json()
        #print(ntp_result_json)
        print("--------------------------------------------------------------------------------")
        for x in ntp_result_json['result']['data']['rows']:
            print("")
            print("Switch : "  + switch)
            print ("NTP Server : " + ntp_result_json['result']['data']['rows'][x]['alaNtpPeerListAddress'])
            print ("NTP offset : " + ntp_result_json['result']['data']['rows'][x]['alaNtpPeerListOffset'])
            print("--------------------------------------------------------------------------------")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
