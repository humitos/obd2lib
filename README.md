obd2lib
=======

OBD-2 library to read information from cars.

The idea is to record as much information as the car support to create
graphs and stats with that data about the car.

This software is based on Karmind project (http://www.karmind.com/)
and its software published under GPL license.

 * http://code.google.com/p/karmind-obd-application/

Since I did not receive any answer from the original authors, I
started coding by myself and changing some functionality that I need.


How to use it
-------------

    >>> from obd2lib.obdconnector import OBDConnector
    >>> connector = OBDConnector('/dev/ttyUSB0', 5, 10)
    >>> connector.initCommunication()
    1
    >>> connector.run_OBD_command('0100')
    ('86 F1 10 41 00 BE 3E B0 11 85', 'Y')
    >>> connector.run_OBD_command('END')


How to read the answers
-----------------------

All the information needed to decode the answer is in Wikipedia:

 * http://en.wikipedia.org/wiki/OBD-II_PIDs
