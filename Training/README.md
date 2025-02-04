# Training
A collection of code examples: Python & Bash Scripts to interact with ALE OmniSwitch and ALE OmniVista

There are various ways of interacting with ALE products and implement various automation tasks/projects using scripts and APIs. 
Here is a list of available methods. Examples for each method can be found in the related directory.
Please note that most of these methods require AOS 8.X and above

1. OmniSwitch Bash-Shell 	:	Since OmniSwitch is running on Linux,Bash scripting can be done on OmniSwitch Shell. In this method, the scripts are executed directly from switch CLI.
2. OmniSwitch Python-API	:	Omniswitch provides a rich API to perform pretty much everything that can be executed through CLI. There are two flavors of API access to OmniSwitch:

a. API call to CLI		:	This is an API call that is initiated from an external system to OmniSwitch. A CLI command is sent in the API request and the output of the command is returned as API response. The response is returned as plain text in a JSON object and needs to be parsed.

b. API call to MIB		: 	This is an API call that is initiated from an external system to OmniSwitch. An API request needs to be created using a known SNMP MIB object. The API request is sent using the specific MIB object name and parameters. The API response will return the content of the MIB object on the switch. The response is returned in a structured JSON object.

3. OmniSwitch Python-Shell	:	In this method, a Python script will be executed directly on the switch CLI. OmniSwitch AOS 8.X is shipped with Python and this makes it possible to execute Python scripts directly on the Shell/CLI.
4. OmniSwitch Python-SSH 	:	This is a Python SSH call that is initiated from an external system to OmniSwitch. With this method, any CLI command can be sent to OmniSwitch using SSH and the response (output of the command execution) will be returned as plain text that needs to be parsed.
5. OmniVista Python-API		:	OmniVista provides an API to access various databases in OV or even make changes on the discovered devices. 
	
