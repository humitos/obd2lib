import random
import string

def debug(msg):
     pass #print('-- ' + msg)

def sample(var):
    if var == 'VSS':
        self = hex (int(random.randrange(40,90)))[2:].upper()
    elif var == 'RPM':
        self = hex (int(random.randrange(750,4500)))[2:].upper()
    else:
        self = hex (int(random.randrange(0,255)))[2:].upper()
    if len(self)%2 == 1:
        self = '0' + self
    return self

def hex_to_str(x, chars = 1):
    if x == None:
        return ''
    else:
        if bytes == 0:
           mask = '%x'
        else:
           mask = '%0.' + str(chars) + 'x'
        return (mask % x).upper()
##TODO Add unittest
##assertEqual(hex_to_str(0,1), '0')
##assertEqual(hex_to_str(0,2), '00')
##assertEqual(hex_to_str(0xFF,2), 'FF')

import binascii

def calculate_crc(hexstr):
    crc_reg = 0xff
    poly, i, j, checksum = 0, 0, 0, 0

    msg_buf = binascii.unhexlify(hexstr)
    for i in range(0, len(msg_buf)):
        byte_point = ord(msg_buf[i])
        bit_point = 0x80
        for j in range(0,8):
            if bit_point & byte_point:
                if crc_reg & 0x80:
                    poly = 1
                else:
                    poly = 0x1c
                crc_reg = ( (crc_reg << 1) | 1) ^ poly;
            else:
                poly = 0
                if crc_reg & 0x80:
                    poly = 0x1d
                crc_reg= (crc_reg << 1) ^ poly
            bit_point >>= 1
        checksum += byte_point
    checksum = checksum % 256
    checksum_hexstr = hex_to_str(checksum, 2)
    # For SAE ~crc_reg
    return checksum_hexstr.upper()

if __name__ == '__main__':
    # Test calculate_crc
    test = [
        {'m': '486B104100BE3EA811', 'r':'B9'},
        {'m': '486B10412080001000', 'r':'B4'},
    ]
    for t in test:
        print "Testing ",t['m'],
        checksum_hexstr = calculate_crc(t['m'])
        assert t['r'] == checksum_hexstr
        print t['r']," == ", checksum_hexstr," ...OK"
