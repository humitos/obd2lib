# -*- coding: utf-8 -*-

import serial


def serial_test():
    """Scan for available ports. return a list of serial names"""

    available = []

    for i in range(256):
        try:  # scan standart ttyS*
            s = serial.Serial(i)
            available.append(s.portstr)
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    for i in range(256):
        try:  # scan USB ttyACM
            s = serial.Serial("/dev/ttyACM"+str(i))
            available.append(s.portstr)
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    for i in range(256):
        try:
            s = serial.Serial("/dev/ttyUSB"+str(i))
            available.append((i, s.portstr))
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    for i in range(256):
        try:
            s = serial.Serial("/dev/ttyd"+str(i))
            available.append((i, s.portstr))
            s.close()   # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass

    # TODO: test using /dev/rfcomm* for Bluetooth devices

    return available


def hex_to_bin(var):
    # Same result using Python .format function
    # "{0:04b}".format(int(var, 16))

    h2b = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
        }

    return h2b[var]


def hex_to_int(str):
    # Same result using Python .format function
    # "{0}".format(int('fa', 16))

    i = eval("0x" + str, {}, {})
    return i


def slugify(s):
    return s.replace(' ', '-').lower()
