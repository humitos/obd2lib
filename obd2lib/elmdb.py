# -*- coding: utf-8 -*-


class ELMdb(object):
    def __init__(self):

        self.database = {
            '0100': {
                'description': 'OBD-II Ping/keepalive + Request available PIDs',
                'mnemonic': 'PING'
                },
            '0101': {
                'description': 'Number of Diagnosic Trouble Codes',
                'mnemonic': 'NUM_DTCS'
                },
            '0102': {
                'description': 'DTC Causing Freeze Frame',
                'mnemonic': 'DTCFRZF'
                },
            '0103': {
                'description': 'Fuel System Status',
                'mnemonic': 'FUELSYS'
                },
            '0104': {
                'description': 'Calculated Load Value',
                'mnemonic': 'LOAD_PCT'},
            '0105': {
                'description': 'Coolant Temperature',
                'mnemonic': 'ECT'
                },
            '0106': {
                'description': 'Short Term Fuel Trim',
                'mnemonic': 'SHRTFT1and3'},
            '0107': {
                'description': 'Long Term Fuel Trim',
                'mnemonic': 'LONGFT1and3'},
            '0108': {
                'description': 'Short Term Fuel Trim',
                'mnemonic': 'SHRTFT2and4'
                },
            '0109': {
                'description': 'Long Term Fuel Trim',
                'mnemonic': 'LONGFT2and4'
                },
            '010A': {
                'description': 'Fuel Rail Pressure',
                'mnemonic': 'FRP'
                },
            '010B': {
                'description': 'Intake Manifold Pressure',
                'mnemonic': 'MAP'
                },
            '010C': {
                'description': 'Engine RPM',
                'mnemonic': 'RPM'
                },
            '010D': {
                'description': 'Vehicle Speed',
                'mnemonic': 'VSS'
                },
            '010E': {
                'description': 'Timing Advance',
                'mnemonic': 'SPARKADV'
                },
            '010F': {
                'description': 'Intake Air Temp',
                'mnemonic': 'IAT'
                },
            '0110': {
                'description': 'Air Flow Rate (MAF)',
                'mnemonic': 'MAF'
                },
            '0111': {
                'description': 'Throttle Position',
                'mnemonic': 'TP'},
            '0112': {
                'description': 'Secondary Air Status',
                'mnemonic': 'ATR_STAT'
                },
            '0113': {
                'description': 'Location of O2 sensors',
                'mnemonic': 'O2SLOC'
                },
            '0114': {
                'description': 'O2 Sensor: 1 - 1',
                'mnemonic': 'BNK1SEN1'
                },
            '0115': {
                'description': 'O2 Sensor: 1 - 2',
                'mnemonic': 'BNK1SEN2'
                },
            '0116': {
                'description': 'O2 Sensor: 1 - 3',
                'mnemonic': 'BNK1SEN3'
                },
            '0117': {
                'description': 'O2 Sensor: 1 - 4',
                'mnemonic': 'BNK1SEN4'
                },
            '0118': {
                'description': 'O2 Sensor: 2 - 1',
                'mnemonic': 'BNK2SEN1'
                },
            '0119': {
                'description': 'O2 Sensor: 2 - 2',
                'mnemonic': 'BNK2SEN2'
                },
            '011A': {
                'description': 'O2 Sensor: 2 - 3',
                'mnemonic': 'BNK2SEN3'
                },
            '011B': {
                'description': 'O2 Sensor: 2 - 4',
                'mnemonic': 'BNK2SEN4'
                },
            '011C': {
                'description': 'OBD Designation',
                'mnemonic': 'OBDSUP'
                },
            '011D': {
                'description': 'Location of O2 sensors',
                'mnemonic': 'O2SLOC2'
                },
            '011E': {
                'description': 'Aux input status',
                'mnemonic': 'AUXINPST'
                },
            '011F': {
                'description': 'Time Since Engine Start',
                'mnemonic': 'RUNTM'
                },
            '0121': {
                'description': 'Engine Run with MIL on',
                'mnemonic': 'MIL_DST'
                },
            '012F': {
                'description': 'Fuel Level Input', 'mnemonic': 'FLI'
                },
            '0131': {
                'description': 'Distance since DTCs cleared',
                'mnemonic': 'CLR_DIST'
                },
            '014D': {
                'description': 'Time run by the engine while MIL is activated',
                'mnemonic': 'MIL_TIME'
                },
            '014E': {
                'description': 'Time since DTCs cleared',
                'mnemonic': 'CLR_TIME'
                },
            '0151': {
                'description': 'Type of fuel being utilized',
                'mnemonic': 'FUEL_TYP'},
            '0152': {
                'description': 'Alcohol fuel percentage',
                'mnemonic': 'ALCH_PCT'
                },
            '03': {
                'description': 'Service $03, get stored DTCs',
                'mnemonic': 'GET_STORED_DTCs'
                },
            # '04': {
            #     'description': 'Service $04, clear DTCs',
            #     'mnemonic': 'CLEAR_DTCs'
            #     }
            '07': {
                'description': 'Service $07, get pending DTCs',
                'mnemonic': 'GET_PENDING_DTCs'
                },
            '0901': {
                'description': 'Vehicle id number message count',
                'mnemonic': 'VIN_COUNT'
                },
            '0902': {
                'description': 'Vehicle id number',
                'mnemonic': 'VIN'
                },
            '0903': {
                'description': 'Calibration id message count',
                'mnemonic': 'CALID_COUNT'
                },
            '0904': {
                'description': 'Calibration IDs (SW version ECU)',
                'mnemonic': 'CALID'
                },
            '0905': {
                'description': 'Calibration verification numbers message count',
                'mnemonic': 'CVN_COUNT'
                },
            '0906': {
                'description': 'Calibration Verification Numbers',
                'mnemonic': 'CVN'
                },
            '0909': {
                'description': 'ECU name', 'mnemonic': 'ECUNAME'
                },
            '090A': {
                'description': 'ECU name  message count',
                'mnemonic': 'ECUNAME_COUNT'
                }
            }
