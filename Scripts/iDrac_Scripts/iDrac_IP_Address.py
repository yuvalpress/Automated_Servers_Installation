from .iDrac_Configuration import ping


def change_ip(iDracs):
    for idrac in iDracs:
        idrac.iDrac_IP()

    for idrac in iDracs:
        while not ping(idrac.ip):
            print("Waiting for ping")
        print("Pingable!")


def ip(idracs_list):
    change_ip(idracs_list)
