# -*- coding: utf-8 -*-

import sys
import csv
import time
import logging
# import argparse
import ConfigParser

from obd2lib.elmdb import ELMdb
from obd2lib.obdconnector import OBDConnector


class CollectData(object):

    def __init__(self, logfile, configfile, commands, interval=1):

        self.commands = commands
        self.invalid_commands = []
        self.logfile = logfile
        self.keep_going = True
        self.connector = None
        self.interval = interval

        config = ConfigParser.RawConfigParser()
        config.read(configfile)
        self.comport = config.get('elm', 'comport')
        self.reconnattempts = int(config.get('elm', 'reconnattempts'))
        self.sertimeout = int(config.get('elm', 'sertimeout'))

    def connect(self):
        self.connector = OBDConnector(
            self.comport, self.reconnattempts, self.sertimeout)
        logging.info('Connecting...')
        success = self.connector.initCommunication()
        if success != 1:
            logging.error('Connection error...')
            sys.exit(1)
        logging.info('Connected')

    def collect(self):
        if self.connector is None:
            logging.error('You should connect to the port first.')
            sys.exit(1)
        for i, command in enumerate(self.commands):
            if command in self.invalid_commands:
                logging.info(' > Skipping command "{0}" ({1}/{2})...'
                             .format(command, i, len(self.commands)))
                continue

            logging.info(' > Excecuting command "{0}" ({1}/{2})...'
                         .format(command, i, len(self.commands)))
            answer, valid = self.connector.run_OBD_command(command)

            if valid == 'N':
                # do not call this command again
                self.invalid_commands.append(command)

            with open(self.logfile, 'ab') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                row = (command, answer, valid, time.time())
                writer.writerow(row)

    def disconnect(self):
        self.connector.run_OBD_command('END')
        logging.info('Disconnected')

    def run(self):
        while self.keep_going:
            try:
                self.collect()
                time.sleep(self.interval)
            except KeyboardInterrupt:
                self.keep_going = False
        self.disconnect()


if __name__ == '__main__':
    logfile = time.strftime('%Y%m%d-%H%M%S-obd-data.log')

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(ch)

    configfile = 'config.ini'
    commands = ELMdb.keys()

    collect = CollectData(logfile, configfile, commands)
    collect.connect()
    collect.run()
