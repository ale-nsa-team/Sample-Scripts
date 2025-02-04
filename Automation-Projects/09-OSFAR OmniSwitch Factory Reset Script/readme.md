# OSFAR

Bash Script to factory reset OmniSwitch

Developed by ALE-NAT Americas workgroup 


# Version

0.1

# Notes

This bash script is for resetting ALE's Omniswitch with AOS version 8.x or higher to factory default.

1. The script is written for AOS 8.x and higher. The script may not work properly in AOS 6.x family of products.

2. The script will NOT remove the user created directories. It only affects the default OmniSwitch files/directories.

3. In a Virtual Chassis setup with multiple chassis, the script needs to be copied and executed on each member of VC. 
Please note that when resetting a VC, disconnecting VFL is required since after resetting any chassis in a VC, Auto-VFL feature may rebuild the VC before completing the factory reset process.

4. After executing the script, the switch needs to be manually rebooted. You can reboot the switch by unplugging the power or by issuing the "reload from working no rollback-timeout command".
Do NOT execute "write-memory" after executing the script and before rebooting the switch since it will write the switch configuration back to the flash.


# How to use?

Step 1

Download the script from the GitHub page. We recommend downloading the osfar.zip file (On Github page, click on osfar.zip and use the Download button on next page) and then extracting the script. If you copy/paste the script text directly from the GitHub page and save it in a Windows machine, the script file will be saved with extra carriage return character at the end of each line. This will prevent the script from execution on the switch.

Step 2
   
Copy osfar.sh on the /flash directory of the OmniSwitch. This can be done using FTP or by using a USB memory stick.

Step 3

Assign read and execute permission to the file. For example : chmod 500 osfar.sh

Step 4

Execute the bash script using ./osfar.sh

The script will prompt twice for confirmation and then wait for five seconds before execution which gives user enough time to cancel the execution using Control-c.
Some file/directory not found warning messages are normal and expected during the execution. 


# License
This project is licensed under the MIT License
Copyright (c) [2023] [ALE-NAT Americas]
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
