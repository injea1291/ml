import subprocess
import win32con
import win32api
import time

# find all devices command
Find_command = 'C:/Windows/SysWOW64/devcon.exe find *'

#list HW ids of devices
hwIds_command = 'C:/devcon.exe hwids *'

#Enable
Enable_command = 'C:/devcon.exe enable *PID_003D'

#Disable
Disable_command = 'C:/devcon.exe disable *PID_003E'

#Find Device
Find_SpecificDevice_command = 'C:/devcon.exe find *PID_003E&MI_00'


a = subprocess.check_output("C:/devcon find @*USB*",shell=True ,stderr=subprocess.STDOUT).split()
print(a)
b = a[a.index('Arduino')-2].split('\\')[1]
c = b[b.find("PID"):b.find("PID")+8]

while True:
    if win32api.GetAsyncKeyState(win32con.VK_F10):
        result = subprocess.check_output(f'C:/devcon.exe disable @*{c}*',shell=True ,stderr=subprocess.STDOUT)
        print(result)
        time.sleep(1)
    elif win32api.GetAsyncKeyState(win32con.VK_F9):
        result = subprocess.check_output(f'C:/devcon.exe enable @*{c}*', shell=True, stderr=subprocess.STDOUT)
        print(result)
        time.sleep(1)
