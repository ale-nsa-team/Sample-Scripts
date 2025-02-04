# Project
confcleaner
Developed by Kaveh Majidi @ ALE
Python Script to replace/mask hashed keys, credentials and passwords from ALE AOS configuration files
The scrip will replace keys/passwords/community strings, etc. with "XXXX" string in the following AOS configurations:
      sa-encryption
      sa-authentication
      ipsec security-key
      ip rip
      ip ospf
      ip isis
      ip bgp
      aaa radius-server
      aaa tacacs+
      aaa ldap-server
      policy server
      ip slb
      snmp community-map
	  

The Configuration log files should be provided as a zip package. Configuration log files should have .log extention. 
This tool is designed to process the output of the OmniVista Log files. Please see "OmniVista CLI Script Log Downloader" project which will generate the zipfiles. 
This script can be modified to process any configuration file.

How to execute:
After getting a ZIP file from the "OmniVista CLI Script Log Downloader", you run the confcleaner.py directly on the zip file as shown below.

Example : python3 confcleaner.py --zipfile=myconfigs.zip -v	  

# Version

1.0

# Requirements

Python > 3.2

# Dependencies
N/A

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
