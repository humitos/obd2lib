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

import cmd

class CLI(cmd.Cmd):
    """Command line interpreter for Car class
    """

    prompt = 'CAR> '
    intro = ""

    def emptyline(self):
        """ Overrides original method """
        return

    def attach_car(self, my_car):
        self.my_car = my_car

    def do_rpm(self, rpm):
        self.my_car.setRPM(rpm)

    def do_vss(self, vss):
        self.my_car.setVSS(vss)


    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        return True