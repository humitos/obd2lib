obd2lib
=======

**WARNING: this is a work-in-progress project. Use it at your OWN RISK**

Python OBD-2 library to read information from cars using an ELM327 (or
similar) as interface.

The idea is to record as much information as the car support to create
graphs and stats with that data about the car.

This software is based on Karmind project (http://www.karmind.com/)
and its software published under GPL license.

 * http://code.google.com/p/karmind-obd-application/

Since I did receive an answer from the original author telling me that
the project doesn't have support now I started coding by myself and
changing some functionality that I need.


How to use it
-------------

    >>> from obd2lib.obdconnector import OBDConnector
    >>> connector = OBDConnector('/dev/ttyUSB0', 38400, 5, 10)
    >>> connector.initCommunication()
    1
    >>> connector.run_OBD_command('0100')
    ('86 F1 10 41 00 BE 3E B0 11 85', 'Y')
    >>> connector.run_OBD_command('END')
    >>>


How to read the answers
~~~~~~~~~~~~~~~~~~~~~~~

All the information needed to decode the answer is in Wikipedia:

 * http://en.wikipedia.org/wiki/OBD-II_PIDs

and ELM pdf datasheet:

 * http://elmelectronics.com/DSheets/ELM327DS.pdf

Also, there is a built-in decoder to a human-readable way:

    >>> from obd2lib import elmdecoder
    >>> from obd2lib.obdconnector import OBDConnector
    >>> connector = OBDConnector('/dev/ttyUSB0', 38400, 5, 10)
    >>> connector.initCommunication()
    1
    >>> answer, valid = connector.run_OBD_command('010F')
    >>> answer, valid
    ('48 6B 10 41 0F 63 76', 'Y')
    >>> elmdecoder.decode_answer('010F', answer)
    (59, 'Degrees Celsius')
    >>> connector.run_OBD_command('END')
    >>>


Command Line Interface (CLI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a command-line interface available in the respository. It
uses ``obd2lib`` to collect data at intervals of time from the car and
create some nice graphics.

    $ ./obd2 --help
    usage: obd2 [-h] (--info | --collect-data | --expert-mode | --create-graphs)
                [-p PORT] [-b BAUDRATE] [-i INTERVAL] [-a CONNECTION_ATTEMPTS]
                [-c COMMAND_ATTEMPTS] [-t TIMEOUT] [-s] [--convert-to-png]
                [--lazy] [-v]
                [inputfile [inputfile ...]]
    Utility to get information from the car using OBDII interface

    positional arguments:
      inputfile             log file used to created the graphics

    optional arguments:
      -h, --help            show this help message and exit
      --info                get compatibility information from car
      --collect-data        collect data at intervals of time
      --expert-mode         interactive expert mode
      --create-graphs       create nice graphs from log file
      -p PORT, --port PORT  port to connect (default: /dev/ttyUSB0)
      -b BAUDRATE, --baudrate BAUDRATE
                            baudrate used to connect to the port (default: 38400)
      -i INTERVAL, --interval INTERVAL
                            interval between queries (default: 1)
      -a CONNECTION_ATTEMPTS, --connection-attempts CONNECTION_ATTEMPTS
                            connection attempts (default: 10)
      -c COMMAND_ATTEMPTS, --command-attempts COMMAND_ATTEMPTS
                            attempts to try an invalid command (default: 3)
      -t TIMEOUT, --timeout TIMEOUT
                            timeout for the connection to the port (default: 10)
      -s, --server          run the obd2lib web-interface
      --convert-to-png      convert graphics from .svg to .png (it requires
                            inkscape)
      --lazy                decode answer to human-readable in expert mode
      -v, --verbose         show logging.DEBUG into stdout

There are 4 major modes:

#. **--info**: this mode connects to the ELM327 and fetchs all the
   supported information by the car just once and print it into the
   screen.

#. **--collect-data**: runs as a daemon fetching the supported
   information by the car at ``--interval``s of time. This is useful
   to check the status of the car while you are driving or to fix some
   issue.

#. **--expert-mode**: launchs an interactive console where you can
   execute any PID (supported and not supported) to check something
   specific.

#. **--create-graphs**: this mode uses the information collected by
   ``--collect-data`` and create some [nice .svg
   graphs](http://oi41.tinypic.com/vxlt7n.jpg) using *pygal*


Permissions
-----------

I needed to add my user to "dialout" group in Ubuntu 13.04

    sudo adduser your-user-here dialout


Simulator
---------

I borrow the "rs232-obd-sim" from here
(http://code.google.com/p/rs232-obd-sim/) and I'm using it to make
some test in the development process. *NOTE: I changed some minor
things to make it more compatible with obd2lib*

It requires "socat". So in Ubuntu I installed it by doing:

    sudo apt-get install socat

and then running in the terminal:

    $ socat -v -x -d -d PTY: PTY:
    2013/10/05 15:19:15 socat[15553] N PTY is /dev/pts/4
    2013/10/05 15:19:15 socat[15553] N PTY is /dev/pts/5
    2013/10/05 15:19:15 socat[15553] N starting data transfer loop with FDs [3,3] and [5,5]

Now, I can connect the "rs232-obd-sim" to /dev/pts/4

    $ python rs232-obd-sim.py /dev/pts/4
    rs232-obd-sim.py - RS-232 to OBD bridge simulator
    Copyright (C) 2010 Miguel Gonzalez, Oscar Iglesias
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; see the COPYING file for details.

    Starting...
    CAR>

and, for example, the "obd2" into --expert mode to /dev/pts/5

     $ ./obd2 --expert --port /dev/pts/5 --lazy
     WARNING: You are enabling EXPERT mode!

     It allows to perform any OBD command against Electronic Control Units.
     May lead to harm in your car if not used wisely. Do you wish to proceed? (Y/N) Y
     WARNING:root:*** DISCLAIMER: There is absolutely no warranty for
     any action performed by the user from here on ***

     Type "quit" or CTRL-C to exit
     ROOT@KT-OBD> 0105
     48 6B 10 41 05 37 40
     ROOT@KT-OBD> 010E
     48 6B 10 41 0E 63 75
     ROOT@KT-OBD> 010F
     48 6B 10 41 0F 63 76
     ROOT@KT-OBD> quit
     $

or, if you want to know WTF those values mean, you can run it with the --lazy option

     ROOT@KT-OBD> 0105
     15 Degrees Celsius
     ROOT@KT-OBD> 010E 
     -14.5 Degrees
     ROOT@KT-OBD> 010F    
     59 Degrees Celsius
