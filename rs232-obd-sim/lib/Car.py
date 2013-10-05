""" Simulates a vehicle.

Implements its pedals, buttons and ECUs
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

RPM_MAX = 16383.75
VSS_MAX = 255



class Car:
    def __init__(self):
        self.rpm = 0
        self.vss = 0
        self.pids_supported = 0xBE3EA811

    def setRPM(self, rpm):
        rpm = int(rpm)
        self.rpm = min(rpm, RPM_MAX)

    def getRPM(self):
        return self.rpm

    def setVSS(self, vss):
        vss = int(vss)
        self.vss = min(vss, VSS_MAX)

    def getVSS(self):
        return self.vss

    def getPIDsSupported(self):
        return self.pids_supported

