# -*- coding: utf-8 -*-

import re
import string
import binascii

import utils


def extract_payload(cmd, answer):
    # Delete headers and checksum. Rework for multiple response messages
    test_pattern = answer.replace(' ', '')
    if cmd == '04' and re.search('44', test_pattern):
        return '44'
    valid_code_answer = '4' + cmd[1:]
    index = string.find(test_pattern, valid_code_answer)
    position = index + len(valid_code_answer)
    return test_pattern[position:-2]


def decode_dtc(frame):
    if frame == '0000' or len(frame) != 4:
        return None
    else:
        description = {
            '00': 'P',
            '01': 'C',
            '10': 'B',
            '11': 'U'
        }
        nibble = frame[0]
        pre_symbol = utils.hex_to_bin(nibble)
        symbol = description[pre_symbol[0:2]]
        first_char = hex(int(pre_symbol[2:], 2))[2:]
        return symbol + first_char + frame[1:]


def decode_answer(cmd, answer):
    # TODO: migrate all of these functions to "elmdb.py" dictionary
    # TODO: use elmdb.ELMdb[cmd]['unit']

    # this will receive only valid answers
    value = None
    unit = None
    payload = extract_payload(cmd, answer)
    if cmd in ['0100', '0120', '0140', '0160', '0180', '01A0', '01C0']:
        value = payload

    elif cmd == '0101':
        mil_state = []
        num_dtcs = []
        supported_tests = []
        while 1:
            if len(payload) >= 8:
                # index = string.find(test_pattern,'4101')
                payload_databyte_1A = payload[0]
                payload_databyte_2A = payload[1]
                code = utils.hex_to_bin(payload_databyte_1A)[0]
                if code:
                    mil_state.append('ON')
                else:
                    mil_state.append('OFF')
                partial1 = str(utils.hex_to_bin(payload_databyte_1A[0]))
                partial2 = str(utils.hex_to_bin(payload_databyte_2A))
                num_dtcs.append(str(int(partial1[1:] + partial2, 2)))
                tests = ''
                for i in range(2, 6):
                    tests = tests + utils.hex_to_bin(payload[i])
                supported_tests.append(tests)
            try:
                # jump ahead checksum and headers of next frame
                payload = payload[16:]
                if payload[0:4] != '4101':   # verify answer of next frame
                    break
                else:
                    payload = payload[4:]
            except IndexError:
                break

        value = [mil_state, num_dtcs, supported_tests]

    elif cmd == '0102':
        value = decode_dtc(payload)

    elif cmd == '0103':
        #OL: open loop. CL: closed loop.
        description = {
            '00000000': 'Wrong state',
            '00000001': 'OL',
            '00000010': 'CL',
            '00000100': 'OL-Drive',
            '00001000': 'OL-Fault',
            '00010000': 'CL-Fault',
            '0010000': 'ISO Reserved',
            '01000000': 'ISO Reserved',
            '10000000': 'ISO Reserved'
        }
        fuel_system1_status = utils.hex_to_bin(payload[0]) + \
            utils.hex_to_bin(payload[1])
        fuel_system2_status = utils.hex_to_bin(payload[2]) + \
            utils.hex_to_bin(payload[3])
        try:
            value = [description[fuel_system1_status],
                     description[fuel_system2_status]]
        except KeyError:
            value = 'Unknown'

    elif cmd in ['0104', '012F', '0152']:
        code = utils.hex_to_int(payload)
        value = code * 100.0 / 255.0
        unit = 'Percent scale'

    elif cmd == '0105' or cmd == '010F':
        code = utils.hex_to_int(payload)
        value = code - 40
        unit = 'Degrees Celsius'

    elif cmd in ['0106', '0107', '0108', '0109']:
        code = utils.hex_to_int(payload)
        value = (code - 128.0) * 100.0 / 128
        unit = 'Percent scale'

    elif cmd == '010A':
        code = utils.hex_to_int(payload)
        value = code * 3
        unit = 'KPa'

    elif cmd == '010B':
        value = utils.hex_to_int(payload)
        unit = 'KPa'

    elif cmd == '010C':
        code = utils.hex_to_int(payload)
        value = code / 4
        unit = 'RPM'

    elif cmd == '010D':
        value = utils.hex_to_int(payload)
        unit = 'Km/h'

    elif cmd == '010E':
        code = utils.hex_to_int(payload)
        value = (code - 128) / 2.0
        unit = 'Degrees'

    elif cmd == '0110':
        code = utils.hex_to_int(payload)
        value = code * 0.01
        unit = 'g/s'

    elif cmd == '0111':
        code = utils.hex_to_int(payload)
        value = code * 0.01
        unit = 'Percent scale'

    elif cmd == '0112':
        description = {
            '00000000': 'Wrong state',
            '00000001': 'UPS',
            '00000010': 'DNS',
            '00000100': 'OFF',
            '00001000': 'ISO Reserved',
            '00010000': 'ISO Reserved',
            '0010000': 'ISO Reserved',
            '01000000': 'ISO Reserved',
            '10000000': 'ISO Reserved'
        }
        air_status = utils.hex_to_bin(payload[0]) + \
            utils.hex_to_bin(payload[1])
        try:
            value = description[air_status]
        except KeyError:
            value = 'Unknown'

    elif cmd in ['0113', '011D']:
        value = utils.hex_to_bin(payload[0]) + utils.hex_to_bin(payload[1])

    elif cmd in ['0114', '0115', '0116', '0117', '0118', '0119',
                 '011A', '011B']:
        code = utils.hex_to_int(payload[0:2])
        voltage = code * 0.005
        code2 = utils.hex_to_int(payload[2:4])
        stft = (code2 - 128.0) * 100.0 / 128
        value = [voltage, stft]
        unit = ['V', 'Percent scale']

    elif cmd == '011C':
        description = {
            '01': 'OBD-II',
            '02': 'OBD',
            '03': 'OBD and OBD-II',
            '04': 'OBD-I',
            '05': 'NO OBD',
            '06': 'EOBD',
            '07': 'EOBD and OBD-II',
            '08': 'EOBD and OBD',
            '09': 'EOBD, OBD and OBD-II',
            '0A': 'JOBD',
            '0B': 'JOBD and OBD-II',
            '0C': 'JOBD and OBD',
            '0D': 'JOBD, EOBD and OBD-II',
            '0E': 'EURO IV B1',
            '0F': 'EURO V B2',
            '10': 'EURO C',
            '11': 'EMD'
        }
        try:
            value = description[payload]
        except KeyError:
            value = 'Unknown'

    elif cmd == '011E':
        code = utils.hex_to_bin(payload[1])[3]
        if code:
            value = 'ON'
        else:
            value = 'OFF'

    elif cmd == '011F':
        code = utils.hex_to_int(payload)
        value = code / 60
        unit = 'min'

    elif cmd in ['0121', '0131']:
        value = utils.hex_to_int(payload)
        unit = 'Km'

    elif cmd in ['014D', '014E']:
        value = utils.hex_to_int(payload)
        unit = 'min'

    elif cmd == '0151':
        description = {
            '01': 'GAS',
            '02': 'METH',
            '03': 'ETH',
            '04': 'DSL',
            '05': 'LPG',
            '06': 'CNG',
            '07': 'PROP',
            '08': 'ELEC',
            '09': 'BI_GAS',
            '0A': 'BI_METH',
            '0B': 'BI_ETH',
            '0C': 'BI_LPG',
            '0D': 'BI_CNG',
            '0E': 'BI_PROP',
            '0F': 'BI_ELEC',
        }
        try:
            value = description[payload]
        except KeyError:
            value = 'Unknown'

    elif cmd in ['0901', '0903', '0905', '0909']:
        value = utils.hex_to_int(payload)
        unit = 'Messages'

    elif cmd in ['0902', '0904', '0906', '090A']:
        matrix = []
        while 1:
            # if there is a compliant frame of response
            if len(payload) >= 9:
                index = utils.hex_to_int(payload[0:2])
                frame = binascii.unhexlify(payload[2:10])
                matrix.append([index, frame])
            else:
                break
            try:
                # jump ahead checksum and headers of next frame
                payload = payload[18:]
                # verify answer of next frame
                if payload[0:4] not in ['4902', '4904', '4906', '490A']:
                    break
                else:
                    payload = payload[4:]
            except IndexError:
                break

        # now, order the values gotten
        if len(matrix) > 0:
            value = ''
            for i in range(len(matrix)):
                if matrix[i][0] == i:
                    value = value + matrix[i][1]

    elif cmd in ['03', '07']:
        value = []
        while 1:
            # if there is a compliant frame of dtcs
            if len(payload) >= 12:
                k = 0
                while k != 12:
                    value_k = decode_dtc(payload[k:k+4])
                    if value_k is not None:
                        value.append(value_k)
                    k += 4
            else:
                break
            try:
                # jump ahead checksum and headers of next frame
                payload = payload[20:]
                # verify answer of next frame
                if payload[0:2] not in ['43', '47']:
                    break
                else:
                    payload = payload[2:]
            except IndexError:
                break

    elif cmd == '04':
        if payload == '44':
            value = True
        else:
            value = False
    return value, unit
