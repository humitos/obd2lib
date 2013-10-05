# -*- coding: utf-8 -*-

import re
import sys
import logging

from obdport import OBDPort


class OBDConnector(object):

    def __init__(self, comport, reconnattempts, sertimeout):
        self.comport = comport
        self.reconnattempts = reconnattempts
        self.sertimeout = sertimeout

    def initCommunication(self):

        self.OBD_Interface = OBDPort(
            self.comport,
            self.sertimeout,
            self.reconnattempts,
            logoutput=True
        )

        if self.OBD_Interface.state == 0:  # serial port can not be opened
            logging.warning('No init interface {0}... shutting down app!'
                            .format(self.OBD_Interface.portnum))
            return 0
        else:
            logging.debug('Interface {0} initialized successfully'
                          .format(self.OBD_Interface.portnum))
            return 1

    def run_OBD_command(self, obd_command, expert=False):

        if (self.OBD_Interface.state == 1):
            # caution, if UNABLE TO CONNECT is received, OBD_Interface
            # remains set to 1

            if obd_command == 'END':
                self.OBD_Interface.close()
                return

            self.OBD_Interface.send_command(obd_command)

            bus_data = ''
            bus_data, validation_test = self.OBD_Interface\
                .get_result(obd_command)

            if bus_data:
                if (re.search('UNABLE', bus_data) or
                        re.search('BUSY', bus_data) or
                        re.search('ERROR', bus_data)) and \
                        not expert:
                    logging.warning(
                        'Unable to connect to OBD socket while getting '
                        'parameters, shutting down app... Please check port '
                        'configuration, connectivity between laptop and OBD '
                        'socket, and turn the ignition on in the car!')
                    self.OBD_Interface.close()
                    sys.exit(1)
                return bus_data, validation_test
            else:
                return 'ERROR', validation_test
        else:
            return 'OBD PORT CLOSED'
