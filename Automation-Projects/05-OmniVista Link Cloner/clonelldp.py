########  Alcatel-Lucent Enterprise OV API
########  Version 1.0
########  Author: Kaveh Majidi , SE Team
########  This Script connects to OV and discovers the LLDP links and clone them to manual links.
import time
import datetime
import requests
import yaml
import urllib3
######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enter OV IP and Credentials here
ip='10.10.10.10'
username='admin'
password='switch'

def log(log_content,action):
    log_file = "clonelldp.log"
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

def ov_login(ip,username,password):
    global ov_session
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
    return login_response

def ov_logout(ip):
    headers = {"Content-Type":"application/json"}
    api_url="https://" + ip + "/api"
    api_domain="/logout"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    logout_response=api_response_json['status']
    return logout_response

def clone_links(ip):
    headers = {"Content-Type":"application/json"}
    api_url="https://" + ip + "/api"
    # Get List of LLDP Links
    api_domain="/topology/topologylinks?linkOrigin=ORIGIN_LLDP"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    lldp_link_list=api_response_json['response']
    # Get List of Manual Links
    api_domain="/topology/topologylinks?linkOrigin=ORIGIN_MANUAL"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    manual_link_list=api_response_json['response']
    #Remove the links that already have been cloned
    del_index_list=[]
    for lldp_link in lldp_link_list:
        lldp_local_id= lldp_link['localId']
        lldp_remote_id= lldp_link['remId']
        lldp_link_index=(lldp_link_list.index(lldp_link))
        for manual_link in manual_link_list:
            if  manual_link['localId'] == lldp_local_id and manual_link['remId'] == lldp_remote_id:
                del_index_list.append(lldp_link_index)
    del_index_list = sorted(del_index_list, reverse=True)
    for idx in del_index_list:
        if idx < len(lldp_link_list):
            lldp_link_list.pop(idx)
    #Clone if there are LLDP links that are not cloned
    link_count=len(lldp_link_list)
    if link_count > 0:
        log("##########        Found  "  + str(link_count) + " link(s) that need(s) to be cloned. Cloning link(s)... ","pl")
        for link in lldp_link_list:
            link['origin']="ORIGIN_MANUAL"
        new_link_list=[]
        for link in lldp_link_list:
            link_item=dict()
            link_item["TopologyLinkVO"]= link
            new_link_list.append(link_item)
        #print(new_link_list)
        api_domain="/topology/topologylinks"
        api_request=requests.Request('POST', api_url + api_domain, headers=headers, json=new_link_list)
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        link_clone_status=api_response_json['status']
        #print(link_clone_status)
        if link_clone_status != "SUCCESS":
            log("##########        Cloning Faild !","pl")
        else:
            log("##########        Cloning Successful","pl")
    else:
        log("##########        No new link found for cloning","pl")

def start():
    start_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    log("##########        Process Started , Connecting to OV  @  "  + now_string ,"pl")
    ov_login_response=ov_login(ip,username,password)
    if ov_login_response != "login.success":
        log("##########        Login/Connection failed for OV @ " + ip + " Please check your credentials or verify connection","pl")
    else:
        clone_links(ip)
        ov_logout_response=ov_logout(ip)
        if ov_logout_response != "SUCCESS":
            log("##########        Logout failed for OV @ " + ip,"pl")
        else:
            log("##########        Logged out of OV @ " + ip,"pl")
    end_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    elapsed_time = calc_exec_time(start_time,end_time)
    log("##########        Operation Completed @ "  + now_string  + " , Execution time: "  + str(elapsed_time),"pl" )
    log("#######################################################################","pl" )

start()
