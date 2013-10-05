# -*- coding: utf-8 -*-

import serial
import string
import time
import re
import logging


class OBDPort(object):
    """OBDPort allows to abstract the communication with ELM-327"""

    def __init__(self, portnum, serial_timeout, max_retries, record):

        baudrate = 38400
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
        self.record = record
        self.max_retries = max_retries

        # commands to setup before start sending OBD commands
        pre_connect_commands = [
            'ate0',
            'ati',
            'ath1',
            'atsp0'
        ]

        # commands to send before closing the connection
        post_connect_commands = [
            'atdp',
            'atdpn',
            'atstff'
        ]

        logging.debug('Opening interface (serial port)')
        self.record.set_info('Opening interface (serial port)')

        try:
            logging.debug('Trying to open designed port "{0}" (serial port)' \
                              .format(self.portnum))
            self.record.set_info('Trying to open designed port "{0}" (serial port)' \
                                     .format(self.portnum))
            self.port = serial.Serial(
                    self.portnum, baudrate, parity=parity, stopbits=stopbits,
                    bytesize=bytesize, timeout=timeout)
        except serial.SerialException as e:
            print(e)
            self.state = 0
            return None

        logging.debug('Interface "{0}" scanned successfully'.format(self.port.portstr))
        self.record.set_info('Interface "{0}" scanned successfully'.format(self.port.portstr))
        logging.debug('Connecting to ECU...')
        self.record.set_info('Connecting to ECU...')

        ready = "ERROR"
        count = 0

        while ready == "ERROR":  # until error is returned try to connect
            try:
                self.send_command('atz')  # initialize
            except serial.SerialException as e:
                print(e)
                self.state = 0
                return None

            self.ELMver, validation_test = self.get_result('atz')
            if not(re.search('ELM', self.ELMver) or
                   re.search('OK', self.ELMver)):

                logging.warning('Aborted execution: unable to connect to ELM device')
                self.record.set_info('Aborted execution: unable to connect to ELM device')

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
                self.record.set_info('Connection attempt failed: {0}'.format(ready))
                ready = 'ERROR'  # Expecting error message: BUSINIT:.ERROR
                time.sleep(5)
                logging.debug('Connection attempt: {0}'.format(count))
                self.record.set_info('Connection attempt: {0}'.format(count))
                count += 1
                if count == self.max_retries:
                    logging.warning('EXECUTION ABORTED: unable to connect after max_retries')
                    self.record.set_info('EXECUTION ABORTED: unable to connect after max_retries')
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

            logging.info('Output of "{0}": "{1}"'.format(cmd, buffer.strip()))
            if valid_response != 'SETUP':
                self.record.set_value(str(cmd),str(string.strip(buffer)))
            else:
                self.record.set_info(str(cmd),'SETUP')

            return buffer, valid_response
        return None, None

    def close(self):
        """Resets device and closes all associated filehandles"""

        if (self.port != None) and self.state == 1:
            self.send_command("atz")
            self.port.close()

        self.port = None
        self.ELMver = "Unknown"

        self.record.do_complete()
