#!/usr/bin/python3
# Imports
import os
import sys
import subprocess
from shutil import copyfile as copy
import time

# Default Values
# iso files links
ISO = "/Jenkins/ISO_Files/Linux/RHEL/7.5/RHEL-7.5_2019-04-07_18-12-58.iso"

# Kickstart Files
KICKSTART = "/Jenkins/Automated_Installation_Files/Kickstart_Templates/ks.cfg.install_on_sda_bios-single"
KICKSTART_TEAM = "/Jenkins/Automated_Installation_Files/Kickstart_Templates/ks.cfg.install_on_sda_bios-team"

# Boot menu
BOOTMENU = "/Jenkins/Automated_Installation_Files/Boot_menu_Templates/RHEL75"

# Get command line arguments
iDrac_Server = sys.argv[1]
hn = sys.argv[2]
network = sys.argv[3] # team or single
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

dir = str(iDrac_Server) + "_ISO"

# mount iso to new folder
if os.path.isdir("//mnt//%s" % str(iDrac_Server)):
    print("Directory already exists..")
else:
    os.mkdir("//mnt//%s" % str(iDrac_Server))
    print("Created mounting directory")

# start iso modification process
if "team" not in network:
    print("Executing ISO Modification process with one port network configuration")
    subprocess.check_call(['/Jenkins/Scripts/bashScripts/copyISOFiles.sh', '/mnt/%s' % str(iDrac_Server), '/Jenkins/tmp_ISO/ISO_Folders/%s' % dir, ISO, KICKSTART, BOOTMENU, "RHEL"])

    if os.path.isdir("//Jenkins//tmp_ISO//ISO_Folders//%s" % dir):
        new_kickstart = open('//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg' % dir, 'wt')
        with open(KICKSTART, 'rt') as kickstart:
            for line in kickstart:
                if "HN=''" in line:
                    new_kickstart.write(line.replace("HN=''", "HN='%s'" % hn))
                elif "i=" in line:
                    new_kickstart.write(line.replace("i=", "i=%s" % interface).replace("--ip=", "--ip=%s" % ip).replace("--netmask=", "--netmask=%s" % nm).replace("--gateway=", "--gateway=%s" % dg))
                elif "NTP=" in line:
                    new_kickstart.write(line.replace("NTP=", "NTP='%s'" % ntp))
                elif "DNS=" in line:
                    new_kickstart.write(line.replace("DNS=", "DNS='%s'" % dns))
                else:
                    new_kickstart.write(line)

        new_kickstart.close()
        kickstart.close()

        sub = subprocess.Popen(["mv", "-f", '//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg' % dir, "//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg.install_on_sda_bios" % dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Generate ISO File")
        subprocess.check_call(['/Jenkins/Scripts/bashScripts/generateISO.sh', '/Jenkins/tmp_ISO/ISO_Folders/%s' % dir, "RHEL-7.5 Server.x86_64", '%s.iso' % hn, "RHEL"])

    else:
        print("Operation Failed")

else:
    print("Executing ISO Modification process with teaming network configuration")
    subprocess.check_call(['/Jenkins/Scripts/bashScripts/copyISOFiles.sh', '/mnt/%s' % str(iDrac_Server), '/Jenkins/tmp_ISO/ISO_Folders/%s' % dir, ISO, KICKSTART_TEAM, BOOTMENU, "RHEL"])

    if os.path.isdir("//Jenkins//tmp_ISO//ISO_Folders//%s" % dir):
        new_kickstart = open('//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg' % dir, 'wt')
        with open(KICKSTART_TEAM, 'rt') as kickstart:
            for line in kickstart:
                if "HN=''" in line:
                    new_kickstart.write(line.replace("HN=''", "HN='%s'" % hn))
                elif "$TEAM_MASTER_NUMBER" in line:
                    new_kickstart.write(line.replace("$TEAM_MASTER_NUMBER", "0"))
                elif "$TEAM_IP" in line:
                    new_kickstart.write(line.replace("$TEAM_IP", "%s" % ip))
                elif "$TEAM_PREFIX" in line:
                    new_kickstart.write(line.replace("$TEAM_PREFIX", "%s" % nm))
                elif "$GATEWAY" in line:
                    new_kickstart.write(line.replace("$GATEWAY", "%s" % dg))
                elif "$NIC1" in line:
                    new_kickstart.write(line.replace("$NIC1", "%s" % interface))
                elif "$NIC2" in line:
                    new_kickstart.write(line.replace("$NIC2", "%s" % second_interface))                    
                elif "NTP=" in line:
                    new_kickstart.write(line.replace("NTP=", "NTP='%s'" % ntp))
                elif "DNS=" in line:
                    new_kickstart.write(line.replace("DNS=", "DNS='%s'" % dns))
                else:
                    new_kickstart.write(line)

        new_kickstart.close()
        kickstart.close()

        sub = subprocess.Popen(["mv", "-f", '//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg' % dir, "//Jenkins//tmp_ISO//ISO_Folders//%s//ks.cfg.install_on_sda_bios" % dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Generate ISO File")
        subprocess.check_call(['/Jenkins/Scripts/bashScripts/generateISO.sh', '/Jenkins/tmp_ISO/ISO_Folders/%s' % dir, "RHEL-7.5 Server.x86_64", '%s.iso' % hn, "RHEL"])

subprocess.check_call(['/Jenkins/Scripts/bashScripts/mountISO.sh', '%s.iso' % hn, iDrac_Server])
