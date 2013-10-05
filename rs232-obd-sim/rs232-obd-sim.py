""" rs232-obd-sim.py - RS-232 to OBD bridge simulator

"""
##    Copyright (C) 2010 Miguel Gonzalez <enoelrocotiv@gmail.com>
##    Copyright (C) 2010 Oscar Iglesias  <osc.iglesias@gmail.com>
##
##    This file is part of rs232-obd-sim.py.
##
##    rs232-obd-sim.py is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program; if not, write to the Free Software Foundation,
##    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


import sys
import threading
from os.path import split

import lib
from lib import Sensors

from lib.utils import debug

def notice():
    return """Copyright (C) 2010 Miguel Gonzalez, Oscar Iglesias
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; see the COPYING file for details.
"""

def usage():
    (path, prog) = split(sys.argv[0])
    return """Usage: python %(prog)s portname

    portname    port, device name

Example:

    > %(prog)s COM3

"""%{'prog': prog}

if __name__ == '__main__':
    print('rs232-obd-sim.py - RS-232 to OBD bridge simulator')
    print(notice())

    try:
        port = sys.argv[1]
    except IndexError:
        print usage()
        sys.exit(1)

    print('Starting...')

    my_car = lib.Car()
    my_elm = lib.Elm(port)

    my_elm.registerSensor(Sensors.PIDsSupported(0x01, 0x00, my_car))
    my_elm.registerSensor(Sensors.Tests(0x01, 0x01))
    my_elm.registerSensor(Sensors.DTCFRZF(0x01, 0x02))
    my_elm.registerSensor(Sensors.FUELSYS(0x01, 0x03))
    my_elm.registerSensor(Sensors.LOAD_PCT(0x01, 0x04))
    my_elm.registerSensor(Sensors.ECT(0x01, 0x05))
    my_elm.registerSensor(Sensors.SHRTFT1and3(0x01, 0x06))
    my_elm.registerSensor(Sensors.LONGFT1and3(0x01, 0x07))
    my_elm.registerSensor(Sensors.MAP(0x01, 0x0B))
    my_elm.registerSensor(Sensors.RPM(0x01, 0x0C, my_car))
    my_elm.registerSensor(Sensors.VSS(0x01, 0x0D, my_car))
    my_elm.registerSensor(Sensors.SPARKADV(0x01, 0x0E))
    my_elm.registerSensor(Sensors.IAT(0x01, 0x0F))
    my_elm.registerSensor(Sensors.TP(0x01, 0x11))
    my_elm.registerSensor(Sensors.O2SLOC(0x01, 0x13))
    my_elm.registerSensor(Sensors.BNK1SEN2(0x01, 0x15))
    my_elm.registerSensor(Sensors.OBDSUP(0x01, 0x1C))

    my_elm.registerSensor(Sensors.DTC_GET(0x03, None))

    my_elm.registerSensor(Sensors.DTC_CLR(0x04, None))

    my_elm.registerSensor(Sensors.DTC_LAST_CYCLE_GET(0x07, None))


    my_elm.start()

    my_cli = lib.CLI()
    my_cli.attach_car(my_car)
    my_cli.cmdloop()

    my_elm.exit()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        print 'Waiting for ', t.getName()
        t.join(3)

