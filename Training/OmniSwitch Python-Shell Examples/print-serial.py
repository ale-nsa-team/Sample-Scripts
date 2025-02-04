#Run the AOS command: show cmm, read and parse out the serial number.
#

import subprocess

output = subprocess.run(["show cmm"], stdout=subprocess.PIPE, shell=True)
output_str = output.stdout.decode("utf-8")

for line in output_str.split("\n"):
    if "Serial Number:" in line:
        serial_number = line.split(":")[1].strip().rstrip(",")
        print(serial_number)