# Project

POE Toggle V1.0
Developed by Kaveh Majidi @ ALE

Python script to toggle POE ports on an AOS switch.
Script has been tested and verified with Ubuntu 18.04

# Version

1.0

# Requirements

Python > 3.2

# Dependencies

Python packages:
yaml
urllib3
keyring

# Installation

Download or clone from https://github.com/kaveh-ale/poe_toggler.git

#  How to use?

Step 1.
Copy the poe_toggler.py  and switch_ip_list.yaml into a directory on a linux machine which has IP connectivity to the management IP of the switches. Make sure the linux user executing the python script has write access on the target directory.

Step2.
Modify the switch_ip_list.yaml using a text-editor to match your target switch IP address and port numbers. Each section starts with the IP of the switch followed by port numbers under it. Make sure you keep the format of the Yaml file as is(spacing and indentation).

Step3.
Make sure that the machine that is used to executed the script has Python 3 installed on it and the following packages are installed for python. If not, use PIP to install the following python packages

yaml
urllib3
keyring

Step4.
On the linux machine that you will be executing the script, execute python3 to get into python shell and use the following commands to create the keyring. In this example, we used the username "admin" and password "switch" which are default on AOS switches. Change them to username and password that matches your environment. This user should be able to login to AOS switch and perform POE Enable/Disable operation.

python3
>>> import keyring
>>> keyring.set_password('admin', 'xkcd', 'switch')

To verify, use the following command which should return the password
>>> keyring.get_password('admin', 'xkcd')
>>>exit()

Step5.
Modify the poe_toggler.py file with a text-editor and change username in lines 37 and 38 with the username that has been selected and used in the keyring above.

Step6.
Make sure Http protocol is enabled on the target switch and AAA for http is set correctly. The script is using AOS API so http access is required.

Step7.
Execute the script on the linux machine as shown below:

Python3 poe_toggler.py

The script connects to each switch, disables POE on the specified port, waits for 10 seconds and re-enable the POE on the target ports.
A log file,poe_toggler.log,  is created in the execution directory.

Step8.
Create a CRON job on the linux machine to execute the script at the specified time.



# License
This project is licensed under the MIT License
Copyright (c) [2020] [Kaveh Majidi]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
