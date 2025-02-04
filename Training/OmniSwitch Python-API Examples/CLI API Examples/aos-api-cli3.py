########  Example of Alcatel-Lucent Enterprise AOS API , Domain = CLI ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using CLI API and pull Linkagg table
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
print("Example of connecting to switch using CLI API and pull Linkagg table and parse the data")
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
##### Pull linkagg table from switch  #####
        headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
        linkagg_result=switch_session.get('https://' + ip + '/cli/aos?&cmd=show+linkagg', headers=headers)
        linkagg_result_json=linkagg_result.json()
        print("")
        print("_____________Linkagg Table  For "  +  switch  + " ________________________")
        print(linkagg_result_json['result']['output'])
        print("____________________________________________________________________")
        linkagg_output = linkagg_result_json['result']['output']
        linkagg_dic = {}
        split_linkagg_output=linkagg_output.splitlines()
        for line in split_linkagg_output:
            if "-+-" in line:
                linkagg_header_line = line
                linkagg_header_len=len(linkagg_header_line)
                plus_pos1= linkagg_header_line.index('+', 0,linkagg_header_len)+1
                plus_pos2= linkagg_header_line.index('+', plus_pos1 ,linkagg_header_len)+2
                plus_pos3= linkagg_header_line.index('+', plus_pos2 ,linkagg_header_len)+2
                plus_pos4= linkagg_header_line.index('+', plus_pos3 ,linkagg_header_len)+1
                plus_pos5= linkagg_header_line.index('+', plus_pos4 ,linkagg_header_len)+2
                plus_pos6= linkagg_header_line.index('+', plus_pos5 ,linkagg_header_len)+2
                for linkagg in split_linkagg_output:
                    if linkagg:
                        linkagg_row=str(linkagg).strip()
                        first_char=linkagg_row[0].strip()
                        if first_char.isnumeric():
                            linkagg_type=str(linkagg_row[plus_pos1-2:plus_pos2-4]).strip()
                            linkagg_snmp_id=str(linkagg_row[plus_pos2-4:plus_pos3-4]).strip()
                            linkagg_size=str(linkagg_row[plus_pos3-4:plus_pos4-4]).strip()
                            linkagg_admin_state=str(linkagg_row[plus_pos4-3:plus_pos5-4]).strip()
                            linkagg_operational_state=str(linkagg_row[plus_pos5-4:plus_pos6-3]).strip()
                            linkagg_dic.update({first_char:{"type":linkagg_type,"snmp_id":linkagg_snmp_id,"size":linkagg_size,"admin_state":linkagg_admin_state,"operational_state":linkagg_operational_state}})
        print(linkagg_dic)
        switch_session.cookies.clear()
        switch_session.close()
print("")
print("##########        Operation Completed       ##########")
