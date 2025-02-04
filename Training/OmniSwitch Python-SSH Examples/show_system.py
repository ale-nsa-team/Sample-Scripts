########  Example of Python and paramiko to connect to AOS ##################
########  Version 1.0                                                                                          ##################
########  Author: Kaveh Majidi , SE Team
######## Example of connecting to switch using Python Paramiko and pull system information

import paramiko
import yaml

######  Loading the list of switches and their IP/User/Password from yaml file #####
with open('switch_list.yaml') as file:
    switch_list=yaml.load(file)

##### Starting a loop to perform the following on each switch  #####
print("##########        Operation Started.........  #############")
print("Example of connecting to switch using SSH  and execute show system")

for switch in switch_list:
    ip=switch_list[switch]['ip']
    username=switch_list[switch]['username']
    password=switch_list[switch]['password']
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print ("Connected to "  +  ip)
        # Send the command (non-blocking)
        command="show system"
        stdin, stdout, stderr = ssh.exec_command(command)
        for line in stdout.read().splitlines():
            print(line)
    except paramiko.AuthenticationException:
        print ("Authentication failed when connecting to " + ip)
        sys.exit()
    except:
        print ("Could not SSH to %s, waiting for it to start" + ip)
        sys.exit()
    print ("Command done, closing SSH connection")
    ssh.close()
