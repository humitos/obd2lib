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
-----------------------

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


Collect and create graphics
---------------------------

I wrote two command line utilities to collect data
(``collect_data.py``) through the OBD-II interface while your are
driving and store it in a file. After that, this file is processed
with another script (``generate_graphs.py``) to create some nice
graphics like this one:

![](http://oi41.tinypic.com/vxlt7n.jpg)


Permissions
-----------

I needed to add my user to "dialout" group in Ubuntu 13.04

    sudo adduser your-user-here dialout


Simulator
---------

I borrow the "rs232-obd-sim" from here
(http://code.google.com/p/rs232-obd-sim/) and I'm using it to make
some test in the development process.

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
