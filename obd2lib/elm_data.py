# -*- coding: utf-8 -*-

import re
import time

import carsdb


class ELM_Data(object):
    def __init__(self):

        # record will contain two type of messages:
        # [pid, answer, boolean, time.time()] or
        # [message, info_level, None, time.time()]

        self.record = []
        self.mode = 'unknown'
        self.completed = False

        self.OBD_database = [
            ['PING', '0100'],
            ['OBDSUP', '011C'],
            ['TESTS', '0101'],
            ['MIL', '0101'],
            ['NUM_DTCS', '0101'],
            ['DTCFRZF', '0102'],
            ['FUELSYS', '0103'],
            ['LOAD_PCT', '0104'],
            ['ECT', '0105'],
            ['SHRTFT1and3', '0106'],
            ['LONGFT1and3', '0107'],
            ['SHRTFT2and4', '0108'],
            ['LONGFT2and4', '0109'],
            ['FRP', '010A'],
            ['MAP', '010B'],
            ['RPM', '010C'],
            ['VSS', '010D'],
            ['SPARKADV', '010E'],
            ['IAT', '010F'],
            ['MAF', '0110'],
            ['TP', '0111'],
            ['ATR_STAT', '0112'],
            ['O2SLOC', '0113'],
            ['BNK1SEN1', '0114'],
            ['BNK1SEN2', '0115'],
            ['BNK1SEN3', '0116'],
            ['BNK1SEN4', '0117'],
            ['BNK2SEN1', '0118'],
            ['BNK2SEN2', '0119'],
            ['BNK2SEN3', '011A'],
            ['BNK2SEN4', '011B'],
            ['O2SLOC2', '011D'],
            ['AUXINPST', '011E'],
            ['RUNTM', '011F'],
            ['MIL_DST', '0121'],
            ['FLI', '012F'],
            ['CLR_DIST', '0131'],
            ['MIL_TIME', '014D'],
            ['CLR_TIME', '014E'],
            ['FUEL_TYP', '0151'],
            ['ALCH_PCT', '0152'],
            ['VIN_COUNT', '0901'],
            ['VIN', '0902'],
            ['CALID_COUNT', '0903'],
            ['CALID', '0904'],
            ['CVN_COUNT', '0905'],
            ['CVN', '0906'],
            ['ECUNAME', '0909'],
            ['ECUNAME_COUNT', '090A'],
            ['GET_STORED_DTCs', '03'],
            ['GET_PENDING_DTCs', '07']
            #['CLEAR_DTCs', '04']
        ]

        # self.OBD_description = {
        #     'PING':'0100 --> OBD-II Ping/keepalive + Request available PIDs',
        #     'TESTS':'0101 --> Status Since DTC Cleared',
        #     'MIL':'0101 --> Malfunction Indicator Lamp',
        #     'NUM_DTCS':'0101 --> Number of Diagnosic Trouble Codes',
        #     'DTCFRZF':'0102 --> DTC Causing Freeze Frame',
        #     'FUELSYS':'0103 --> Fuel System Status',
        #     'LOAD_PCT':'0104 --> Calculated Load Value',
        #     'ECT':'0105 --> Coolant Temperature',
        #     'SHRTFT1and3':'0106 --> Short Term Fuel Trim',
        #     'LONGFT1and3':'0107 --> Long Term Fuel Trim',
        #     'SHRTFT2and4':'0108 --> Short Term Fuel Trim',
        #     'LONGFT2and4':'0109 --> Long Term Fuel Trim',
        #     'FRP':'010A --> Fuel Rail Pressure',
        #     'MAP':'010B --> Intake Manifold Pressure',
        #     'RPM':'010C --> Engine RPM',
        #     'VSS':'010D --> Vehicle Speed',
        #     'SPARKADV':'010E --> Timing Advance',
        #     'IAT':'010F --> Intake Air Temp',
        #     'MAF':'0110 --> Air Flow Rate (MAF)',
        #     'TP':'0111 --> Throttle Position',
        #     'ATR_STAT':'0112 --> Secondary Air Status',
        #     'O2SLOC':'0113 --> Location of O2 sensors',
        #     'BNK1SEN1':'0114 --> O2 Sensor: 1 - 1',
        #     'BNK1SEN2':'0115 --> O2 Sensor: 1 - 2',
        #     'BNK1SEN3':'0116 --> O2 Sensor: 1 - 3',
        #     'BNK1SEN4':'0117 --> O2 Sensor: 1 - 4',
        #     'BNK2SEN1':'0118 --> O2 Sensor: 2 - 1',
        #     'BNK2SEN2':'0119 --> O2 Sensor: 2 - 2',
        #     'BNK2SEN3':'011A --> O2 Sensor: 2 - 3',
        #     'BNK2SEN4':'011B --> O2 Sensor: 2 - 4',
        #     'OBDSUP':'011C --> OBD Designation',
        #     'O2SLOC2':'011D --> Location of O2 sensors',
        #     'AUXINPST':'011E --> Aux input status',
        #     'RUNTM':'011F --> Time Since Engine Start',
        #     'MIL_DST':'0121 --> Engine Run with MIL on',
        #     'FLI':'012F --> Fuel Level Input',
        #     'CLR_DIST':'0131 --> Distance since DTCs cleared',
        #     'MIL_TIME':'014D --> Time run by the engine while MIL is activated',
        #     'CLR_TIME':'014E --> Time since DTCs cleared',
        #     'FUEL_TYP':'0151 --> Type of fuel being utilized',
        #     'ALCH_PCT':'0152 --> Alcohol fuel percentage',
        #     'VIN_COUNT':'0901 --> Vehicle id number message count',
        #     'VIN':'0902 --> Vehicle id number',
        #     'CALID_COUNT':'0903 --> Calibration id message count',
        #     'CALID':'0904 --> Calibration IDs (SW version ECU)',
        #     'CVN_COUNT':'0905 --> Calibration verification numbers message count',
        #     'CVN':'0906 --> Calibration Verification Numbers',
        #     'ECUNAME_COUNT':'0909 --> ECU name  message count',
        #     'ECUNAME':'090A --> ECU name',
        #     'GET_STORED_DTCs':'03 --> Service $03, get stored DTCs',
        #     'GET_PENDING_DTCs':'07 --> Service $07, get pending DTCs',
        #     #'CLEAR_DTCs':'04 --> Service $04, clear DTCs'
        # }

        self.OBD_polling_database = [
            ['ECT', '0105'],
            ['FRP', '010A'],
            ['MAP', '010B'],
            ['RPM', '010C'],
            ['VSS', '010D'],
            ['IAT', '010F'],
            ['MAF', '0110'],
            ['TP', '0111'],
            ['RUNTM', '011F'],
            ['FLI', '012F']
        ]

        self.OBD_polling_description = {
            'ECT': '0105 --> Coolant Temperature',
            'FRP': '010A --> Fuel Rail Pressure',
            'MAP': '010B --> Intake Manifold Pressure',
            'RPM': '010C --> Engine RPM',
            'VSS': '010D --> Vehicle Speed',
            'IAT': '010F --> Intake Air Temp',
            'MAF': '0110 --> Air Flow Rate (MAF)',
            'TP': '0111 --> Throttle Position',
            'RUNTM': '011F --> Time Since Engine Start',
            'FLI': '012F --> Fuel Level Input'
        }

    def GetOBD_DBInfo(self, param='-C'):

        commands = []

        if param == '-C':
            return carsdb.PEUGEOT_206['commands']
        elif param == '-S':
            for i in range(len(self.OBD_polling_database)):
                commands.append(self.OBD_polling_database[i][1])

        return commands

    def do_init(self, mode):
        self.mode = mode

    def do_complete(self):
        self.completed = True

    def test_if_valid(self, pid, answer):
        valid_response = False
        pattern = '4' + pid[1:]
        value_to_test = answer.replace(' ', '')
        if re.search(pattern, value_to_test):
            valid_response = True
        return valid_response

    def set_value(self, pid, answer):
        # Insert parameter validation here before storing

        boolean = self.test_if_valid(pid, answer)
        self.record.append([pid, answer, boolean, time.time()])
        return

    def set_info(self, message, info_level='INFO'):
        # Insert parameter validation here before storing

        self.record.append([message, info_level, None, time.time()])
        return

    def get_value(self, position):
        if len(self.record) >= position:
            return self.record[position]
        else:
            return None
