########  Python Port Scanner
########  Alcatel-Lucent Enterprise OV API
########  Version 0.4
########  Author: Kaveh Majidi , SE Team
######## This Script connects to OV and discovers network devices and their ports. Then it will admin down ports based on specific criteria, for example if the switch ports has been inactive for a specific amount of time.

import time
import datetime
import requests
import urllib3
import os
import json
import argparse
import textwrap
import ipaddress
import sys
from getpass import getpass
from cryptography.fernet import Fernet

######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validate_ipaddress(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        pass
        return False

def log(log_content,action):
    log_file = log_file_name
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

def grid(grid_layout,data_object):
    try:
        col_count = (len(grid_layout))
        col_width_list =[]
        # Getting the Max string length in Data or Header
        for header in grid_layout:
            field = "x." + grid_layout[header]
            max_col_len=max(max([len(eval(field)) for x in data_object]),len(header))+1
            col_width_list.append(max_col_len)
        table_header_top = " " + "_" * (sum(col_width_list)+col_count-1)
        # Building table Header
        i=0
        table_header = ""
        table_header_bottom = ""
        table_tail = ""
        for header in grid_layout:
            table_header += header + " " * (col_width_list[i]-len(header)) +  "|"
            table_header_bottom += "-" * (col_width_list[i]) + "|"
            table_tail += "_" * (col_width_list[i]) + "|"
            i += 1
        # buiilding data rows
        table_row_block = ""
        for x in data_object:
            table_row = "|"
            i=0
            for header in grid_layout:
                field = "x." + grid_layout[header]
                table_row +=  eval(field) + " " * (col_width_list[i]-len(eval(field))) + "|"
                i += 1
            table_row_block += table_row + "\n"
        table = table_header_top + "\n|" + table_header + "\n|" + table_header_bottom + "\n" + table_row_block + "|" + table_tail
        return(table)
    except:
        print("Error building Grid")
        pass

def ov_login():
    global ov_session
    ov_ip=config.ov_ip
    user_hash =config.user_hash
    fernet = Fernet(user_hash.encode('utf8'))
    ov_username = fernet.decrypt(config.ov_username.encode('utf8')).decode()
    pass_hash=config.pass_hash
    fernet = Fernet(pass_hash.encode('utf8'))
    ov_password = fernet.decrypt(config.ov_password.encode('utf8')).decode()
    ov_session=requests.Session()
    headers = {"Content-Type":"application/json"}
    api_url="https://" + ov_ip + "/api"
    api_domain="/login"
    credentials={}
    credentials['userName']=ov_username
    credentials['password']=ov_password
    # Make a login API call to OV
    api_request=requests.Request('POST', api_url + api_domain, headers=headers, json=credentials)
    try:
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        login_response=api_response_json['message']
        return login_response
    except:
        log("Connection to OV failed, Please check OV IP and credentials.","pl")

def ov_logout(ov_ip):
    headers = {"Content-Type":"application/json"}
    api_url="https://" + ov_ip + "/api"
    api_domain="/logout"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    logout_response=api_response_json['status']
    return logout_response

class Config:
    def __init__(self):
        self.ov_ip=""
        self.ov_username=""
        self.ov_password=""
        self.inactive_days="90"
        self.execution_mode="Discover"
        self.execution_domain=["0.0.0.0/0"]
        self.user_hash=""
        self.pass_hash=""
    def load(self):
        config_file_exists = os.path.isfile('config.ini')
        if not config_file_exists:
            config_file = open("config.ini", "w+")
            clean_config={"ov_ip": "", "ov_username": "", "ov_password": "", "inactive_days": "90", "execution_mode": "discover","execution_domain": ["0.0.0.0/0"],"user_hash":"","pass_hash":""}
            json_clean_config=json.dumps(clean_config)
            config_file.write(json_clean_config)
            config_file.close()
            print("")
            print("Initial Setup...")
            print("")
            self.load()
        else:
            config_file = open("config.ini","r")
            json_config = config_file.read()
            config_file.close()
            config_list = json.loads(json_config)
            self.ov_ip = config_list["ov_ip"]
            self.ov_username = config_list["ov_username"]
            self.ov_password = config_list["ov_password"]
            self.inactive_days =  config_list["inactive_days"]
            self.execution_mode = config_list["execution_mode"]
            self.execution_domain = config_list["execution_domain"]
            self.user_hash =  config_list["user_hash"]
            self.pass_hash = config_list["pass_hash"]

    def save(self):
        config_list={}
        config_list["ov_ip"] = self.ov_ip
        config_list["ov_username"] = self.ov_username
        config_list["ov_password"] = self.ov_password
        config_list["inactive_days"] = self.inactive_days
        config_list["execution_mode"] = self.execution_mode
        config_list["execution_domain"] = self.execution_domain
        config_list["user_hash"] = self.user_hash
        config_list["pass_hash"] = self.pass_hash
        json_config=json.dumps(config_list)
        config_file = open("config.ini", "w")
        config_file.write(json_config)
        config_file.close()

class Port:
    def __init__(self):
        self.device_id="N/A"
        self.device_ip="N/A"
        self.device_name="N/A"
        self.device_location="N/A"
        self.ifindex="N/A"
        self.port_number="N/A"
        self.port_admin_status="N/A"
        self.port_operation_status="N/A"
        self.port_last_link_change="N/A"
        self.port_last_link_change_date="N/A"
        self.port_last_link_change_days="N/A"

class Port_List:
    def __init__(self):
        self.ports=[]
    def make_port_table(self,port_data):
        grid_layout={
        "Switch Name":'device_name',
        "Switch IP":'device_ip',
        "Location":'device_location',
        "Port#":'port_number',
        "Admin State":'port_admin_status',
        "Operation State":'port_operation_status',
        "Link Change Date":'port_last_link_change_date',
        "Inactive Day(s)":'port_last_link_change_days'
        }
        data_object =  port_data.ports
        port_table = grid(grid_layout,data_object)
        return port_table
    def pull_ports(self,device_list,ov_ip):
        headers = {"Content-Type":"application/json"}
        api_url="https://" + ov_ip
        list_start = 0
        list_end = len(device_list)
        list_step = 5
        for i in range(list_start, list_end, list_step):
            x = i
            current_list=device_list[x:x+list_step]
            current_list_str=""
            for device in current_list:
                current_list_str +=device + ","
            api_domain="/rest-api/port?deviceIds=" + current_list_str
            api_request=requests.Request('GET', api_url + api_domain , headers=headers)
            api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
            api_response_json=api_response.json()
            api_response_status=api_response_json['status']
            if api_response_status != "SUCCESS":
                log("API Call for some ports Failed !","pl")
            else:
                ov_json_device_list=api_response_json['response']
                current_unix_utc = int(datetime.datetime.utcnow().timestamp())
                for device in ov_json_device_list:
                    device_id=device['deviceId']
                    device_ip=device['deviceIp']
                    device_name=device['deviceName']
                    device_location=device['deviceLocation']
                    device_port_list=device['portList']
                    for port_item in device_port_list:
                        if "LAG" not in port_item['portData']['portNumber']:
                            port=Port()
                            port.device_id=device_id
                            port.device_ip=device_ip
                            port.device_name=device_name
                            port.device_location=device_location
                            port.port_number=port_item['portData']['portNumber']
                            port.ifindex=str(port_item['portData']['ifIndex'])
                            port.port_admin_status=port_item['portData']['adminStatus']
                            port.port_operation_status=port_item['portData']['PortStatus']
                            if port_item['portData']['lastTimeLinkChanged']:
                                port.port_last_link_change=port_item['portData']['lastTimeLinkChanged']
                                port.port_last_link_change_date=str(datetime.datetime.fromtimestamp(port.port_last_link_change/1000).strftime('%m-%d-%Y %H:%M:%S'))
                                port.port_last_link_change_days=str(round((float(current_unix_utc)-float((port.port_last_link_change/1000)))/(60*60*24)//1))
                                if port.port_admin_status == "Up" and port.port_operation_status == "Down" and int(port.port_last_link_change_days) >= int(inactive_days):
                                    self.ports.append(port)
    def disable_ports(self,port_list):
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        api_url="https://" + ov_ip
        api_domain="/api/port/update"
        for port in port_list.ports:
            target_device_id=port.device_id
            target_port_list=[]
            target_port_list.append(int(port.ifindex))
            api_payload={"data":{"portViewDeviceInfos":[{"deviceKey":target_device_id,"ports":target_port_list,"fields":{"adminStatus":"Down"}}]}}
            api_request=requests.Request('PUT', api_url + api_domain , headers=headers,json=api_payload)
            api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
            time.sleep(1)
            if api_response.status_code == 200:
                log("Disabling port " + port.port_number + " on device : " + port.device_name + " ,IP address: " + port.device_ip,"pl")
                port.port_admin_status="Disabled"
            else:
                log("Error : in disabling port " + " on device : " + port.device_name + " ,IP address: " + port.device_ip ,"pl")
                port.port_admin_status="N/A"

def pull_ov_devices(ov_ip):
    headers = {"Content-Type":"application/json"}
    api_url="https://" + ov_ip
    #Get List of Devices from OV
    api_domain="/rest-api/devices"
    api_request=requests.Request('GET', api_url + api_domain, headers=headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    api_response_status=api_response_json['status']
    if api_response_status != "SUCCESS":
        log("API Call for Device list Failed !","pl")
    else:
        ov_json_device_list=api_response_json['response']
        ov_device_list=[]
        for device_item in ov_json_device_list:
            device_id = device_item['deviceId']
            device_ip = ipaddress.ip_address(device_item['ipAddress'])
            device_add_flag=False
            for domain in execution_domain:

                ip_network=ipaddress.IPv4Network(domain)
                if device_ip in ip_network:
                    device_add_flag=True
                    break
            if device_add_flag == True:
                ov_device_list.append(device_id)
        return(ov_device_list)

def start():
    global ov_ip
    global inactive_days
    global execution_mode
    global execution_domain
    try:
        ov_ip=config.ov_ip
        if not ov_ip:
            print("OmniVista IP address is not configured. Please configure OV IP from Setting Menu.")
            main_menu()
        if not config.ov_username or not config.ov_password:
            print("OmniVista credentials are not configured. Please configure OV credentials from Setting Menu.")
            main_menu()
        inactive_days=config.inactive_days
        execution_mode=config.execution_mode
        execution_domain=config.execution_domain
    except:
        main_menu()
    start_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    log("","pl")
    log("######################## PSCAN Ver 0.1 ################################################","pl")
    log("Process Started , Connecting to OV @ " + ov_ip + ", Time: " + now_string ,"pl")
    ov_login_response=ov_login()
    if ov_login_response != "login.success":
        log("Login/Connection failed for OV @ " + ov_ip + " Please check your credentials or verify connection","pl")
    else:
        log("Pulling devices from OV ...","pl")
        ov_device_list=pull_ov_devices(ov_ip)
        if ov_device_list:
            device_count=len(ov_device_list)
            if device_count > 0:
                log("","pl")
                log( str(device_count) + " Devices detected. Pulling port information...","pl")
                log("","pl")
                log (" =======[ Searching Condition ]====================","pl")
                log (" Port Admin State     : Up","pl")
                log (" Port Operation State : Down","pl")
                log (" Port Inactive days   : " + inactive_days,"pl")
                log (" Switch Subnet(s)   : " + str(execution_domain),"pl")
                log (" ==================================================","pl")
                log("","pl")
                device_list=ov_device_list
                port_list=Port_List()
                port_list.pull_ports(device_list,ov_ip)
                port_count=len(port_list.ports)
                if port_count > 0:
                    port_table = port_list.make_port_table(port_list)
                    log(" " + str(port_count) + " port(s) found With the specified condition.","pl")
                    log("","pl")
                    log(port_table,"pl")
                    if execution_mode == "Discover":
                        log("Script is running in Discover mode , Report generated.","pl")
                    elif execution_mode == "Active":
                        log("Script is running in Active mode, Trying to Admin Down the ports that are matching condition...","pl")
                        port_list.disable_ports(port_list)
                        port_table = port_list.make_port_table(port_list)
                        log(port_table,"pl")
                else:
                    log("","pl")
                    log("No ports found With the specified condition.","pl")
            else:
                log("","pl")
                log("No device has been detected in OV within the specified domain(s)!","pl")
        else:
            log("","pl")
            log("No device has been detected in OV within the specified domain(s)!","pl")
        ov_logout_response=ov_logout(ov_ip)
        if ov_logout_response != "SUCCESS":
            log("Logout failed for OV @ " + ov_ip,"pl")
        else:
            log("Logged out of OV @ " + ov_ip,"pl")
    end_time = time.time()
    now = datetime.datetime.now()
    now_string = now.strftime("%H:%M:%S %m/%d/%Y ")
    elapsed_time = calc_exec_time(start_time,end_time)
    log("Operation Completed @ "  + now_string  + " , Execution time: "  + str(elapsed_time),"pl" )
    log("########################################################################################","pl" )
    log("","pl")

def show_config():
        print ("")
        print (" =======[ Current Settings ]==============================")
        print (" Omnivista IP address           :   " + config.ov_ip)
        if not config.ov_username or not config.ov_password:
            print (" Omnivista Credentials          :   " + "Not Configured")
        else:
            print (" Omnivista Credentials          :   " + "Configured")
        print (" Number of Port Inactivity Days :   " + config.inactive_days)
        print (" Script Execution mode          :   " + config.execution_mode)
        print (" Script Execution Domain        :   " + str(config.execution_domain))
        print (" =========================================================")
        print ("")

def set_ov_ip():
    print("")
    input_ov_ip = input("Enter OmniVista IP address (q for quit):")
    while(input_ov_ip.lower()!='q'):
        if(validate_ipaddress(input_ov_ip)==False):
            print("Invalid IP address.Try again")
        else:
            config.ov_ip =input_ov_ip
            print("OmniVista IP set to :" + input_ov_ip)
            break
        input_ov_ip = input("Enter OmniVista IP address (q for quit):")
    print("")
    config.save()

def set_ov_credentials():
    print("")
    input_user_name = input("Enter OmniVista username: ")
    while(input_user_name.lower()!='q'):
        if(not input_user_name):
            print("Invalid entry.Try again")
        else:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            enc_username = fernet.encrypt(input_user_name.encode())
            config.user_hash=key.decode('utf8')
            config.ov_username =enc_username.decode('utf8')
            print("OmniVista username is saved")
            break
        input_user_name = input("Enter OmniVista username: ")
    print("")
    input_password = getpass("Enter OmniVista password: ")
    while(input_password.lower()!='q'):
        if(not input_password):
            print("Invalid entry.Try again")
        else:
            key = Fernet.generate_key()
            fernet = Fernet(key)
            enc_password = fernet.encrypt(input_password.encode())
            config.pass_hash=key.decode('utf8')
            config.ov_password=enc_password.decode('utf8')
            print("OmniVista password is saved")
            break
        input_password = getpass("Enter OmniVista password: ")
    print("")
    config.save()

def set_inactive_days():
    print("")
    input_inactive_days = input("Enter Number of port inactivity days (q for quit):")
    while(input_inactive_days.lower()!='q'):
        if(not input_inactive_days):
            print("Invalid entry.Try again")
        elif not str.isdigit(input_inactive_days) or int(input_inactive_days) == 0:
            print("Invalid Number of days, Number of days should be an integer greater than 0")
        else:
            config.inactive_days =str(input_inactive_days)
            print("Number of port inactivity days is saved")
            break
        input_inactive_days = input("Enter Number of port inactivity days (q for quit):")
    print("")
    config.save()

def set_execution_mode():
    print ("")
    input_execution_mode = str(input("Select Execution mode, enter [1] for Discover and [2] for Active (q for quit):"))
    while(input_execution_mode.lower()!='q'):
        if(not input_execution_mode):
            print("Invalid entry.Try again")
        elif input_execution_mode == "1" or input_execution_mode == "2":
            if input_execution_mode == "1":
                config.execution_mode="Discover"
            if input_execution_mode == "2":
                config.execution_mode="Active"
            print("Execution mode is saved")
            break
        else:
            print(" Invalid selection, Please try again")
        input_execution_mode = input("Select Execution mode, enter [1] for discover and [2] for Active (q for quit):")
    print("")
    config.save()

def set_execution_domain():
    print ("")
    input_execution_domain = str(input("Enter IP subnet followed by CIDR that you want to be included. If multiple, separate with commas.For example: '192.168.1.0/24, 172.16.0.0/16'. For all IPs (Default), type '0.0.0.0/0' or hit entet. (q for quit):"))
    while(input_execution_domain.lower()!='q'):
        if not input_execution_domain:
            config.execution_domain=[]
            config.execution_domain.append('0.0.0.0/0')
            print ("")
            print("Execution domain is reset to all IPs and saved.")
        else:
            execution_domain_list=[]
            execution_domain_list = input_execution_domain.split(",")
            config.execution_domain=[]
            for network in execution_domain_list:
                try:
                    domain = str(ipaddress.IPv4Network(network))
                    config.execution_domain.append(domain)
                    print ("")
                    print("Execution domain is saved")
                except:
                    print ("")
                    print("Invalid IP Subnet.Please make sure you enter an IP Network address with CIDR. Try again")
                    set_execution_domain()
        break
    if len (config.execution_domain) == 0:
        print ("")
        config.execution_domain.append('0.0.0.0/0')
        print("Execution domain is reset to all IPs and saved.")
    print("")
    config.save()

def main_menu():
    print ("")
    print (" =======[ Main Menu ]==========")
    print (" [1] Settings")
    print (" [2] Execute")
    print (" [0] Quit")
    print (" ==============================")
    print ("")
    while True:
        try:
            selected_menu = int(input(" Select an option from menu:"))
        except ValueError:
            print ("")
            continue
        if selected_menu < 0 or selected_menu > 2:
            print ("")
            print(" Invalid selection, Please try again")
            print ("")
            continue
        elif selected_menu == 1:
            setting_menu()
        elif selected_menu == 2:
            start()
            main_menu()
        elif selected_menu == 0:
            print(" See ya!")
            sys.exit()

def setting_menu():
    print ("")
    print (" =====[ Configure Setting Menu ]=======================")
    print (" [1] Show Current Configurations")
    print (" [2] Set OmniVista IP address")
    print (" [3] Set OmniVista Credentials")
    print (" [4] Set Number of Inactivity Days")
    print (" [5] Set Script Execution Mode")
    print (" [6] Set Script Execution Domain by IP subnet")
    print (" [0] Back to Main Menu")
    print (" =======================================================")
    print ("")
    while True:
        try:
            selected_menu = int(input(" Select an option from menu:"))
        except:
            print ("")
            continue
        if selected_menu < 0 or selected_menu > 6:
            continue
        elif selected_menu == 1:
            show_config()
            setting_menu()
        elif selected_menu == 2:
            set_ov_ip()
            setting_menu()
        elif selected_menu == 3:
            set_ov_credentials()
            setting_menu()
        elif selected_menu == 4:
            set_inactive_days()
            setting_menu()
        elif selected_menu == 5:
            set_execution_mode()
            setting_menu()
        elif selected_menu == 6:
            set_execution_domain()
            setting_menu()
        elif selected_menu == 0:
            main_menu()

def menu_start():
    print(" __________________________________________________________")
    print(" _____")
    print("|  __ \ ")
    print("| |__) |___   ___  __ _  _ __ ")
    print("|  ___// __| / __|/ _` || '_ \ ")
    print("| |    \__ \| (__| (_| || | | |")
    print("|_|    |___/ \___|\__,_||_| |_|")
    print("__________________________________________________________")
    print("_________ Welcome To Pscan Python Port Scanner   _________")
    print("_________              Ver 0.4 Dev               _________")
    print("_________         ALE System Engineering Team    _________")
    print("_________         Support:kaveh majidi @ ALE     _________")
    print("__________________________________________________________")
    main_menu()

def main():
    parser = argparse.ArgumentParser(
        prog='PScan',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
           Port Scanner V0.4
           Developed by Kaveh Majidi @ ALE
           ---------------------------------------------------
           This Python tool pulls switch port status from OmniVista and it can be used
           to admin down the port based on the number of days that a port has been inactive.
           The script can be executed in two different modes:
           1. Discover : In this mode, the script will only pull the port information and
           createa a log with all the information
           2. Active :  In this mode, the script will pull the ports status and then
           Admin Down the ports if they have been inactive for specified number of days.

           Executing "python3 pscan.py"  will enter the Menu where you can specify the
           settings such as OmniVista IP/username/password, operation mode, number of days.
           If you wish to execute the script with already configured settings, use the -a parameter:

           Example : python3 pscan.py -a

           '''))
    parser.add_argument("-a",action="store_true",help="Script will execute automatically without going to Menu. It will use the specified settings")
    args = parser.parse_args()
    global log_file_name
    log_file_name=datetime.datetime.now().strftime('pscan_%m_%d_%Y_%H_%M.log')
    global config
    config = Config()
    config.load()
    if args.a:
        start()
    else:
        menu_start()

main()
