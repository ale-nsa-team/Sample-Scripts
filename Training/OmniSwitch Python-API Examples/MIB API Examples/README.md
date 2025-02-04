API call to MIB	:	This is an API call that is initiated from an external system to OmniSwitch. An API request needs to be created using a known SNMP MIB object. The API request is sent using the specific MIB object name and parameters. The API response will return the content of the MIB object on the switch. The response returned in a structured JSON object.
switch_list.yaml file includes a list of switches with their respective IPs and login credentials that the scripts will be executed on.  
Examples:
1.	Connect to switch using MIB API and pull NTP information
2.	Connect to switch using MIB API and pull all ports MACs
3.	Connect to switch using MIB API and create a VLAN with description
4.	Connect to switch using MIB API and pull IP interface information
5.	Connect to switch using MIB API and pull linkagg information

