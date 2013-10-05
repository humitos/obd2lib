# -*- coding: utf-8 -*-

from obd2lib import elm as elm327

elm327.build_logging()

elm = elm327.Elm()
elm.do_connect()

# AVAILABLE MODES
# -C Chec
#   Perform a check already prepeared.
# -D Clear
#   Clears all stored trouble codes and turns the MIL off.
# -S Sampler
#   Not sure what this is.
# -E Expert
#   Interactive console where you can excecute OBD commands.
elm.do_test('-E')
elm.do_disconnect()
