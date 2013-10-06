# -*- coding: utf-8 -*-

import re
import sys
import logging
import argparse

from obd2lib.elmdecoder import decode_answer
from obd2lib.obdconnector import OBDConnector

MSG_WARNING = '''\
WARNING: You are enabling EXPERT mode!

It allows to perform any OBD command against Electronic Control Units.
May lead to harm in your car if not used wisely. Do you wish to \
proceed? (Y/N) '''

MSG_DISCLAIMER = '''\
*** DISCLAIMER: There is absolutely no warranty for any action \
performed by the user from here on ***
'''


class ExpertMode(object):

    def __init__(self, port, baudrate, reconnattempts, sertimeout, lazy_mode):
        self.connector = None
        self.keep_going = True

        self.port = port
        self.baudrate = baudrate
        self.reconnattempts = reconnattempts
        self.sertimeout = sertimeout

        self.lazy_mode = lazy_mode

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

        logging.info(' > Launching Expert Mode console...')
        choice = ''
        valid_answers = ['Y', 'N']
        while choice not in valid_answers:
            choice = raw_input(MSG_WARNING)
        if choice.upper() == 'Y':
            logging.warning(MSG_DISCLAIMER)
            print('Type "quit" or CTRL-C to exit')

            while self.keep_going is True:
                try:
                    user_command = raw_input('ROOT@KT-OBD> ').upper()
                    if re.search('\AAT', user_command):
                        print('Wrong command, ELM configuration is not '
                              'allowed')
                    elif re.search('QUIT', user_command):
                        raise KeyboardInterrupt
                    elif user_command == '':
                        pass
                    else:
                        result, validation = self.connector.run_OBD_command(
                            user_command, expert=True)

                        if re.search('ERROR', result) or \
                                re.search('DATA', result):
                            print('ERROR: Wrong command or not supported, '
                                  'type another one')
                        elif re.search('BUSY', result):
                            print('ERROR: Bus busy, try again')
                        elif re.search('UNABLE', result):
                            print('ERROR: Communication lost, shutting '
                                  'down app!')
                            break
                        else:
                            if self.lazy_mode:
                                value, unit = decode_answer(
                                    user_command, result)
                                print('{0} {1}'.format(value, unit))
                            else:
                                print(result)
                except KeyboardInterrupt:
                        break
        logging.info(' >>> Expert mode aborted by user, finishing...')
        self.connector.run_OBD_command('END', expert=True)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Connect to OBDII interface in an '
        'interactive console (Expert Mode)')
    parser.add_argument(
        '-p', '--port',
        help='port to connect (default: /dev/ttyUSB0)',
        default='/dev/ttyUSB0')
    parser.add_argument(
        '-b', '--baudrate', type=int,
        help='baudrate used to connect to the port (default: 38400)',
        default=38400)
    parser.add_argument('-a', '--reconnattempts', type=int, default=10,
                        help='connection attempts (default: 10)')
    parser.add_argument(
        '-t', '--sertimeout', type=int,
        help='timeout for the connection to the port (default: 10)',
        default=10)
    parser.add_argument(
        '--lazy-mode', action='store_true',
        help='convert the answer into a human-readable way')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show logging.DEBUG into stdout')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.DEBUG)

    expert_mode = ExpertMode(args.port, args.baudrate,
                             args.reconnattempts, args.sertimeout,
                             args.lazy_mode)
    expert_mode.connect()
    expert_mode.run()
