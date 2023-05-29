#!/usr/bin/python3

import os
import time
import can
import subprocess
import array
import datetime

subprocess.run("python3 /home/pi/OAP-Config/scripts/lcd_to_vga.py", shell=True)

os.system('sudo ip link set can0 type can bitrate 127000')
os.system('sudo ifconfig can0 up')

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')# socketcan_native

while True:
    message = bus.recv()
    if message.arbitration_id == 0x108e0080:
        dy = str(array.array('B', message.data)[0])
        dm = str(array.array('B', message.data)[1])
        dd = str(array.array('B', message.data)[2])
        th = str(int((message.data.hex()[7]+message.data.hex()[8]), 16))
        tm = str(int(int((message.data.hex()[9]+message.data.hex()[10]), 16)/4))
        subprocess.run("sudo timedatectl set-ntp no", shell=True)
        subprocess.run("sudo timedatectl set-time '"+dy+"-"+dm+"-"+dd+" "+th+":"+tm+"'", shell=True)
        subprocess.run("sudo timedatectl set-ntp yes", shell=True)
    if message.arbitration_id == 0x10ae6080 and (array.array('B', message.data)[0] == 0):
        print("jest on")
        subprocess.run("python3 /home/pi/OAP-Config/scripts/lcd_to_hdmi.py", shell=True)
    if message.arbitration_id == 0x10ae6080 and (array.array('B', message.data)[0] == 16):
        print("jest off")
        subprocess.run("python3 /home/pi/OAP-Config/scripts/lcd_to_vga.py", shell=True)
