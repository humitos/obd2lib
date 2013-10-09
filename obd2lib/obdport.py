# -*- coding: utf-8 -*-

import sys
import serial
import time
import re
import logging


class OBDPort(object):
    """OBDPort allows to abstract the communication with ELM-327"""

    def __init__(self, portnum, baudrate, serial_timeout,
                 max_retries, logoutput=False):

        baudrate = baudrate
        bytesize = serial.EIGHTBITS
        parity = serial.PARITY_NONE
        stopbits = serial.STOPBITS_ONE
        timeout = serial_timeout

        self.ELMver = "Unknown"
        # state SERIAL is
        #  1 connected
        #  0 disconnected (connection failed)
        self.state = 1
        self.portnum = portnum
        self.max_retries = max_retries
        self.log = []
        self.logoutput = logoutput

        # commands to setup before start sending OBD commands
        pre_connect_commands = [
            'ate0',  # character echo ON (00 -> ON, FF -> OFF)
            'ati',  # request for the product ID string
            'ath1',  # printing of header bytes (0 -> OFF, 1 -> ON)
            'atsp0'  # set protocol to AUTO
        ]

        # commands to send before closing the connection
        post_connect_commands = [
            'atdp',  # display protocol
            'atdpn',  # display protocol by number
            'atstff'  # set the "NO DATA" timeout to 0xFF
        ]

        logging.debug('Opening interface (serial port)')

        try:
            logging.debug('Trying to open designed port "{0}" (serial port)'
                          .format(self.portnum))
            self.port = serial.Serial(
                self.portnum, baudrate, parity=parity, stopbits=stopbits,
                bytesize=bytesize, timeout=timeout)
        except serial.SerialException as e:
            s = re.search(r'\[Errno (\d+)\]', e.message)
            errno = int(s.groups()[0])
            if errno == 2:
                print('No such file or directory: "{0}"'.format(self.portnum))
                print('Please, check that you have your ELM327 connected to '
                      'that port')
                sys.exit(1)
            else:
                print(e)
                self.state = 0
                return None

        logging.debug('Interface "{0}" scanned successfully'
                      .format(self.port.portstr))
        logging.debug('Connecting to ECU...')

        ready = "ERROR"
        count = 0

        while ready == "ERROR":  # until error is returned try to connect
            try:
                self.send_command('atz')  # reset chips
            except serial.SerialException as e:
                print(e)
                self.state = 0
                return None

            self.ELMver, validation_test = self.get_result('atz')
            if not(re.search('ELM', self.ELMver) or
                   re.search('OK', self.ELMver)):

                logging.warning('Aborted execution: unable to connect to ELM '
                                'device')

                self.close()
                self.state = 0
                return None

            # connected
            for i in pre_connect_commands:
                self.send_command(i)
                got, validation_test = self.get_result(i)

            self.send_command('0100')  # ping/PID request
            ready, validation_test = self.get_result('0100')

            if re.search('[0-9]', ready) or re.search('OK', ready):
                for i in post_connect_commands:
                    self.send_command(i)
                    got, validation_test = self.get_result(i)
            else:
                logging.debug('Connection attempt failed: {0}'.format(ready))
                logging.warning('Be sure that the key is in the '
                                'IGNITION position')
                ready = 'ERROR'  # Expecting error message: BUSINIT:.ERROR
                time.sleep(5)
                logging.debug('Connection attempt: {0}'.format(count))
                count += 1
                if count == self.max_retries:
                    logging.warning('EXECUTION ABORTED: unable to connect '
                                    'after max_retries')
                    self.close()
                    self.state = 0
                    return None

    def send_command(self, cmd):
        """Internal use only: not a public interface"""

        if self.port:
            self.port.flushOutput()
            self.port.flushInput()
            for c in cmd:
                self.port.write(c)
            self.port.write("\r\n")
        return

    def get_result(self, cmd):
        """Internal use only: not a public interface"""

        if self.port:
            buffer = ''
            ini_t = time.time()
            cur_t = time.time()
            while (cur_t - ini_t < 5):
                c = self.port.read(1)
                cur_t = time.time()
                if c == '>' and len(buffer) > 0:
                    # prompt received
                    break
                else:
                    if (buffer != '' or c != '>'):
                        if (c == '\r' or c == '\n' or c == ':'):
                            buffer = buffer + ' '
                        else:
                            buffer = buffer + c

            if re.search('at', cmd, flags=re.IGNORECASE):
                valid_response = 'SETUP'
            else:
                valid_response = 'N'
                test_pattern = buffer.replace(' ', '')
                check = '4' + cmd[1:]
                if re.search(check, test_pattern):
                    valid_response = 'Y'

            buffer = buffer.strip()
            logging.info('Output of "{0}": "{1}"'.format(cmd, buffer))
            if self.logoutput:
                self.log_answer(cmd, buffer, valid_response)

            # TODO: check if this 're-connection' is valid
            # if valid_response == 'N':
            #     # verify that the connection is still active, and
            #     # reinitialize the connection
            #     logging.warning('Command "{0}" was invalid. Reactivating '
            #                     'the connection by sending "0100" and "atpc"')
            #     self.send_command('0100')
            #     self.send_command('atpc')

            return buffer, valid_response
        return None, None

    def log_answer(self, cmd, answer, valid):
        self.log.append([cmd, answer, valid, time.time()])

    def close(self):
        """Resets device and closes all associated filehandles"""

        if not(self.port is None) and self.state == 1:
            self.send_command("atz")
            self.port.close()

        self.port = None
        self.ELMver = "Unknown"
