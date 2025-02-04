########  Using SAA on switch and execute a python script on the switch based on the results of saa
########  Version 1.0                                                ##################
########  Author: Kaveh Majidi , SE Team

import time
import subprocess
import re
import os

file=open("/flash/python/port-map.txt","r")
for line in file:
    camera = ""
    port = ""
    command= ""
    if line != "":
        line_split = line.split("=")
        if len(line_split) > 1:
            camera=line_split[0]
            port=line_split[1].strip("\n")
            saa_output = subprocess.check_output(["show","saa",camera],universal_newlines=True)
            verify_string = re.search(rf"{camera}.*",saa_output)[0]
            if "failed" in verify_string:
                command= "interfaces " + port + "  admin-state disable"
                output = subprocess.check_output(command,shell=True)
                time.sleep(3)
                command="interfaces " + port + " admin-state enable"
                output = subprocess.check_output(command,shell=True)
            elif "success" in verify_string:
                pass
