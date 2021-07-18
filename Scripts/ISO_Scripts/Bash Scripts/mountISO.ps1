$iso=$args[0]
$server=$args[1]

# Making sure there is no ISO file mounted to server $server
racadm -r $server -u root -p password --nocertwarn remoteimage -d

# Attaching ISO file to server $server
racadm -r $server -u root -p password --nocertwarn remoteimage -c -u admin -p Rel7.xPass! -l "/\/\172.29.30.230/\tmp_ISO_Files/\$iso"

# Making iDrac $server to boot once from Virtual Media
racadm -r $server -u root -p password --nocertwarn set iDRAC.VirtualMedia.BootOnce 1

racadm -r $server -u root -p password --nocertwarn set iDRAC.ServerBoot.FirstBootDevice VCD-DVD

# Restarting server for installation to start.
racadm -r $server -u root -p password --nocertwarn serveraction powercycle

