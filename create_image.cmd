wsl -u root -d Ubuntu -e mkdir -p /mnt/test
wsl -u root -d Ubuntu -e mount "/mnt/c/Users/admin/Desktop/Automated Configuration/ISO Files/RHEL-7.6_2019-11-25_11-41-11.iso" /mnt/test
wsl -u root -d Ubuntu -e if [ ! -d "/mnt/test_copy" ]; then rsync -zhr --info=progress2 /mnt/test/ /mnt/test_copy; fi
wsl -u root -d Ubuntu -e rsync -a "/mnt/c/Users/admin/Desktop/ks.cfg.install_on_sda_bios" /mnt/test_copy/

wsl -u root -d Ubuntu -e mkisofs -o /mnt/test.iso -b isolinux/isolinux.bin -J -R -l -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e images/efiboot.img -no-emul-boot -graft-points -V "RHEL-7.6 Server.x86_64" /mnt/test_copy/

wsl -u root -d Ubuntu -e cp -f /mnt/test.iso "/mnt/c/Users/admin/Desktop/test.iso"
wsl -u root -d Ubuntu -e umount /mnt/test
pause