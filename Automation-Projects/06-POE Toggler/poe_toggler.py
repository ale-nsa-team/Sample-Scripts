########  POE Toggler AOS API , Domain = CLI                                             ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Connecting to switch using CLI API and Restart POE service on some ports
import requests
import yaml
import urllib3
import time
import datetime
import keyring

######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def log(log_content,action):
    log_file = "poe_toggler.log"
    if "p" in action:
        print(log_content)
    if "l" in action:
        log_file = open(log_file,"a")
        log_file.write(log_content + "\n")
        log_file.close()
    if "c" in action:
        log_file = open(log_file,"w")
        log_file.write(log_content)
        log_file.close()
def calc_exec_time(start_time,end_time):
    execution_elapsed_time = end_time - start_time
    hours, rem = divmod(execution_elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    exec_duration  = ("{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds)))
    return exec_duration
def toggle_poe():
    ######  Loading the list of switches and their ports from yaml file #####
    with open('switch_ip_list.yaml') as file:
        switch_ip_list=yaml.load(file)
    username='admin'
    password=keyring.get_password('admin','xkcd')
    switch_session=requests.Session()
    headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
    ##### Starting a loop to perform the following on each switch  #####
    for ip in switch_ip_list:
        log("###############################################","pl")
        log("Connecting to " + ip + " ...","pl")
        login_response=switch_session.get('https://' + ip + '/auth/?&username=' + username + '&password=' + password, verify=False, headers=headers)
        login_response_json=login_response.json()
        login_status_code=login_response_json['result']['diag']
        if login_status_code != 200:
             log("","pl")
             log("Error ! Login/Connection failed for " + switch + " Please check your credentials or verify connection","pl")
             log("","pl")
        else:
            headers= {'Accept': 'application/vnd.alcatellucentaos+json'}
            ports_list=switch_ip_list[ip].split()
            for port in ports_list:
                log("Disabling POE on port " + port,"pl")
                command="lanpower+port+" + port + "+admin-state+disable"
                command_result=switch_session.get('https://' + ip + '/cli/aos?&cmd=' + command, headers=headers)
                command_result_json=command_result.json()
            log("Waiting for 10 Seconds...","pl")
            time.sleep(10)
            for port in ports_list:
                log("Enabling POE on port " + port,"pl")
                command="lanpower+port+" + port + "+admin-state+enable"
                command_result=switch_session.get('https://' + ip + '/cli/aos?&cmd=' + command, headers=headers)
                command_result_json=command_result.json()
        log("Closing the connection to " + ip + " ...","pl")
        switch_session.cookies.clear()
        switch_session.close()

def main():
    global start_time
    global end_time
    start_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    log("","c")
    log("","pl")
    log("##########        Operation Started  @  "  + now_string + "   #############","pl")
    toggle_poe()
    end_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    elapsed_time = calc_exec_time(start_time,end_time)
    log("","pl")
    log("##########        Operation Completed @ "  + now_string  + " , Execution time: "  + str(elapsed_time) + " ##########" ,"pl" )
    log("","pl")
main()
