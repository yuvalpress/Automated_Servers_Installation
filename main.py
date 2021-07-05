import sys
import subprocess

from Scripts.iDrac_Scripts import pre_iDrac as pre
from Scripts.iDrac_Scripts import iDrac_IP_Address as set_ip
from Scripts.iDrac_Scripts import iDrac_Rest_Of_Settings as idrac_settings
from Scripts.iDrac_Scripts import iDrac_Raids as set_raid
from Scripts.iDrac_Scripts import iDrac_Configuration as idrac_stracture
from Scripts.iDrac_Scripts import post_kafka_worker as post_storage


def config(iDracs, ex):
    print("Creating iDrac objects")
    idracs_list = []
    for server in iDracs:
        # Create iDrac object
        iDrac = idrac_stracture.iDracConf(server["name"], server["tmp_ip"], server["ip_address"], server["subnet"],
                                          server["gateway"],
                                          server["timezone"], server["vconsole"], server["boot_mode"], server["vdisks"],
                                          server["pdisks"], server["IP_Check"], server["Raid1_Check"],
                                          server["Raid2_Check"])
        idracs_list.append(iDrac)
    print("Done!\n")
    print("Starting pre stage for all servers..")
    try:
        pre.do_pre(ex)
        print("Done!\n")
    except Exception as err:
        print("Failed with the following error: %s\n" % err)

    print("Starting IP Addresses changing stage..")
    try:
        set_ip.ip(idracs_list)
        print("Done!\n")
    except Exception as err:
        print("Failed with the following error: %s\n" % err)

    print("Starting general settings stage..")
    try:
        idrac_settings.settings(idracs_list)
        print("Done!\n")
    except Exception as err:
        print("Failed with the following error: %s\n" % err)

    print("Starting Raids creation stage..")
    try:
        set_raid.do_raids(idracs_list)
        print("Done!\n")
    except Exception as err:
        print("Failed with the following error: %s\n" % err)

    # print("Creating ISO Costumed images..")
    # try:
    #     print(sys.argv[1])
    #     sub = subprocess.Popen(
    #         ["C:\\Users\\admin\\Desktop\\Automated Configuration\\Scripts\\ISO_Scripts\\call_bash_environment.cmd",
    #          sys.argv[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     print(str(sub.stdout.read()), "\n")
    #     print("error: ", sub.stderr.read())
    #     print("Done!\n")
    # except Exception as err:
    #     print("Failed with the following error: %s\n" % err)

    print("Mounting ISO Costumed images..")
    try:
        for server in idracs_list:
            sub = subprocess.Popen(["powershell",
                                    "& \"C:\\Users\\admin\\Desktop\\Automated "
                                    "Configuration\\Scripts\\ISO_Scripts\\Bash Scripts\\mountISO.ps1\" {}.iso {}".format(
                                        server.name, server.ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(sub.stdout.read(), "\n")
            print("error: ", sub.stderr.read())
            print("Done!\n")
    except Exception as err:
        print("Failed with the following error: %s\n" % err)

    print(
        "Don't close the script window! Making sure Operating Systems were installed successfully and initiating post "
        "installation configuration process.")
    try:
        post_storage.post(ex)
    except Exception as err:
        print("Failed with the following error: ", err)


if __name__ == "__main__":
    print("Analysing Excel file..")
    iDracs = idrac_stracture.readExcel(sys.argv[1]).read()
    print("Done!")
    config(iDracs, sys.argv[1])
