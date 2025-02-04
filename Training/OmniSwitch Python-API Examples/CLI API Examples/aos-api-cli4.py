########  Example of Alcatel-Lucent Enterprise AOS API , Domain = CLI ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using CLI API and apply Multiple QOS commands
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
print("Example of connecting to switch using CLI API and apply Multiple QOS commands")
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
##### Creating and executing QOS commands  #####
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
##### Creating a list of commands to be executed ####################
        commands_list={}
        commands_list[0]='qos+flush'
        commands_list[1]='qos+apply'
        commands_list[2]='policy+condition+playback+multicast+ip+239.232.139.10+destination+ip+192.168.1.222'
        commands_list[3]='policy+action+kill_live+disposition+drop'
        commands_list[4]='policy+rule+playback_active+condition+playback+action+kill_live'
        commands_list[5]='qos+apply'
##### Executing Commands in the command list one by one from top to bottom ###
        for command in  commands_list:
            current_command=commands_list[command]
            exe_command=switch_session.get('https://' + ip + '/cli/aos?&cmd=' + current_command, headers=headers)

        show_command="show+configuration+snapshot+qos"
        show_result=switch_session.get('https://' + ip + '/cli/aos?&cmd=' + show_command, headers=headers)
        show_result_json=show_result.json()
        print("")
        print("____________        Show qos result for "  +  switch  + " ___________________")
        print(show_result_json['result']['output'])
        print("____________________________________________________________________")
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
