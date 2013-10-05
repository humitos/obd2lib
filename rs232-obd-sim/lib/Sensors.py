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



from utils import hex_to_str


class Sensor():
    def __init__(self, service, pid = None, my_car = None):
        self.service = service
        self.car = my_car
        self.pid = pid

    def getService(self):
        return self.service

    def getPID(self):
        return self.pid

    def payload(self):
        return hex_to_str(0x00)

    def response(self):
        msg =  hex_to_str(0x40 + self.getService(), 2)
        msg += hex_to_str(self.getPID(), 2)
        msg += self.payload()
        return msg


class PIDsSupported(Sensor):
    """Response to Service $01 PID $00 (Ping/Keepalive message of ISO15031-5:2006).

    PIDs supported from [01-20] group.
    Payload composed by 4 bytes, stating each bit whether every PID in the group
    is supported (1: available).

    TODO (optional): implement the rest of the PID availability request
    messages ($0120,$0140,$0160,$0180,$01A0,$01B0,$01C0).
    """

    def payload(self):
        pids_supported = self.car.getPIDsSupported()
        return hex_to_str(pids_supported, 8)


class Tests(Sensor):

    # Response to Service $01 PID $01 request message (Tests).
    # Payload composed by 4 bytes.
        #A[7]: MIL indicator. A[0-6]: # of DTCs stored in ECU.
        #B,C,D: Supported test and completion state.

    def payload(self):
        return hex_to_str(0x8307E500, 8)


class DTCFRZF(Sensor):

    # Response to Service $01 PID $02 (DTC that caused required freeze frame data storage).
    # Payload composed by 4 bytes. ($0000 indicates no freeze frame data). Valid range: $0000-$FFFF.

    def payload(self):
        return hex_to_str(0x0000, 4) # 4 bytes sure?!


class FUELSYS(Sensor):

    # Response to Service $01 PID $03 (Fuel System Status).
    # Payload composed by 2 bytes.
    # A,B bytes description: only one bit set to a '1' in each byte at the same time. A,B[5-7] reserved, shall be reported as '0'.

    # TO DO: Show the real state of fuel system in the application rather than only hex string!

    def payload(self):
        return hex_to_str(0x0100, 4)


class LOAD_PCT(Sensor):

    # Response to Service $01 PID $04 (Calculated Load Value).
    # Payload composed by 1 byte.
    # A byte description: ranging from $00to $FF, meaning 0% to 100%, scaling through *100/255.

    # TO DO: This parameter must be dependent of RPM and speed measures.

    def payload(self):

        # Temporary implemented as an uniform variable

        data  = 99
        return hex_to_str(data, 2)


class ECT(Sensor):

    # Response to Service $01 PID $05 (Engine Coolant Temperature).
    # Payload composed by 1 byte.
    # A byte  description: ranging from $00 to $FF, meaning 40 below zero up to 215 Celsius degrees, scaling 1 degree with minus 40 offset.
    # TO DO: This parameter should be dependent of time and stabilize between 75 and 120 degrees.

    def payload(self):
        # Temporary implemented as an uniform variable
        data = 55
        return hex_to_str(data, 2)


class SHRTFT1and3(Sensor):

    # Response to Service $01 PID $06 (Short Term Fuel Trim - Bank 1 and 3).
    # Payload composed by 2 bytes.

    # Short Term Fuel Trim Bank 1/3 shall indicate the correction being utilized by the closed-loop fuel algorithm. If the
    # fuel system is in open loop, SHRTFT1/3 shall report 0 % correction.
    # Data B shall only be included in the response to a PID $06 request if PID $1D (Location of Oxygen Sensors)
    # indicates an oxygen sensor is present in Bank 3. The external test equipment can determine length of the
    # response message based on the data content of PID $13 or $1D. In no case shall an ECU send an unsupported
    # data byte A if data byte B is supported.

    # A,B bytes description: ranging from $00 to $FF, meaning minus 100% (lean) up to 99.22% (rich) , scaling *100/128 (0% at 128)

    # TO DO: The behaviour should be correctly implemented, as indicated above.

    def payload(self):
        return hex_to_str(0x51, 4)

class LONGFT1and3(Sensor):

    # Response to Service $01 PID $07 (Long Term Fuel Trim - Bank 1 and 3).
    # Payload composed by 2 bytes.

    #Fuel trim correction for Bank 1/3 stored in Non-volatile RAM or Keep-alive RAM. LONGFT shall indicate the
    #correction being utilized by the fuel control algorithm at the time the data is requested, in both open-loop and
    #closed-loop fuel control. If no correction is utilized in open-loop fuel, LONGFT shall report 0 % correction. If longterm
    #fuel trim is not utilized at all by the fuel control algorithm, the PID shall not be supported.
    #Data B shall only be included in the response to a PID $07 request if PID $1D (Location of Oxygen Sensors)
    #indicates an oxygen sensor is present in Bank 3. The external test equipment can determine length of the
    #response message based on the data content of PID $13 or $1D. In no case shall an ECU send an unsupported
    #data byte A if data byte B is supported. See examples in the description of PID $09.

    # A,B bytes description: ranging from $00 to $FF, meaning minus 100% (lean) up to 99.22% (rich) , scaling *100/128 (0% at 128)

    # TO DO: The behaviour should be correctly implemented, as indicated above.

    def payload(self):
        return hex_to_str(0x80, 4)


class MAP(Sensor):

    # Response to Service $01 PID $0B (Intake Manifold Absolute Pressure).
    # Payload composed by 1 byte.

    # MAP shall display manifold pressure derived from a Manifold Absolute Pressure sensor, if a sensor is utilized. If a
    # vehicle uses both a MAP and MAF sensor, both the MAP and MAF PIDs shall be supported.
    # If PID $4F is not supported for this ECU, or if PID $4F is supported and includes $00 for Intake Manifold Absolute
    # Pressure, the external test equipment shall use the scaling values included in this table for those values. If PID
    # $4F is supported for this ECU, the external test equipment shall calculate scaling and range for this PID as
    # explained in the PID $4F Data D definition.

    # A byte description: ranging from $00 to $FF, meaning from 0 KPa up to 255 KPa

    # TO DO: The behaviour should be correctly implemented, as indicated above. Should be translated from psi units to KPa (SI)

    def payload(self):
        # Temporary implemented as an uniform variable
        data = 99
        return hex_to_str(0x51, 2)


class RPM(Sensor):
    """Response to Service $01 PID $0C (Engine RPM).

    Payload composed by 2 bytes.
    Engine RPM shall display revolutions per minute of the engine crankshaft.

    A,B byte description: ranging from $00 to $FF, meaning from 0 to 16383,75 RPM,
    due to the scaling factor *1/4.
    """
    def payload(self):
        rpm = self.car.getRPM()
        return hex_to_str(rpm*4, 4)



class VSS(Sensor):
    """Response to Service $01 PID $0D (Vehicle Speed Sensor).

    Payload composed by 1 byte.

    VSS shall display vehicle road speed, if utilized by the control
    module strategy. Vehicle speed may be derived
    from a vehicle speed sensor, calculated by the PCM using other
    speed sensors, or obtained from the vehicle serial data communication bus.

    A byte description: ranging from $00 to $FF, meaning from 0 to 255 Km/h, no scaling factor.
    """
    # TO DO: The behaviour must be implemented in a more realistic way, and translated from MPH to KMPH.

    def payload(self):
        vss = self.car.getVSS()
        return hex_to_str(vss, 2)



class SPARKADV(Sensor):

    # Response to Service $01 PID $0E (Ignition Time Advance for #1 Cylinder).
    # Payload composed by 1 byte.

    # Ignition timing spark advance for #1 cylinder (not including mechanical advance).

    # A byte description: ranging from $00 to $FF, meaning from minus 64 to 63,5 degrees,  scaling factor 0.5 with 0 at 128.


    def payload(self):
        # Temporary implemented as an uniform variable
        data = 99
        return hex_to_str(data, 2)



class IAT(Sensor):

    # Response to Service $01 PID $0F (Intake Air Temperature).
    # Payload composed by 1 byte.

    # IAT shall display intake manifold air temperature, if utilized by the control module strategy. IAT may be obtained
    # directly from a sensor, or may be inferred by the control strategy using other sensor inputs.

    # A byte description: ranging from $00 to $FF, meaning from minus 40 to 215 degrees, no scaling factor  with minus 40 offset.


    def payload(self):
        # Temporary implemented as an uniform variable
        data = 99
        return hex_to_str(data, 2)




class TP(Sensor):

    # Response to Service $01 PID $11 (Absolute Throttle Position).
    # Payload composed by 1 byte.


    # Absolute throttle position (not relative or learned throttle position) shall be displayed as a normalized value,
    # scaled from 0 to 100. For example, if a 0 to 5 volt sensor is used (uses a 5,0 volt reference voltage), and the
    # closed throttle position is at 1,0 volts, TP shall display (1,0 div 5,0) = 20 at closed throttle and 50 at 2,5 volts.
    # Throttle position at idle will usually indicate greater than 0, and throttle position at wide open throttle will usually
    # indicate less than 100.

    # A byte description: ranging from $00 to $FF, meaning % , scaling *100/255


    def payload(self):
        # Temporary implemented as an uniform variable
        data = 99
        return hex_to_str(data, 2)




class O2SLOC(Sensor):

    # Response to Service $01 PID $13 (Location of Oxygen Sensors).
    # Payload composed by 1 byte.


    # Where sensor 1 is closest to the engine. Each bit indicates the presence or absence of an oxygen sensor at the following location.
    # PID 13 shall only be supported by a given vehicle if PID 1D is not supported. In no case shall a vehicle support both PIDs.

    # A byte description: 8 sensors, each bit set to 1 if sensor es present


    def payload(self):
        # Temporary implemented as an uniform variable
        data = 99
        return hex_to_str(data, 2)




class BNK1SEN2(Sensor):

    # Response to Service $01 PID $15 (Bank1 - Sensor2).
    # Payload composed by 2 bytes.


    # A byte description O2Sxy: from 0 up to 1,275 V scaling *0,005 (Oxigen Sensor Output Voltage)
    # B byte description SHRTFTxy: from minus 100 up to 99,22 percent scaling *100/128 (Short Term Fuel Trim)

    # TO DO: response display in pyOBD implementation is wrong !!!

    def payload(self):
        # Temporary implemented as an uniform variable
        data1 = 50 * 0x100
        data2 = 50
        return hex_to_str(data1+data2, 4)

class OBDSUP(Sensor):

    # Response to Service 01 PID 1C (OBD requirements to wich vehicle is designed).
    # Payload composed by 1 byte.

    # A byte description:

    # OBD II (California ARB) 01 OBD II
    # OBD (Federal EPA) 02 OBD
    # OBD and OBD II 03 OBD and OBD II
    # OBD I 04 OBD I
    # Not OBD compliant 05 NO OBD
    # EOBD 06 EOBD
    # EOBD and OBD II 07 EOBD and OBD II
    # EOBD and OBD 08 EOBD and OBD
    # EOBD, OBD and OBD II 09 EOBD, OBD and OBD II
    # JOBD 0A JOBD
    # JOBD and OBD II 0B JOBD and OBD II
    # JOBD and EOBD 0C JOBD and EOBD
    # JOBD, EOBD, and OBD II 0D JOBD, EOBD, and OBD II
    # Heavy Duty Vehicles (EURO IV) B1 0E EURO IV B1
    # Heavy Duty Vehicles (EURO V) B2 0F EURO V B2
    # Heavy Duty Vehicles (EURO EEC) C (gas engines) 10 EURO C
    # Engine Manufacturer Diagnostics (EMD) 11 EMD
    # ISO/SAE reserved 12  FA
    # ISO/SAE - Not available for assignment from FB to FF SAE J1939 special meaning


    def payload(self):
        return hex_to_str(0x06, 2)

class DTC_GET(Sensor):


    # Response to Service 03 (Request emission-related stored DTCs).
    # Payload composed by 7 bytes per ECU responding to code 0101.

    # Bytes description (per ECU!)

    # 1 Request emission-related DTC response SID (43) SIDPR
    # 2 DTC1 High Byte of P0143 01 DTC1HI
    # 3 DTC1 Low Byte of P0143 43 DTC1LO
    # 4 DTC2 High Byte of P0196 01 DTC2HI
    # 5 DTC2 Low Byte of P0196 96 DTC2LO
    # 6 DTC3 High Byte of P0234 02 DTC3HI
    # 7 DTC3 Low Byte of P0234 34 DTC3LO

    # If not valid DTC number, the values shall contain 00

    # TODO: This command must be dependent on the second byte reponse of 0101 (number of DTCs stored)


    def payload(self):
        a = 0x01
        a = 0x43 + a * 0x100
        a = 0x01 + a * 0x100
        a = 0x44 + a * 0x100
        a = 0x01 + a * 0x100
        a = 0x52 + a * 0x100
        return hex_to_str(a, 12)


class DTC_CLR(Sensor):


    # Response to Service 04 (Clear/reset emission-related diagnostic information).

    # MIL and number of diagnostic trouble codes (can be read with Service 01, PID 01)
    # Clear the IM (Inspection Maintenance) readiness bits (Service 01, PID 01 and 41)
    # Confirmed diagnostic trouble codes (can be read with Service 03)
    # Pending diagnostic trouble codes (can be read with Service 07)
    # Diagnostic trouble code for freeze frame data (can be read with Service 02, PID 02)
    # Freeze frame data (can be read with Service 02)
    # Oxygen sensor test data (can be read with Service 05)
    # Status of system monitoring tests (can be read with Service 01, PID 01)
    # On-board monitoring test results (can be read with Service 06)
    # Distance travelled while MIL is activated (can be read with Service 01, PID 21)
    # Number of warm-ups since DTCs cleared (can be read with Service 01, PID 30)
    # Distance travelled since DTCs cleared (can be read with Service 01, PID 31)
    # Time run by the engine while MIL is activated (can be read with Service 01, PID 4D)
    # Time since diagnostic trouble codes cleared (can be read with Service 01, PID 4E)
    # Other manufacturer

    # Payload composed by 1 or 3 bytes per ECU responding to code 0101.

    # Bytes description (per ECU) if request succeeded
    # 1 Clear or reset emission-related diagnostic information (44) SIDPR

    # Bytes description (per ECU) if request did not succeed
    # 1 Negative Response Service Identifier (7F) SINDR
    # 2 Clear or reset emission-related diagnostic information request SID (04) SIDRQ
    # 3 Negative Reponse or Condition not correct (22)

    # TODO: This command must reset many other parameters simulated in the other PID responses
    # FIXME: Negative response behaviour not implemented in pyOBD


    def payload(self):
        return hex_to_str(None)



class DTC_LAST_CYCLE_GET(Sensor):


    # Response to Service 07 (Request emission-related DTC detected during current or last completed driving cycle).

    # Payload composed by 7 bytes per ECU responding to code 0101, as in service 03.
    # Same reported messages changind the SIDPR from 43 to 47.

    def payload(self):
        return hex_to_str(0x014400000000, 12)