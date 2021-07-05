def change_Settings(iDracs):
    for idrac in iDracs:
        idrac.setName()
        idrac.setTZ()
        idrac.setBootMode()
        idrac.setVconsole()


def settings(iDracs):
    change_Settings(iDracs)
