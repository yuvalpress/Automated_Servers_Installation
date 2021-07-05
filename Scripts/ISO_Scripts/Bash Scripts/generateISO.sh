#!/usr/bin/bash

directory=$1
partition=$2
isoFile=$3
os=$4

if [ $os == "VMWARE" ]; then
  echo "$directory"
  mkisofs -relaxed-filenames -J -R -o "/mnt/c/Users/admin/Desktop/Automated Configuration/tmp_ISO_Files/$isoFile" -b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e efiboot.img -no-emul-boot "$directory"
elif [ $os == "RHEL" ]; then 
  mkisofs -o "/mnt/c/Users/admin/Desktop/Automated Configuration/tmp_ISO_Files/$isoFile" -b isolinux/isolinux.bin -J -R -l -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e images/efiboot.img -no-emul-boot -graft-points -V "$partition" "$directory"
fi