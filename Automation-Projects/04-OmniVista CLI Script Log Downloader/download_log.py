########  OmniVista CLI Script Log Downloader
########  Version 1.0
########  Author: Kaveh Majidi , SE Team
########  Credit: Brian Witt  @ ALE
########  This script connects to OmniVista and dowmloads a list of CLI-script log files, then it selects specific logs and download all the selected logs as a zip file.
########  The followin script collect all the log files that has been generated during last 24 hours and have the "health_check_script"  string as part of the log file name.
########  The output of the script is a single Zip file containing all the individual log files (seperated by directories having switch IP as directory name) 
########  OmniVista IP and credentials should be provided in the ov_list.yaml file.

import requests
import yaml
import urllib3
import time
import datetime
import zipfile

######  Disable warning on insecure connection  #####
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

######  Loading the OV IP/User/Password from yaml file #####
with open('ov_list.yaml') as file:
    ov_list=yaml.load(file)
for ov in ov_list:
    ip=ov_list[ov]['ip']
    username=ov_list[ov]['username']
    password=ov_list[ov]['password']

print("##########        Operation Started.........  #############")
print("")
# Defining all API requirements
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

# if login is successful then continue
if login_response != "login.success":
    print("")
    print("Error ! Login/Connection failed for OV @ " + ip + " Please check your credentials or verify connection")
    print("")
else:
    print("Downloading List of log files")
    print("")
    access_token= login_response=api_response_json['accessToken']
    # Get the list of scripting log files.
    api_domain="/telnet/scriptinglogfiles"
    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_request=requests.Request('GET', api_url + api_domain, headers=api_call_headers)
    api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
    api_response_json=api_response.json()
    response_status=api_response_json['status']
    if response_status != "SUCCESS":
        print("")
        print("Error in getting requested data, please check your query. Response Code: " + response_code)
        print("")
    else:
        print("Compiling List of log files, the following log files will be included in the final zip file :")
        print("")
        # Get the current system time and subtract the period that logs need to be collected, in this example : logs in last 24 Hrs
        current_time=(datetime.datetime.now())
        current_unixtime = time.mktime(current_time.timetuple())

        # 86400 seconds in 24 hrs multiplied by 1000 to Miliseconds since OV saves timestamps in Miliseconds
        log_start_time=int((current_unixtime  -  86400) * 1000)
        # Creating request_body placeholder with empty valueObjects
        request_body={"TelnetGenericRequestObject":{"requestType":"delete","objectType":"ScriptingLogFile","valueObjects":[]}}
        for log in api_response_json['response']['result']:
            log_timestamp=int(log['timeStamp'])

           # Get the information for all the log files that their timestamp are greater than last 24 hrs
            if log_timestamp > log_start_time:
                fileName=log['fileName']
                ipAddress=log['ipAddress']
                macAddress=log['macAddress']
                if  "health_check_script" in fileName:
                    log_item={'ScriptingLogFileVO':{}}
                    log_item['ScriptingLogFileVO'].update({'fileName':fileName})
                    log_item['ScriptingLogFileVO'].update({'ipAddress':ipAddress})
                    log_item['ScriptingLogFileVO'].update({'macAddress':macAddress})
                    request_body['TelnetGenericRequestObject']['valueObjects'].append(log_item)
                    print(ipAddress + " -> " + fileName)

        # Export all logs to a zip file, the name of the zip file will be returned in the api response
        print("")
        print("Generating Zip file on OV server")
        print("")
        api_domain="/telnet/exportlog"
        api_call_headers = {'Authorization': 'Bearer ' + access_token}
        api_request=requests.Request('POST', api_url + api_domain, headers=api_call_headers, json=request_body)
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        api_response_json=api_response.json()
        export_response_status=api_response_json['status']
        if export_response_status != "SUCCESS":
            print("")
            print("Error in Exporting the log files " + response_code)
            print("")
        else:
            for file_item in api_response_json['response']['result']:
                zip_file_name=file_item['ScriptingLogFileVO']['fileName']
        print("Downloading Zip file from OV server")
        print("")
        api_domain="/telnet//downloadzip?zipFileName=" +  zip_file_name
        api_call_headers = {'Authorization': 'Bearer ' + access_token}
        api_request=requests.Request('GET', api_url + api_domain, headers=api_call_headers)
        api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
        download_response_status_code=api_response.status_code
        if download_response_status_code != 200:
            print("")
            print("Error in Dwonloading the Zip file " + str(download_response_status_code))
            print("")
        else:
            with open(zip_file_name, 'wb') as f:
                f.write(api_response.content)
            print("Zip File -> " + zip_file_name + " Downloaded!")
            print("")

#Logout of Omnivista
api_domain="/logout"
api_request=requests.Request('GET', api_url + api_domain, headers=headers)
api_response = ov_session.send(ov_session.prepare_request(api_request), verify=False)
api_response_json=api_response.json()
