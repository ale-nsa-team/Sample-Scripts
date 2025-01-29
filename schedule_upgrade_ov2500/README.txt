# OmniVista 2500 Upgrade Scheduling Script

This script demonstrates how to use the OmniVista 2500 API to schedule an upgrade for an OmniSwitch.

## Requirements 
- OmniVista 2500

## Usage
1. **Upload the image archive**:  
   Before running the script, you need to upload the archive containing the image, FPGA, and U-Boot files to OmniVistai 2500.  
   To do this, navigate to `CONFIGURATION > Resource Manager > Upgrade Image`, then click **Import**.
2. **Modify the script**:  
   Edit the script (`schedule_upgrade_ov2500.py`) to set the following parameters:
   - **OmniVista 2500 IP address**
   - **Username and password**
   - **Switch name** to upgrade
3. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the script**:  
   Once the script is configured, you can run it to schedule the upgrade:
   ```bash
   python3 schedule_upgrade_ov2500.py
   ```

## Generalization
This script can be reused in other applications to automate the scheduling of upgrades for multiple switches. You can integrate the code into your own automation workflows to schedule upgrades based on your network needs, or trigger upgrades as part of a larger maintenance process.
