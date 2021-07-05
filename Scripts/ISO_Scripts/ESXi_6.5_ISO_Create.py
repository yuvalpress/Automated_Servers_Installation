#!/usr/bin/python3
# Imports
import os
import sys
import subprocess
from shutil import copyfile as copy
import time

# Default Values

# Kickstart Files
VMWARE65_KICKSTART_ETH = "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Kickstart/ks-eth.cfg"
VMWARE65_KICKSTART_FIBER = "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Kickstart/ks-fiber.cfg"

# Get command line arguments
iDrac_Server = sys.argv[1]
hn = sys.argv[2]
network = sys.argv[3]  # team or single
ip = sys.argv[4]
nm = sys.argv[5]
dg = sys.argv[6]
ntp = sys.argv[7]
dns = sys.argv[8]
if "team" in network:
    interface = sys.argv[9]
    second_interface = sys.argv[10]
else:
    interface = sys.argv[9]
    second_interface = sys.argv[10]

# dir = str(iDrac_Server) + "_ISO"

# mount iso to new folder
# if os.path.isdir("//mnt//%s" % str(iDrac_Server)):
#     print("Directory already exists..")
# else:
#     os.mkdir("//mnt//%s" % str(iDrac_Server))
#     print("Created mounting directory")

# start iso modification process
print("Executing ISO Modification process..")
# subprocess.check_call(['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash '
#                        'Scripts/copyISOFiles.sh', VMWARE65_KICKSTART_ETH, "VMWARE"])

try:
    if os.path.exists('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                      'Content//Mounted_ISO//ESXi6.5//ks.cfg'):
        os.remove('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                        'Content//Mounted_ISO//ESXi6.5//ks.cfg')

    new_kickstart = open('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                         'Content//Mounted_ISO//ESXi6.5//ks.cfg', 'wt')
    with open('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files Content//Kickstart//ks-eth.cfg',
              'rt') as kickstart:
        for line in kickstart:
            if "--device=" in line:
                new_kickstart.write(
                    line.replace("--device=", "--device=%s" % interface).replace("--ip=", "--ip=%s" % ip).replace(
                        "--gateway=", "--gateway=%s" % dg).replace("--netmask=", "--netmask=%s" % nm).replace(
                        "--hostname=", "--hostname=%s" % hn))
            elif "interface1" in line:
                new_kickstart.write(line.replace("interface1", interface))
            elif "interface2" in line:
                new_kickstart.write(line.replace("interface2", second_interface))
            else:
                new_kickstart.write(line)
            # elif "NTP=" in line:
            #    new_kickstart.write(line.replace("NTP=", "NTP='%s'" % ntp))
            # else:
            #    new_kickstart.write(line.replace("DNS=", "DNS='%s'" % dns))

    new_kickstart.close()
    kickstart.close()

    print("Generate ISO File")
    subprocess.check_call(['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash '
                           'Scripts/generateISO.sh',
                           '/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/ESXi6.5',
                           "null", '%s.iso' % hn,
                           "VMWARE"])

except Exception as err:
    print("Operation Failed with the following error: %s" % err)
