# -*- coding: utf-8 -*-

import sys
import csv
import time
import json
import logging
import argparse
import requests

from obd2lib.elmdb import ELMdb
from obd2lib.obdconnector import OBDConnector


class CollectData(object):

    def __init__(self, port, baudrate, reconnattempts,
                 sertimeout, logfile, commands,
                 command_attempts, interval, server):

        self.commands = commands
        self.command_attempts = command_attempts
        self.invalid_commands = {}
        self.logfile = logfile
        self.keep_going = True
        self.connector = None
        self.interval = interval
        self.server = server
        self.server_post_url = 'http://127.0.0.1:5000/post'

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

    def collect(self):
        if self.connector is None:
            logging.error('You should connect to the port first.')
            sys.exit(1)
        for i, command in enumerate(self.commands):
            if command in self.invalid_commands and \
                    self.invalid_commands[command] == self.command_attempts:
                logging.info(' > Skipping command "{0}" ({1}/{2})...'
                             .format(command, i, len(self.commands)))
                continue

            logging.info(' > Excecuting command "{0}" ({1}/{2})...'
                         .format(command, i, len(self.commands)))
            answer, valid = self.connector.run_OBD_command(command)
            timestamp = time.time()
            if valid == 'N':
                # do not call this command again after
                # "self.command_attempt" times
                if command in self.invalid_commands:
                    self.invalid_commands[command] += 1
                else:
                    self.invalid_commands[command] = 1

            with open(self.logfile, 'ab') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                row = (command, answer, valid, timestamp)
                writer.writerow(row)

            if self.server and command in ['0105', '010C', '010E']:
                data = json.dumps({
                        'answer': answer,
                        'command': command,
                        'timestamp': timestamp,
                        })
                requests.post(url=self.server_post_url, data=data)

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

    parser = argparse.ArgumentParser(
        description='Collect data periodically from the car using OBDII '
        'interface')
    parser.add_argument(
        '-p', '--port',
        help='port to connect (default: /dev/ttyUSB0)',
        default='/dev/ttyUSB0')
    parser.add_argument(
        '-b', '--baudrate', type=int,
        help='baudrate used to connect to the port (default: 38400)',
        default=38400)
    parser.add_argument('-i', '--interval', type=int, default=1,
                        help='interval between queries (default: 1)')
    parser.add_argument('-a', '--attempts', type=int, default=10,
                        help='connection attempts (default: 10)')
    parser.add_argument('-c', '--command-attempts', type=int, default=3,
                        help='attempts to try an invalid command (default: 3)')
    parser.add_argument(
        '-t', '--timeout', type=int,
        help='timeout for the connection to the port (default: 10)',
        default=10)
    parser.add_argument(
        '-s', '--server',
        help='post values to obd2lib server',
        action='store_true')
    parser.add_argument(
        '-v', '--verbose', action="store_true",
        help='show logging.DEBUG into stdout')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
            level=logging.DEBUG)

    logfile = time.strftime('%Y%m%d-%H%M%S-obd-data.log')
    commands = ELMdb.keys()

    collect = CollectData(
        args.port, args.baudrate, args.attempts, args.timeout,
        logfile, commands, args.command_attempts, args.interval,
        args.server)
    collect.connect()
    collect.run()
