@echo off

wsl wslpath -a "%1" > path.txt
SET /p p=<path.txt
echo %p%
wsl -d Ubuntu -u root -e python3 "/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/call_ISO_creation.py" "%p%"