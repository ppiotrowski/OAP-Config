from smbus2 import SMBus, i2c_msg
from argparse import ArgumentParser
import os
import usb.core
import subprocess

parser = ArgumentParser()

parser.add_argument("-i", "--interface", help =  "Interface number (default = 2)", metavar = "x", type = int, default = 2)
args = parser.parse_args()

bus = SMBus(args.interface)
data = [0x10,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25,0x25]
msg = i2c_msg.write(0x35, data)
bus.i2c_rdwr(msg)
bus.i2c_rdwr(msg)

subprocess.run("uhubctl -l 1-1 -a 1", shell=True)
dev = usb.core.find(idVendor=0x0eef, idProduct=0x0005)
dev.reset()
if not dev.is_kernel_driver_active(0):
    dev.attach_kernel_driver(0)

