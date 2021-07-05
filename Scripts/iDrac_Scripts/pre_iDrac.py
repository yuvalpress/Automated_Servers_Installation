import xlrd
import subprocess

import asyncio

import sys

from .iDrac_Configuration import ping


async def allReady(iDrac):
    await iDrac.raidReady()
    await asyncio.sleep(1)


async def iDracObjectSummon(iDracsList):
    await asyncio.gather(*[allReady(x) for x in iDracsList])


class colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    OKBLUE = '\033[96m'
    OKPURPLE = '\033[95m'
    ENDC = '\033[0m'


class readExcel:
    def __init__(self, excel_file):
        self.excelFile = excel_file

    def read(self):
        wb = xlrd.open_workbook(self.excelFile)
        sheet = wb.sheet_by_name("Server_Configuration")
        iDrac_Data = []
        for i in range(6, sheet.nrows, +1):
            if "1" in str(sheet.cell_value(i, 1)):
                iDrac = {"tmp_ip": sheet.cell_value(i, 8), "ip_address": sheet.cell_value(i, 9),
                         "subnet": sheet.cell_value(i, 10), "gateway": sheet.cell_value(i, 11),
                         "name": sheet.cell_value(i, 6), "vconsole": sheet.cell_value(i, 13),
                         "timezone": sheet.cell_value(i, 14), "boot_mode": sheet.cell_value(i, 12),
                         "vdisks": [sheet.cell_value(i, 16), sheet.cell_value(i, 18)],
                         "pdisks": [sheet.cell_value(i, 17), sheet.cell_value(i, 19)],
                         "IP_Check": sheet.cell_value(i, 20), "Raid1_Check": sheet.cell_value(i, 21),
                         "Raid2_Check": sheet.cell_value(i, 22)}

                # Append all iDrac data
                iDrac_Data.append(iDrac)

        return iDrac_Data


class raidData:
    def __init__(self, ip):
        self.ip = ip

    def getControllers(self):
        try:
            sub = subprocess.Popen(
                ["powershell", "& racadm -r {} -u root -p password storage get controllers".format(self.ip)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = sub.stdout.readlines()
            for r in output:
                if "RAID.Integrated" in str(r).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", ""):
                    controller = str(r).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "")

            return controller

        except Exception as err:
            print(err)
            return None


class iDrac_Pre:
    def __init__(self, name, tmp_ip, ip, subnet, gateway, timezone, vconsole, boot_mode, raids, pdisks, ip_check,
                 raid1_check, raid2_check):
        self.name = name
        self.tmp_ip = tmp_ip
        self.ip = ip
        self.subnet = subnet
        self.gateway = gateway
        self.timezone = timezone
        self.vconsole = vconsole
        self.boot_mode = boot_mode
        self.raids = raids
        self.pdisks = pdisks
        self.ip_check = ip_check
        self.raid1_check = raid1_check
        self.raid2_check = raid2_check

    def powerUp(self):
        if ping(self.tmp_ip):
            sub = subprocess.Popen(["powershell",
                                    "& racadm -r {} -u root -p password --nocertwarn serveraction powerup".format(
                                        self.tmp_ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            isSuccess = sub.stdout.readlines()
            if "successfully" in str(isSuccess).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", ""):
                print(colors.OKGREEN + "{} PowerUp was Successfull".format(self.name) + colors.ENDC)
            elif "already" in str(isSuccess).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", ""):
                print(colors.OKPURPLE + "{} already in PowerUp state".format(self.name) + colors.ENDC)
            else:
                print(colors.FAIL + "{} PowerUp was not Successfull".format(self.name) + colors.ENDC)

            print("\r")

    async def raidReady(self):
        if ping(self.tmp_ip):
            if self.raid1_check == 1 or self.raid2_check == 1:
                controller = raidData(self.tmp_ip).getControllers()
                # get all disks names and states
                sub = subprocess.Popen(["powershell",
                                        "& racadm -r {} -u root -p password --nocertwarn storage get pdisks -o -p state".format(
                                            self.tmp_ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = sub.stdout.readlines()

                # collect all disks in "Ready" state
                all_non_ready = []
                for disk, state in zip(range(0, len(output), +2), range(1, len(output), +2)):
                    if "Online" not in str(output[state]) and "Ready" not in str(output[state]):
                        all_non_ready.append(str(output[disk]).replace(" ", "").replace("\\r\\n", "").strip("b'"))
                        sub = subprocess.Popen(["powershell",
                                                "& racadm -r {} -u root -p password --nocertwarn storage converttoraid:{}".format(
                                                    self.tmp_ip,
                                                    str(output[disk]).replace(" ", "").replace("\\r\\n", "").strip(
                                                        "b'"))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if len(all_non_ready) != 0:
                    sub = subprocess.Popen(["powershell",
                                            "& racadm -r {} -u root -p password --nocertwarn jobqueue create {} --realtime".format(
                                                self.tmp_ip, controller)], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                    output = sub.stdout.readlines()
                    line = str(output[2]).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "")

                    JID = line.split("=")[1]
                    print("Job has been initiated succesfully on server {}".format(self.tmp_ip))
                    print("Process JID:", JID)

                    if len(sub.stderr.readlines()) == 0:
                        trueUntil = True
                        while trueUntil:
                            # Run until job is done
                            sub = subprocess.Popen(["powershell",
                                                    "& racadm -r {} -u root -p password --nocertwarn jobqueue view -i {}".format(
                                                        self.tmp_ip, JID)], stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
                            lines = sub.stdout.readlines()
                            line3 = str(lines[3]).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "")
                            line7 = str(lines[7]).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "")

                            await asyncio.sleep(1)
                            if "100" in line7 and "Completed" in line3:
                                print(colors.OKGREEN + "All disks are now in Ready state on server {}".format(
                                    self.name) + colors.ENDC)
                                trueUntil = False

                            elif "100" in line7 and "Failed" in line3:
                                print(colors.FAIL + "Failed to turn disks on server {} to Ready state".format(
                                    self.name) + colors.ENDC)
                                trueUntil = False

                else:
                    print(colors.OKPURPLE + "No disks to turn to Ready state." + colors.ENDC)

            else:
                print(colors.OKBLUE + "No disks to turn to Ready state" + colors.ENDC)

    def getPdisksInfo(self):
        if ping(self.tmp_ip):
            print(colors.OKBLUE + "Disk Name             Disk Size" + colors.ENDC)
            print("---------             ---------")
            sub = subprocess.Popen(["powershell",
                                    "& racadm -r {} -u root -p password --nocertwarn storage get pdisks -o -p name,size".format(
                                        self.tmp_ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = sub.stdout.readlines()
            diskInfoDict = {}
            for diskName, diskSize in zip(range(1, len(output), +3), range(2, len(output), +3)):
                size = \
                    str(output[diskSize]).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "").split(
                        "=")[
                        1]
                name = \
                    str(output[diskName]).strip("b'").replace("\\r\\n", "").replace(" ", "").replace("\\r", "").split(
                        "=")[
                        1]
                name = name[:8] + " " + name[8:12] + " " + name[12:]
                space = 22 - len(name)
                print(name + " " * space + size)
                diskInfoDict[name] = size

            print("\r")

            sizeAndNames = {}
            for key, item in diskInfoDict.items():
                if item not in sizeAndNames:
                    sizeAndNames[item] = [key]
                else:
                    sizeAndNames[item].append(key)

            print(colors.OKBLUE + "Size of disks     " + "Amount of disks     " + "Total size" + colors.ENDC)
            print("-------------     ---------------     ----------")
            for key, item in sizeAndNames.items():
                space1 = 18 - len(key)
                space2 = 20 - len(str(len(item)))
                print(str(key) + " " * space1 + str(len(item)) + " " * space2 + str(len(item) * float(key[:-2])))

            print("\r")


def do_pre(ex):
    # Get all servers details
    excel_data = readExcel(ex).read()

    # Set all servers to powerup state and all servers disks to Raid Ready state.
    allIdracs = []
    for iDrac_server in excel_data:
        print("====================Starting iDrac Prerequisite process for server {}====================".format(
            iDrac_server["name"]))
        iDrac = iDrac_Pre(iDrac_server["name"], iDrac_server["tmp_ip"], iDrac_server["ip_address"],
                          iDrac_server["subnet"], iDrac_server["gateway"],
                          iDrac_server["timezone"],
                          iDrac_server["vconsole"], iDrac_server["boot_mode"], iDrac_server["vdisks"],
                          iDrac_server["pdisks"],
                          iDrac_server["IP_Check"], iDrac_server["Raid1_Check"], iDrac_server["Raid2_Check"])

        allIdracs.append(iDrac)

        # Power Up server
        iDrac.powerUp()

        # get disks info
        iDrac.getPdisksInfo()

    # Turn all disks into Ready state
    asyncio.run(iDracObjectSummon(allIdracs))
