from .iDrac_Configuration import iDracObjectSummon
from .iDrac_Configuration import ping
import asyncio


def create_Raid(idracs):
    # Raid sections
    pingable_iDracs = []
    for iDrac in idracs:
        if ping(iDrac.ip):
            pingable_iDracs.append(iDrac)

    # Run all raids creation in async mode
    asyncio.run(iDracObjectSummon(pingable_iDracs))


def do_raids(idracs):
    create_Raid(idracs)
