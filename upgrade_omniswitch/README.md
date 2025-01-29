# OmniSwitch Upgrade Script
This script is an example of how to automate the upgrade process for OmniSwitches using the REST API and SFTP.  

## Requirements
- The image file must be in the same folder as the script.
- The FPGA and U-Boot files are only required if necessary for your upgrade.
- HTTP access on the switch must be enabled with the following command:
   ```bash
   aaa authentication http local
   ```

## Usage
1. Modify the script (`upgrade_omniswitch.py`) to set the following parameters:
   - **Image, FPGA, and U-Boot file names**
   - **Switch IP address**
   - **Username and password**  
2. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python3 upgrade_omniswitch.py
   ```

## Generalization
To upgrade multiple OmniSwitches, you can modify the script to loop over a list of switches and apply the upgrade process accordingly.
