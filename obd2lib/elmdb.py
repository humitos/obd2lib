# -*- coding: utf-8 -*-

# Information from Wikipedia
# http://en.wikipedia.org/wiki/OBD-II_PIDs


class ELMdb(object):
    def __init__(self):

        self.database = {
            '0100': {
                'description': 'OBD-II Ping/keepalive + Request available PIDs',
                'mnemonic': 'PING'
                'unit': None,
                },
            '0101': {
                'description': 'Number of Diagnosic Trouble Codes',
                'mnemonic': 'NUM_DTCS'
                'unit': None,
                },
            '0102': {
                'description': 'DTC Causing Freeze Frame',
                'mnemonic': 'DTCFRZF'
                'unit': None,
                },
            '0103': {
                'description': 'Fuel System Status',
                'mnemonic': 'FUELSYS'
                'unit': None,
                },
            '0104': {
                'description': 'Calculated Load Value',
                'mnemonic': 'LOAD_PCT',
                'unit': 'Percent scale',
                }
            '0105': {
                'description': 'Coolant Temperature',
                'mnemonic': 'ECT'
                'unit': 'Degrees Celsius',
                },
            '0106': {
                'description': 'Short Term Fuel Trim',
                'mnemonic': 'SHRTFT1and3',
                'unit': 'Percent scale',
                }
            '0107': {
                'description': 'Long Term Fuel Trim',
                'mnemonic': 'LONGFT1and3',
                'unit': 'Percent scale',
                }
            '0108': {
                'description': 'Short Term Fuel Trim',
                'mnemonic': 'SHRTFT2and4',
                'unit': 'Percent scale',
                },
            '0109': {
                'description': 'Long Term Fuel Trim',
                'mnemonic': 'LONGFT2and4',
                'unit': 'Percent scale',
                },
            '010A': {
                'description': 'Fuel Rail Pressure',
                'mnemonic': 'FRP'
                'unit': 'KPa',
                },
            '010B': {
                'description': 'Intake Manifold Pressure',
                'mnemonic': 'MAP',
                'unit': 'KPa',
                },
            '010C': {
                'description': 'Engine RPM',
                'mnemonic': 'RPM',
                'unit': 'RPM',
                },
            '010D': {
                'description': 'Vehicle Speed',
                'mnemonic': 'VSS',
                'unit': 'Km/h',
                },
            '010E': {
                'description': 'Timing Advance',
                'mnemonic': 'SPARKADV',
                'unit': 'Degrees',
                },
            '010F': {
                'description': 'Intake Air Temp',
                'mnemonic': 'IAT',
                'unit': None,
                },
            '0110': {
                'description': 'Air Flow Rate (MAF)',
                'mnemonic': 'MAF',
                'unit': 'g/s',
                },
            '0111': {
                'description': 'Throttle Position',
                'mnemonic': 'TP',
                'unit': 'Percent scale',
                },
            '0112': {
                'description': 'Secondary Air Status',
                'mnemonic': 'ATR_STAT',
                'unit': None,
                },
            '0113': {
                'description': 'Location of O2 sensors',
                'mnemonic': 'O2SLOC',
                'unit': None,
                },
            '0114': {
                'description': 'O2 Sensor: 1 - 1',
                'mnemonic': 'BNK1SEN1',
                'unit': ['V', 'Percent scale'],
                },
            '0115': {
                'description': 'O2 Sensor: 1 - 2',
                'mnemonic': 'BNK1SEN2',
                'unit': ['V', 'Percent scale'],
                },
            '0116': {
                'description': 'O2 Sensor: 1 - 3',
                'mnemonic': 'BNK1SEN3',
                'unit': ['V', 'Percent scale'],
                },
            '0117': {
                'description': 'O2 Sensor: 1 - 4',
                'mnemonic': 'BNK1SEN4',
                'unit': ['V', 'Percent scale'],
                },
            '0118': {
                'description': 'O2 Sensor: 2 - 1',
                'mnemonic': 'BNK2SEN1',
                'unit': ['V', 'Percent scale'],
                },
            '0119': {
                'description': 'O2 Sensor: 2 - 2',
                'mnemonic': 'BNK2SEN2',
                'unit': ['V', 'Percent scale'],
                },
            '011A': {
                'description': 'O2 Sensor: 2 - 3',
                'mnemonic': 'BNK2SEN3',
                'unit': ['V', 'Percent scale'],
                },
            '011B': {
                'description': 'O2 Sensor: 2 - 4',
                'mnemonic': 'BNK2SEN4',
                'unit': ['V', 'Percent scale'],
                },
            '011C': {
                'description': 'OBD Designation',
                'mnemonic': 'OBDSUP',
                'unit': None,
                },
            '011D': {
                'description': 'Location of O2 sensors',
                'mnemonic': 'O2SLOC2',
                'unit': None,
                },
            '011E': {
                'description': 'Aux input status',
                'mnemonic': 'AUXINPST',
                'unit': None,
                },
            '011F': {
                'description': 'Time Since Engine Start',
                'mnemonic': 'RUNTM',
                'unit': 'min',
                },
            '0121': {
                'description': 'Engine Run with MIL on',
                'mnemonic': 'MIL_DST',
                'unit': 'Km',
                },
            '012F': {
                'description': 'Fuel Level Input',
                'mnemonic': 'FLI',
                },
            '0131': {
                'description': 'Distance since DTCs cleared',
                'mnemonic': 'CLR_DIST',
                'unit': 'Km',
                },
            '014D': {
                'description': 'Time run by the engine while MIL is activated',
                'mnemonic': 'MIL_TIME',
                'unit': 'min',
                },
            '014E': {
                'description': 'Time since DTCs cleared',
                'mnemonic': 'CLR_TIME',
                'unit': 'min',
                },
            '0151': {
                'description': 'Type of fuel being utilized',
                'mnemonic': 'FUEL_TYP',
                'unit': None,
                },
            '0152': {
                'description': 'Alcohol fuel percentage',
                'mnemonic': 'ALCH_PCT',
                'unit': 'Percent scale',
                },
            '03': {
                'description': 'Service $03, get stored DTCs',
                'mnemonic': 'GET_STORED_DTCs',
                'unit': None,
                },
            # '04': {
            #     'description': 'Service $04, clear DTCs',
            #     'mnemonic': 'CLEAR_DTCs',
            #     'unit': '',
            #     }
            '07': {
                'description': 'Service $07, get pending DTCs',
                'mnemonic': 'GET_PENDING_DTCs',
                'unit': None,
                },
            '0901': {
                'description': 'Vehicle id number message count',
                'mnemonic': 'VIN_COUNT',
                'unit': 'Messages',
                },
            '0902': {
                'description': 'Vehicle id number',
                'mnemonic': 'VIN',
                'unit': None,
                },
            '0903': {
                'description': 'Calibration id message count',
                'mnemonic': 'CALID_COUNT',
                'unit': 'Messages',
                },
            '0904': {
                'description': 'Calibration IDs (SW version ECU)',
                'mnemonic': 'CALID',
                'unit': None,
                },
            '0905': {
                'description': 'Calibration verification numbers message count',
                'mnemonic': 'CVN_COUNT',
                'unit': 'Messages',
                },
            '0906': {
                'description': 'Calibration Verification Numbers',
                'mnemonic': 'CVN',
                'unit': None,
                },
            '0909': {
                'description': 'ECU name',
                'mnemonic': 'ECUNAME',
                'unit': 'Messages',
                },
            '090A': {
                'description': 'ECU name  message count',
                'mnemonic': 'ECUNAME_COUNT',
                'unit': None,
                }
            }
