# -*- coding: utf-8 -*-

import sys
import logging

from obd2lib.elmdecoder import decode_answer
from obd2lib.obdconnector import OBDConnector


# TODO:
# - PIDs supported
# - Car's name
# - ELM version
# - VIN (http://en.wikipedia.org/wiki/Vehicle_Identification_Number)
# - ECU name


class Info(object):

    def __init__(self, port, baudrate, reconnattempts, sertimeout, lazy_mode):
        self.connector = None

        self.port = port
        self.baudrate = baudrate
        self.reconnattempts = reconnattempts
        self.sertimeout = sertimeout

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

        results = []

        for command in self.commands:
            command = ''
            result, validation = self.connector.run_OBD_command(command)
            if validation == 'Y':
                value, unit = decode_answer(command, result)
                results.append((value, unit))
