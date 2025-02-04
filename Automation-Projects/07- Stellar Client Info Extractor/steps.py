"""
STEPS Project V 1.0,  Alcatel-Lucent Enterprise
OmniAccess Stellar Export Python Script
STEPS is an API Interface to ALE's OmniVista NMS to extract and export OmniAcess Stellar Access Points data.
This module is developed to pull APs and Live Clients from OmniVisa and export them as a csv file.
June 2020, ALE SE Team, USA
"""
import os
import configparser
import csv
import requests
import time
import datetime
import urllib3
import json
import logging
from logging import handlers


class Config:
    def __init__(self):
        self.ov_ip = ""
        self.ov_username = ""
        self.ov_password = ""
        self.ov_access_token=""
        self.report_interval = ""
        self.ap_list_data_columns = ""
        self.ap_list_columns=[]
        self.client_list_data_columns = ""
        self.client_list_columns=[]
        self.device_file_name=""
        self.ap_file_name=""
        self.ov_session=""


def initiate_logger():
    global logger
    rfh = logging.handlers.RotatingFileHandler(
     	filename='logs/steps.log',
      	mode='a',
      	maxBytes=2*1024*1024,
      	backupCount=20,
      	encoding=None,
      	delay=0
    )
    logging.basicConfig(
      	level=logging.DEBUG,
      	format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%y-%m-%d %H:%M:%S",
        handlers=[
        	rfh
        ]
    )
    logger = logging.getLogger()

def load_config():
    try:
        config_data = configparser.ConfigParser()
        config_data.read_file(open('steps_config.cfg'))
        config.ov_ip = config_data.get('ov', 'ov_ip')
        config.ov_username = config_data.get('ov', 'ov_username')
        config.ov_password = config_data.get('ov', 'ov_password')
        config.report_interval = config_data.get('params', 'report_interval')
        config.ap_list_data_columns = config_data.get('params', 'ap_list_data_columns')
        config.ap_list_columns = [x.strip() for x in config.ap_list_data_columns .split(',')] if config.ap_list_data_columns else []
        config.client_list_data_columns = config_data.get('params', 'client_list_data_columns')
        config.client_list_columns = [x.strip() for x in config.client_list_data_columns .split(',')] if config.client_list_data_columns else []
        if int(config.report_interval)  < 60:
            print("Report interval is too short. Increase report interval in config file (Min 60 Seconds)")
            logger.error('Report interval is too short. Increase report interval in config file (Min 60 Seconds)')
            exit(1)
    except Exception as e:
        print("Error loading configuration file. Check the logs.")
        logger.error('Exception while parsing the configuration file - %s' %str(e))
        exit(1)

def connect_to_ov():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        logger.info('Connecting to OmniVista...')
        ov_session=requests.Session()
        headers = {"Content-Type":"application/json"}
        api_url="https://" + config.ov_ip + "/api"
        api_domain="/login"
        credentials={}
        credentials['userName']=config.ov_username
        credentials['password']=config.ov_password
        api_request=requests.Request('POST', api_url + api_domain, headers=headers, json=credentials)
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        login_response=api_response_json['message']
        if login_response != "login.success":
            print("Error Connecting to OV. Check the logs")
            logger.error("Login/Connection failed for OV @ " + config.ov_ip + " Please check your credentials or verify connection")
            return False
        else:
            logger.info("Connected to OV. Access token aquired.")
            config.ov_access_token= api_response_json['accessToken']
            config.ov_session=ov_session
            return True
    except Exception as e:
        logger.error('Login/Connection failed - %s' %str(e))
        return False

def get_client_data():
    try:
        logger.info("Pulling Client Data...")
        client_data=[]
        for page_number in range(1,11):
            api_url="https://" + config.ov_ip + "/api"
            ov_session=requests.Session()
            api_domain="/wma/onlineClient/getOnlineClientListByPage"
            request_payload={}
            request_payload['pageNumber']=page_number
            request_payload['pageSize']=1000
            request_payload['orderBy']= "clientName"
            request_payload['orderType']="ASC"
            api_call_headers = {'Authorization': 'Bearer ' + config.ov_access_token}
            api_request=requests.Request('POST', api_url + api_domain, headers=api_call_headers, json=request_payload)
            api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
            api_response_json=api_response.json()
            response_status=api_response_json['result']
            error_code=api_response_json['errorCode']
            error_message=api_response_json['errorMessage']
            if response_status != "success":
                logger.error('Error Pulling Client Data. Check the logs. %s')
            else:
                client_page_data=(api_response_json['data']['data'])
                if client_page_data:
                    client_data.extend(client_page_data)
                else:
                    break
        filtered_client_data=[]
        for client in client_data:
            new_client={}
            for client_property in config.client_list_columns:
                if client_property in client:
                    new_client[client_property]=client[client_property]
                else:
                    new_client[client_property]="N/A"
            filtered_client_data.append(new_client)
        client_header_dic={
        'clientName':'Client Name',
        'groupName':'Group Name',
        'apMac':'AP Mac',
        'assocationSSID':'Associated SSID',
        'workingMode':'Working Mode',
        'attachedBand':'Attached Band',
        'clientMac':'Client Mac',
        'clientIP':'Client IPv4 Address',
        'clientIPv6':'Client IPv6 Address',
        'clientType':'Device Category',
        'clientOS':'Device OS',
        'apName':'AP Name',
        'associateTime':'Associate Time',
        'channel':'Channel',
        'rssi':'RSSI',
        'rxError':'Rx Error',
        'txRetry':'Tx Retry',
        'inputFlow':'Rx Total',
        'outputFlow':'Tx Total',
        'rxRate':'Rx Rate',
        'txRate':'Tx Tate',
        'phyrxRate':'PHY Rx Rate',
        'phytxRate':'PHY Tx Rate',
        'apUNP':'Access Role Profile',
        'apVlanId':'VLAN',
        'tunnelID':'Tunnel',
        'farEndIP':'Far End IP',
        'securityType':'Security Type',
        'location':'Location',
        'auth_8021x_name':'802.1X User-Name'}
        client_list_header=[]
        for client_property in config.client_list_columns:
            if client_property in client_header_dic:
                client_list_header.append(client_header_dic[client_property])
            else:
                client_list_header.append("invalid column")
        save_to_csv(client_list_header,config.client_list_columns,filtered_client_data,config.client_file_name)
    except Exception as e:
        logger.error('Error Pulling Client Data. Check the logs. %s' %str(e))
        pass

def get_ap_data():
    try:
        logger.info("Pulling AP Data...")
        ap_data=[]
        api_url="https://" + config.ov_ip + "/api"
        ov_session=requests.Session()
        api_domain="/wma/accessPoint/getAPList/normal"
        api_call_headers = {'Authorization': 'Bearer ' + config.ov_access_token}
        api_request=requests.Request('GET', api_url + api_domain, headers=api_call_headers)
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        response_status=api_response_json['result']
        error_code=api_response_json['errorCode']
        error_message=api_response_json['errorMessage']
        if response_status != "success":
            logger.error('Error Pulling Client Data. Check the logs. %s')
        else:
            ap_data=(api_response_json['data'])
        filtered_ap_data=[]
        for ap in ap_data:
            new_ap={}
            for ap_property in config.ap_list_columns:
                if ap_property == "groupName":
                    new_ap[ap_property]=ap['apGroups'][ap_property]
                elif ap_property == "groupDescription":
                    new_ap[ap_property]=ap['apGroups']['description']
                elif ap_property == "countryCode":
                    new_ap[ap_property]=ap['apGroups']['profile']['countryCode']
                elif ap_property == "profileName":
                    new_ap[ap_property]=ap['apGroups']['profile']['name']
                elif ap_property in ap:
                    new_ap[ap_property]=ap[ap_property]
                else:
                    new_ap[ap_property]="N/A"
            filtered_ap_data.append(new_ap)
        ap_header_dic={
        'apName':'AP Name',
        'groupName':'Group Name',
        'groupDescription':'Group Description',
        'macAddress':'AP MAC',
        'bleMac':'BLE MAC',
        'ipMode':'IP Mode',
        'ipAddress':'IP Address',
        'gateway':'Default Gateway',
        'subnetMask':'Subnet Address',
        'deviceDNS':'DNS',
        'location':'AP Location',
        'apStatus':'Status',
        'countryCode':'Country Code',
        'vlanId':'Management VLAN ID',
        'model':'AP Model',
        'version':'AP Version',
        'profileName':'RF Profile',
        'clientCount':'Client Count',
        'changes':'Saved/Unsaved',
        'ledMode':'LED Mode',
        'channels':'Channel',
        'noiseFloor':'Noise Floor',
        'channelUtilization':'Channel Utilization',
        'eirps':'EIRP',
        'lacpStatus':'LACP Status',
        'linkStatus':'Link Status',
        'workMode':'Work Mode',
        'channelWidth':'Channel Width',
        'upTime':'Up Time',
        'wcfStatus':'Web Content Filtering'}
        ap_list_header=[]
        for ap_property in config.ap_list_columns:
            if ap_property in ap_header_dic:
                ap_list_header.append(ap_header_dic[ap_property])
            else:
                ap_list_header.append("invalid column")
        save_to_csv(ap_list_header,config.ap_list_columns,filtered_ap_data,config.ap_file_name)
    except Exception as e:
        print(e)
        logger.error('Error Pulling Client Data. Check the logs. %s' %str(e))
        pass

def save_to_csv(header,fields,data,filename):
    try:
        logger.info("Saving Data to "+filename)
        with open(filename, 'w') as csvfile:
            header_writer = csv.writer(csvfile)
            header_writer.writerow(header)
            data_writer= csv.DictWriter(csvfile,fieldnames = fields)
            data_writer.writerows(data)
    except Exception as e:
        logger.error('Error Writting to CSV file. Check access permissions %s' %str(e))
        pass

def logout_ov():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        headers = {"Content-Type":"application/json"}
        api_url="https://" + config.ov_ip + "/api"
        api_domain="/logout"
        api_request=requests.Request('GET', api_url + api_domain, headers=headers)
        api_response = config.ov_session.send(config.ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        logout_response=api_response_json['status']
        if logout_response == "SUCCESS":
            logger.info("Closed connection to OmniVista.")
    except Exception as e:
        pass

def main():
        global config
        config=Config()
        initiate_logger()
        load_config()
        print('STEPS is Running.... Interval to collect data is  ' + str(config.report_interval) + ' Seconds.' )
        while True:
            try:
                load_config()
                logger.info("____________ Execution Cycle Started________________________")
                ov_connection=connect_to_ov()
                if ov_connection:
                    start_time = time.time()
                    cur_time = time.strftime("%Y_%m_%d_T_%H_%M_%S", time.localtime())
                    config.ap_file_name='ap_data/stellar_APs_%s.csv' %str(cur_time)
                    config.client_file_name='client_data/stellar_Clients_%s.csv' %str(cur_time)
                    get_ap_data()
                    get_client_data()
                    logout_ov()
            except Exception as e:
                print(str(e))
                logger.error('Error while Pulling Data using APIs %s' %str(e))
            finally:
                end_time = time.time()
                exe_time = round(end_time - start_time)
                logger.debug('Execution time - %dsec.' %exe_time)
                logger.info("____________ Execution Cycle Completed____________________")
                time.sleep(int(config.report_interval) - exe_time)

main()
