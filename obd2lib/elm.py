# -*- coding: utf-8 -*-

import re
import time
import logging
import ConfigParser

import carsdb
from obdconnector import OBDConnector


class Elm(object):
    def __init__(self):

        self.MODES = [
            '-C',
            '-D',
            '-E',
            '-S'
        ]

        self.port = None
        self.keep_going = True
        self.total_steps = 30
        self.current_step = 0

    def do_cancel(self):
        self.keep_going = False

    def create_connection(self):
        # TODO: if there is not response from ECU to atz command, the
        # app remains freezed here
        self.connector = OBDConnector()
        self.serial = self.connector.initCommunication()
        if self.serial != 1:
            logging.error('Connection error...')

    def do_connect(self):
        self.keep_going = True
        logging.info('Creating data structures...')
        logging.info('Connecting...')
        self.create_connection()
        logging.info('Connected')

    def do_disconnect(self):
        logging.info('Disconnecting...')
        time.sleep(0.5)
        logging.info('Disconnected')

    def do_test(self, option):
        if option not in self.MODES:
            logging.error('App mode selected unsupported. Shutting down...')
            raise
        logging.info('Working...')

        self.option = option

        if self.option == '-C':
            self.check_mode(self.connector)
        elif self.option == '-D':
            self.delete_mode(self.connector)
        elif self.option == '-E':
            self.expert_mode(self.connector)
        elif self.option == '-S':
            try:
                self.sampler_mode(self.connector)
            except KeyboardInterrupt:
                logging.info('>>> Polling aborted by user, finishing...')
            self.connector.run_OBD_command('END', self.option)
        logging.info('Work finished')
        return

    def check_mode(self, connector):
        # TODO: ability to select your car from carsdb
        self.commands = carsdb.PEUGEOT_206['commands']

        self.total_steps = len(self.commands)
        current_step = 1
        total = len(self.commands)
        for i in range(len(self.commands)):
            logging.info(' > Getting OBD polling parameter ({0}/{1})...'
                         .format(current_step, total))
            if self.keep_going is False:
                logging.info('Cancelled by user')
                # time.sleep(1)
                return
            # time.sleep(0.1)
            connector.run_OBD_command(self.commands[i], self.option)
            # time.sleep(.1)
            current_step += 1
        connector.run_OBD_command('END', self.option)
        logging.info('Succesfully tested')

    def delete_mode(self, connector):
        logging.info(' > Executing CLEAR status command...')
        SERVICE_CLEAR = '04'
        result, validation = connector.run_OBD_command(
            SERVICE_CLEAR, self.option)
        if validation == 'Y':
            logging.info(' > Done! Try again Check mode to take a new '
                         'snapshot of system status...')
        else:
            logging.info(' > Fail! ECU busy, try again in a few later...')
        connector.run_OBD_command('END', self.option)

    def expert_mode(self, connector):
        logging.info(' > Launching Expert Mode console...')
        choice = ''
        valid_answers = ['Y', 'N']
        while choice not in valid_answers:
            choice = raw_input('WARNING: You are enabling EXPERT mode!\n\
It allows to perform any OBD command against Electronic Control Units.\n\
May lead to harm in your car if not used wisely. Do you wish to proceed? '
                               '(Y/N) ')
        if choice.upper() == 'Y':
            logging.warning(' *** DISCLAIMER: There is absolutely no warranty '
                            'for any action performed by the user from here '
                            'on ***')
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
                        result, validation = connector.run_OBD_command(
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
                            print(result)
                except KeyboardInterrupt:
                        break
        logging.info(' >>> Expert mode aborted by user, finishing...')
        connector.run_OBD_command('END', expert=True)

    def sampler_mode(self, connector):
        """Poll every single PID once, then only those wich respond"""

        self.poll_commands = self.record.GetOBD_DBInfo(self.option)
        round = 1
        total = len(self.poll_commands)
        available_pids = []
        for i in range(len(self.poll_commands)):
            available_pids.append(1)

        while self.keep_going is True:
            k = 1
            logging.info(' > Polling parameters: round %i' % round)
            self.total_steps = len(self.poll_commands)
            for i in range(len(self.poll_commands)):
                logging.info(' > Getting OBD polling parameter ({0}/{1})...'
                             .format(k, total))
                if available_pids[i] == 1:
                    data, validation = connector.run_OBD_command(
                        self.poll_commands[i], self.option)
                    time.sleep(.1)
                    if re.search('NO DATA', data) or validation == 'N':
                        available_pids[i] = 0
                k += 1
            round += 1


def build_logging():
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
        }

    config = ConfigParser.RawConfigParser()
    configfilepath = 'config.ini'

    config.read(configfilepath)
    event_log = config.get('logging', 'event_log')
    logging_level = config.get('logging', 'level')

    if event_log == 'yes':
        LOG_FILENAME = time.strftime("%Y%m%d-%H%M%S-logger.log")
        logging.basicConfig(
            format = '%(levelname)s;%(asctime)s;%(message)s',
            datefmt = '%d/%m/%Y %H:%M:%S',
            filename = LOG_FILENAME,
            filemode = 'a',
            level = LEVELS.get(logging_level, logging.NOTSET)
            )
        f = open(LOG_FILENAME, 'a')
        f.write('LOG_LEVEL;TIMESTAMP;MESSAGE\n')
        f.close()
        return True
    else:
        return False
