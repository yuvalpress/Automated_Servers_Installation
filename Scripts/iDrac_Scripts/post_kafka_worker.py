# Script for configuring second raid for kafka server after installation and turning
# the physical disks of worker server to non raid disks

import xlrd
import asyncio
from time import sleep
from Scripts.iDrac_Scripts import iDrac_Configuration as idrac_stracture


async def post_async(iDrac, os):
    if os["server_type"] == "Kafka":
        await iDrac.iDrac_Raids()
        await asyncio.sleep(1)

    elif os["server_type"] == "Worker":
        await iDrac.set_Worker_pdisks()
        await asyncio.sleep(1)


async def summon_post_async(iDracsList, os_list):
    await asyncio.gather(*[post_async(x, y) for x, y in zip(iDracsList, os_list)])


async def post(excel_file):
    try:
        iDracs = idrac_stracture.readExcel(excel_file).read()
        idracs_list = []

        # Creating iDrac list for workers and kafka
        for server in iDracs:
            # Create iDrac object
            if server["server_type"] == "Kafka" or server["server_type"] == "Worker":
                iDrac = idrac_stracture.iDracConf(server["name"], server["tmp_ip"], server["ip_address"],
                                                  server["subnet"],
                                                  server["gateway"],
                                                  server["timezone"], server["vconsole"], server["boot_mode"],
                                                  server["vdisks"],
                                                  server["pdisks"], server["IP_Check"], server["Raid1_Check"],
                                                  server["Raid2_Check"])
                idracs_list.append(iDrac)

        # Creating list for os of workers and kafka
        wb = xlrd.open_workbook(excel_file)
        sheet = wb.sheet_by_name("Server_Configuration")
        os_data = []
        for i in range(6, sheet.nrows, +1):
            if "1" in str(sheet.cell_value(i, 1)):
                print("OS: ", sheet.cell_value(i, 4))
                if "Kafka" in sheet.cell_value(i, 4) or "Worker" in sheet.cell_value(i, 4):
                    os = {"hostname": sheet.cell_value(i, 6), "server_type": sheet.cell_value(i, 4),
                          "os_ip": sheet.cell_value(i, 24)}

                    # Append all os data
                    os_data.append(os)

        print("Waiting for the following servers to be reachable for further configuration:")
        for os, idrac in zip(os_data, iDracs):
            print("Server {} of type {} with the following management address: {}".format(os["hostname"],
                                                                                          idrac["server_type"],
                                                                                          os["os_ip"]))

        # waiting for ping loop
        for server, iDrac in zip(os_data, idracs_list):
            while not idrac_stracture.ping(server["os_ip"]):
                sleep(30)
                print("Waiting for server {} to be reachable..".format(iDrac.name))
            print("Server {} is now reachable!".format(iDrac.name))

        print("Starting iDrac post configuration..")
        sleep(90)  # waiting for server to fully boot

        # start post installation raid and physical disks configuration in async way
        await summon_post_async(idracs_list, os_data)

    except Exception as err:
        print("Failed with the following error: ", err)
