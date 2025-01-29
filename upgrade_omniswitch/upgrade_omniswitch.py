import requests
import json
import paramiko
import socket
import time
requests.packages.urllib3.disable_warnings() 

def sftp_transfer(hostname, port, username, password, local_file_path, remote_file_path):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for production!)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the host
        ssh_client.connect(hostname, port, username, password)
        
        # Create an SFTP session from the SSH connection
        sftp = ssh_client.open_sftp()
        
        # Transfer the file
        sftp.put(local_file_path, remote_file_path)
        
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh_client.close()
        
        print(f"Successfully transferred {local_file_path} to {hostname}:{remote_file_path}")
        
    except Exception as e:
        raise Exception(f"Failed to transfer file: {e}")



switch_session = requests.Session()

SWITCH_IP = "192.168.125.253"
SWITCH_WEBVIEW_PORT = "443"
SWITCH_URL = f"{SWITCH_IP}:{SWITCH_WEBVIEW_PORT}"
USERNAME = 'admin'
PASSWORD = 'switch'
SWITCH_SSH_PORT = "22"
IMAGE_NAME = "Uos.img"
FPGA_FILE_NAME = "fpga_kit_8757" #Put None if no upgrade
UBOOT_FILE_NAME = "u-boot.8.7.R03.30.tar.gz" #Put None if no upgrade

#AUTH
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json'
}
url = f"https://{SWITCH_URL}/?domain=auth&username={USERNAME}&password={PASSWORD}"
payload = {}
auth_response = switch_session.get(url, headers=headers, data=payload, verify=False)
if auth_response.status_code != 200:
   raise Exception(f"Login failed, check your credentials\n{auth_response.text}")

#Get version before
url = f"https://{SWITCH_URL}/?domain=mib&urn=systemMicrocodeLoadedTable%7CsystemVcHardwareTable&systemMicrocodeLoadedTable-mibObject0=systemMicrocodeLoadedDirectory&systemMicrocodeLoadedTable-mibObject1=systemMicrocodeLoadedVersion&systemVcHardwareTable-mibObject0=systemVcHardwareFpga1Version&systemVcHardwareTable-mibObject1=systemVcHardwareUbootVersion"
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json'
}
payload = {}
get_version_before = switch_session.get(url, headers=headers, data=payload, verify=False)
get_version_before_json = get_version_before.json()
running_directory = get_version_before_json["result"]["data"]["rows"][0]["systemMicrocodeLoadedDirectory"]
version_before_upgrade = get_version_before_json["result"]["data"]["rows"][0]["systemMicrocodeLoadedVersion"]
fpga_version_before = get_version_before_json["result"]["data"]["rows"][1]["systemVcHardwareFpga1Version"]
uboot_version_before = get_version_before_json["result"]["data"]["rows"][1]["systemVcHardwareUbootVersion"]

print(f"Before the upgrade:\nFPGA version: {fpga_version_before}\nU-Boot version: {uboot_version_before}\nWorking directory: {running_directory}\nRunning version: {version_before_upgrade}\n\n")

#Push FPGA and UBOOT upgrade files
if FPGA_FILE_NAME is not None:
    sftp_transfer(SWITCH_IP, 22, USERNAME, PASSWORD, FPGA_FILE_NAME, f"/flash/{FPGA_FILE_NAME}")
if UBOOT_FILE_NAME is not None:
    sftp_transfer(SWITCH_IP, 22, USERNAME, PASSWORD, UBOOT_FILE_NAME, f"/flash/{UBOOT_FILE_NAME}")

#If FPGA upgrade it
if FPGA_FILE_NAME is not None:
  url = f"https://{SWITCH_URL}/?domain=cli&cmd=update+fpga-cpld+cmm+all+file+{FPGA_FILE_NAME}"
  payload = {}
  headers = {
    'Accept': 'application/vnd.alcatellucentaos+json'
  }
  fpga_update_output = switch_session.get(url, headers=headers, data=payload, verify=False)
  if fpga_update_output.status_code != 200:
   raise Exception(f"FPGA upgrade failed\n{fpga_update_output.text}")
  time.sleep(60)

#If U-Boot upgrade it
if UBOOT_FILE_NAME is not None:
  url = f"https://{SWITCH_URL}/?domain=cli&cmd=update+uboot+cmm+all+file+/flash/{UBOOT_FILE_NAME}"
  payload = {}
  headers = {
    'Accept': 'application/vnd.alcatellucentaos+json'
  }
  uboot_update_output = switch_session.get(url, headers=headers, data=payload, verify=False)
  if uboot_update_output.status_code != 200:
   raise Exception(f"U-Boot upgrade failed\n{uboot_update_output.text}")
  time.sleep(60)

#Write Memory
url = f"https://{SWITCH_URL}/?domain=mib&urn=configManager"
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json',
  'Content-Type': 'application/x-www-form-urlencoded'
}
payload = 'mibObject0=configWriteMemory%3A1'
write_mem_output = switch_session.post(url, headers=headers, data=payload, verify=False)
if write_mem_output.status_code != 200:
 raise Exception(f"Write memory failed\n{write_mem_output.text}")
time.sleep(60)

#Send new image
sftp_transfer(SWITCH_IP, 22, USERNAME, PASSWORD, IMAGE_NAME, f"/flash/{running_directory}/{IMAGE_NAME}")

#Reload from running directory
url = f"https://{SWITCH_URL}/?domain=mib&urn=chasControlModuleTable"
payload = f"mibObject0=entPhysicalIndex%3A65&mibObject1=chasControlActivateTimeout%3A0&mibObject2=chasControlVersionMngt%3A6&mibObject3=chasControlWorkingVersion%3A{running_directory}&mibObject4=chasControlRedundancyTime%3A%200&mibObject5=chasControlDelayedActivateTimer%3A0&mibObject6=chasControlChassisId%3A0"
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json',
  'Content-Type': 'application/x-www-form-urlencoded',
}
reload_output = switch_session.post(url, headers=headers, data=payload, verify=False)
if reload_output.status_code != 200:
 raise Exception(f"Reload failed\n{reload_output.text}")
time.sleep(60)
#Wait until reboot end
wait = True
while wait:
  try:
    socket.create_connection((SWITCH_IP, SWITCH_WEBVIEW_PORT), timeout=10)
    wait = False
    print("Reboot done")
  except:
    print("Waiting until reboot")
    time.sleep(60)

#RE-AUTH
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json'
}
url = f"https://{SWITCH_URL}/?domain=auth&username={USERNAME}&password={PASSWORD}"
payload = {}
auth_response = switch_session.get(url, headers=headers, data=payload, verify=False)
if auth_response.status_code != 200:
  raise Exception(f"Login failed, check your credentials\n{auth_response.text}")

#Check version after upgrade
url = f"https://{SWITCH_URL}/?domain=mib&urn=systemMicrocodeLoadedTable%7CsystemVcHardwareTable&systemMicrocodeLoadedTable-mibObject0=systemMicrocodeLoadedDirectory&systemMicrocodeLoadedTable-mibObject1=systemMicrocodeLoadedVersion&systemVcHardwareTable-mibObject0=systemVcHardwareFpga1Version&systemVcHardwareTable-mibObject1=systemVcHardwareUbootVersion"
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json'
}
payload = {}
get_version_after = switch_session.get(url, headers=headers, data=payload, verify=False)
get_version_after_json = get_version_after.json()
running_directory = get_version_after_json["result"]["data"]["rows"][0]["systemMicrocodeLoadedDirectory"]
version_after_upgrade = get_version_after_json["result"]["data"]["rows"][0]["systemMicrocodeLoadedVersion"]
fpga_version_after = get_version_after_json["result"]["data"]["rows"][1]["systemVcHardwareFpga1Version"]
uboot_version_after = get_version_after_json["result"]["data"]["rows"][1]["systemVcHardwareUbootVersion"]

print(f"After the upgrade:\nFPGA version: {fpga_version_after}\nU-Boot version: {uboot_version_after}\nRunning version: {version_after_upgrade}\n\n")


#Copy Running to Certified
url = f"https://{SWITCH_URL}/?domain=mib&urn=chasControlModuleTable"

payload = 'mibObject0=entPhysicalIndex%3A65&mibObject1=chasControlWorkingVersion%3Aworking&mibObject2=chasControlVersionMngt%3A2'
headers = {
  'Accept': 'application/vnd.alcatellucentaos+json',
  'Content-Type': 'application/x-www-form-urlencoded'
}
running_to_certified_output = switch_session.post(url, headers=headers, data=payload, verify=False)
if running_to_certified_output.status_code != 200:
 raise Exception(f"Copy Running to Certified failed.\n{running_to_certified_output.text}\n\n Try to run the command: copy running certified flash-synchro")
time.sleep(2)

print("Upgrade Done!")
