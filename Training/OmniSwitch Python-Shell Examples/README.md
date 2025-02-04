# Python On Shell / CLI
In this method, a Python script will be executed directly on the switch CLI. OmniSwitch AOS 8.X is shipped with Python and this makes it possible to execute Python scripts directly on the Shell/CLI.
The example scripts that is provided here can be copied on the flash of the switch and then can be executed using python3 on the switch. There is a default "Python" directory on the switch that is the default path for Python scripts when using SAA and other features. However, a python script can be copied into any directory on the switch.
For example to execute the print-serial.py on the /flash directory of the switch, just execute "Python3 print-serial.py" from CLI of the switch. 	
