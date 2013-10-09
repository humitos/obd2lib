# -*- coding: utf-8 -*-

import sys
import logging

from obd2lib.utils import hex_to_bin
from obd2lib.elmdb import ELMdb
from obd2lib.elmdecoder import decode_answer
from obd2lib.obdconnector import OBDConnector


# TODO:
# - Car's name
# - VIN (http://en.wikipedia.org/wiki/Vehicle_Identification_Number)
# - ECU name


class Info(object):

    def __init__(self, port, baudrate, reconnattempts, sertimeout, lazy):
        self.connector = None

        self.port = port
        self.baudrate = baudrate
        self.reconnattempts = reconnattempts
        self.sertimeout = sertimeout
        self.lazy = lazy

        self.commands = [
            '0100',  # PIDs supported [01 - 20]  n: 0
            '0120',  # PIDs supported [21 - 40]  n: 20
            '0140',  # PIDs supported [41 - 60]  n: 40
            '0160',  # PIDs supported [61 - 80]  n: 60
            '0180',  # PIDs supported [81 - A0]  n: 80
            '01A0',  # PIDs supported [A1 - C0]  n: A0
            '01C0',  # PIDs supported [C1 - E0]  n: C0
            '050100',  # OBD Monitor IDs supported ($01 – $20)
            '0900',  # mode 9 supported PIDs 01 to 20  n: 0
            ]

    def add_hex(self, n1, n2):
        integer = int('0x' + n1, 16) + int('0x' + n2, 16)
        hexa = hex(integer).upper()[2:]
        return hexa

    def supported_pids(self, answer, command):
        n = command[2:]
        mode = command[:2]

        hexa = ''
        for s in answer:
            hexa += hex_to_bin(s)

        pids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                'B', 'C', 'D', 'E', 'F', '10', '11', '12', '13', '14',
                '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E',
                '1F', '20']

        supported_pids = []
        for i, bit in enumerate(hexa):
            if bit == '1':
                pid = self.add_hex(n, pids[i])
                if len(pid) == 1:
                    pid = '0' + pid
                supported_pids.append(mode + pid)

        return supported_pids

    def connect(self):
        self.connector = OBDConnector(
            self.port, self.baudrate, self.reconnattempts, self.sertimeout)
        logging.info('Connecting...')
        success = self.connector.initCommunication()
        if success != 1:
            logging.error('Connection error...')
            sys.exit(1)
        logging.info('Connected')

    def run(self):
        if self.connector is None:
            logging.error('You should connect to the port first.')
            sys.exit(1)

        supported_pids = []

        print('INFORMATION FETCHED FROM THE CAR')
        print('--------------------------------\n\n')

        # check which commands are supported by this car
        for command in self.commands:
            result, validation = self.connector.run_OBD_command(command)
            if validation == 'Y':
                value, unit = decode_answer(command, result)
                supported_pids += self.supported_pids(value, command)

        # use the supported commands to get some info
        for command in supported_pids:
            result, validation = self.connector.run_OBD_command(command)
            if validation == 'Y':
                if self.lazy:
                    value, unit = decode_answer(command, result)
                    print('Command: {0}\nDescription: {1}\nValue: {2}\nUnit: {3}\n\n'
                          .format(command, ELMdb[command]['description'], value, unit))
                else:
                    print('Command: {0}\nResult: {1}'.format(command, result))
            else:
                logging.warning('Something wrong happened with "{0}" command'
                                .format(command))
