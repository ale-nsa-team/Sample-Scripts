# SSH With Python to OmniSwitch

Developed by Kaveh Majidi @ ALE

Some Examples on how to use Python to connect to AOS over SSH. 
In this example, "show system" command is sent to switch. Any other CLI command can be sent using this method. If the CLI command have an output, the output will be returned in stdout.
The Paramiko Python Library is used in this example.

switch_list.yaml file includes a list of switches with their respective IPs and login credentials that the scripts will be executed on.  


# Version

1.0

# Requirements

Python > 3.2

# Dependencies
Paramiko Python Library

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
