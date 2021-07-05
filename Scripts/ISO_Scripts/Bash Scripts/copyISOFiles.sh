#!/usr/bin/bash

kickstart=$1
os=$2

if [ $os == "RHEL7.6" ]; then
    echo
    echo Copy Kickstart file to /mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.6/
    # shellcheck disable=SC2216
    yes | cp -f "$kickstart" "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.6/ks.cfg.install_on_sda_bios"

elif [ $os == "RHEL7.5" ]; then
    echo
    echo Copy Kickstart file to /mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.5/
    # shellcheck disable=SC2216
    yes | cp -f "$kickstart" "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/RHEL7.5/ks.cfg.install_on_sda_bios"
fi

echo All needed files have been copid to "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files Content/Mounted_ISO/$os/"

