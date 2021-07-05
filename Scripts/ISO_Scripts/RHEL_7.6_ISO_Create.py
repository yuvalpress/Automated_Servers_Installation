#!/usr/bin/python3
# Imports
import os
import sys
import subprocess
from shutil import move
import time

def create_iso():
    # Default Values
    # Kickstart Files
    KICKSTART = "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Kickstart/ks.cfg.install_on_sda_bios-single"
    KICKSTART_TEAM = "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Kickstart/ks.cfg.install_on_sda_bios-team"

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

    # dir = str(iDrac_Server) + "_ISO"

    # mount iso to new folder
    # if os.path.isdir("//mnt//%s" % str(iDrac_Server)):
    #     print("Directory already exists..")
    # else:
    #     os.mkdir("//mnt//%s" % str(iDrac_Server))
    #     print("Created mounting directory")

    # start iso modification process
    if "team" not in network:
        print("Executing ISO Modification process with one port network configuration")
        # subprocess.check_call(['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash Scripts/copyISOFiles.sh', KICKSTART, "RHEL7.6"])
        try:
            if os.path.exists('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                              'Content//Mounted_ISO//RHEL7.6//ks.cfg'):
                os.remove('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg')

            new_kickstart = open('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg', 'wt')
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

            move('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg', KICKSTART)

            print("Generate ISO File")
            popen = subprocess.call(
                ['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash '
                                   'Scripts/generateISO.sh',
                                   '/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.6',
                                   "RHEL-7.6 Server.x86_64", '%s.iso' % hn,
                                   "RHEL"])

        except Exception as err:
            print("Failed with the following error: %s" % err)

    else:
        print("Executing ISO Modification process with teaming network configuration")
        # subprocess.check_call(['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash Scripts/copyISOFiles.sh', KICKSTART_TEAM, "RHEL7.6"])
        try:
            if os.path.exists('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                              'Content//Mounted_ISO//RHEL7.6//ks.cfg'):
                os.remove('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg')

            new_kickstart = open('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg', 'wt')
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

            move('//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg', '//mnt//c//Users//admin//Desktop//Automated Configuration//ISO Files '
                          'Content//Mounted_ISO//RHEL7.6//ks.cfg.install_on_sda_bios')

            print("Generate ISO File")
            popen = subprocess.check_call(['/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/Bash '
                                   'Scripts/generateISO.sh',
                                   '/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.6',
                                   "RHEL-7.6 Server.x86_64", '%s.iso' % hn,
                                   "RHEL"])
            # for stdout_line in iter(popen.stdout.readline, ""):
            #     yield str(stdout_line).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "")
            # popen.stdout.close()
            # return_code = popen.wait()
            # if return_code:
            #     raise subprocess.CalledProcessError(return_code, "here")

        except Exception as err:
            print("Failed with the following error: %s" % err)


if __name__ == "__main__":
    create_iso()