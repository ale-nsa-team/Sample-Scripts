# OmniVista 2500 MAC Address Location Script

This script demonstrates how to use the OmniVista 2500 API to retrieve the location of a MAC address on the network. The location information can then be reused in other applications or processes.

## Requirements
- OmniVista 2500

## Usage
1. Modify the script (`get_mac_location_ov2500.py`) to set the following parameters:
   - **OmniVista 2500 IP address**
   - **Username and password**
   - **MAC address** to search for 
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python3 get_mac_location_ov2500.py
   ```

## Generalization
You can reuse the MAC location retrieval logic in other applications or automation workflows by integrating it into your own processes.
