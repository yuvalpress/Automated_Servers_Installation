@echo off

wsl wslpath -a %1 > "c:\users\admin\Desktop\Automated Configuration\path.txt"
wsl -u root -e python3 "/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/edit_path_to_excel.py" &
SET /p p=<"c:\users\admin\Desktop\Automated Configuration\new_path.txt"
wsl -u root -e python3 "/mnt/c/Users/admin/Desktop/Automated Configuration/Scripts/ISO_Scripts/call_ISO_creation.py" "%p%" &