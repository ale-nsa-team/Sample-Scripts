API call to CLI	:	This is an API call that is initiated from an external system to OmniSwitch. A CLI command is sent in the API request and the output of the command is returned as API response. The response is returned as plain text in a JSON object and needs to be parsed.

switch_list.yaml file includes a list of switches with their respective IPs and login credentials that the scripts will be executed on.  

Examples:
1.	Connect to switch using an API call and pull VLAN table
2.	Connect to switch using an API call and create a VLAN 
3.	Connect to switch using an API call and pull linkagg table
4.	Connect to switch using an API call and apply multiple QOS commands
