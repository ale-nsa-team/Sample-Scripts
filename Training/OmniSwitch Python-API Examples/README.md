OmniSwitch Python-API		:	Omniswitch provides a rich API to perform pretty much everything that can be executed through CLI. There are two flavors of API access to OmniSwitch:

a. API call to CLI		:	This is an API call that is initiated from an external system to OmniSwitch. A CLI command is sent in the API request and the output of the command is returned as API response. The response is returned as plain text in a JSON object and needs to be parsed.

b. API call to MIB		: 	This is an API call that is initiated from an external system to OmniSwitch. An API request needs to be created using a known SNMP MIB object. The API request is sent using the specific MIB object name and parameters. The API response will return the content of the MIB object on the switch. The response is returned in a structured JSON object.
