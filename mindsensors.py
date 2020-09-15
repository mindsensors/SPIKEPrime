# Write your code here :-)
#!/usr/bin/env python
#
# Copyright (c) 2020 mindsensors.com.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# History:
# Date            Author            Comments
# 09/13/20 Nitin Patil             Updated methods for   reading and changing modes in SUMOEYES module
#


import utime as time
import ustruct
import hub




IN = 0
OUT = 1
LOW = 0
HI = 1

## @package SPIKEi2c
# This is the SPIKEi2c module for Lego education SPIKE Prime and mindsensors.com
"""
Soft I2C Implementation
"""
class SPIKEi2c():

    int_clk = -1

    def tick(self,anz):
        time.sleep(anz*self.int_clk)

    def GPIO_setup(self,line,state):
        line.direction(state)

    def GPIO_output(self,line,value):
        line.value(value)

    def GPIO_input(self,line):
        return line.value()

    def __init__(self,port, i2c_address,bitrate = 100):
        port.mode(hub.port.MODE_GPIO)
        time.sleep(0.1)
        self.SCL = port.p5  # pin 5
        self.SDA = port.p6  # pin 6
        self.SCL.direction(OUT)
        self.SDA.direction(OUT)
        self.SCL.value(HI)
        self.SDA.value(HI)
        self.address = i2c_address

        if bitrate == 100:
            self.int_clk = 0.0000025
        elif bitrate == 400:
            self.int_clk = 0.000000625
        elif bitrate == 1000:
            self.int_clk = 1
        elif bitrate == 3200:
            self.int_clk = 1

    def Start(self):
        #SCL
        #  ______
        #  |     |______
        #SDA
        #  ___
        #  |  |_________

        self.GPIO_setup(self.SDA, OUT) #configure SDA as output
        self.GPIO_output(self.SDA, HI)
        self.GPIO_output(self.SCL, HI)
        #self.tick(1)
        self.GPIO_output(self.SDA, LOW)
        #self.tick(1)
        self.GPIO_output(self.SCL, LOW)
        #self.tick(2)


    def ReadAck(self):
        self.GPIO_setup(self.SDA, IN)
        readbuffer =0
        for i in range(8):
            self.GPIO_output(self.SCL, HI)
            #self.tick(2)
            readbuffer |= (self.GPIO_input(self.SDA)<< 7) >> i
            self.GPIO_output(self.SCL, LOW)
            #self.tick(2)

        self.GPIO_setup(self.SDA, OUT)
        self.GPIO_output(self.SDA, LOW)
        self.GPIO_output(self.SCL, HI)
        #self.tick(2)
        self.GPIO_output(self.SCL, LOW)
        self.GPIO_output(self.SDA, LOW)
        #self.tick(2)
        return readbuffer

    def ReadNack(self):
        self.GPIO_setup(self.SDA, IN)
        readbuffer =0
        for i in range(8):
            self.GPIO_output(self.SCL, HI)
            #self.tick(2)
            readbuffer |= (self.GPIO_input(self.SDA)<< 7) >> i
            self.GPIO_output(self.SCL, LOW)
            #self.tick(2)

        self.GPIO_setup(self.SDA, OUT)
        self.GPIO_output(self.SDA, HI)
        self.GPIO_output(self.SCL, HI)
        #self.tick(2)
        self.GPIO_output(self.SCL, LOW)
        self.GPIO_output(self.SDA, LOW)
        #self.tick(2)
        return readbuffer

    def WriteByte(self,byte):
        if byte > 0xff:
            return -1
        #print byte
        self.GPIO_setup(self.SDA, OUT)
        for i in range(8):
            #MSB First
            if (byte << i) & 0x80 == 0x80:
                self.GPIO_output(self.SDA, HI)
                self.GPIO_output(self.SCL, HI)
                #self.tick(2)
                self.GPIO_output(self.SCL, LOW)
                self.GPIO_output(self.SDA, LOW)
                #self.tick(2)
            else:
                self.GPIO_output(self.SDA, LOW)
                self.GPIO_output(self.SCL, HI)
                #self.tick(2)
                self.GPIO_output(self.SCL, LOW)
                #self.tick(2)

        self.GPIO_setup(self.SDA, IN)
        self.GPIO_output(self.SCL, HI)
        #self.tick(1)
        #Get The ACK
        #if GPIO.input(self.SDA):
        #    print "ACK"
        #else:
        #    print "NACK"
        #self.tick(2)
        self.GPIO_output(self.SCL, LOW)
        #self.tick(2)

    def Stop(self):
        #SCL
        #  _____________
        #  |
        #SDA
        #     __________
        #   __|
        self.GPIO_setup(self.SDA, OUT) #cnfigure SDA as output

        self.GPIO_output(self.SDA, LOW)
        self.GPIO_output(self.SCL, HI)
        #self.tick(1)
        self.GPIO_output(self.SDA, HI)
        #self.tick(3)

    def readByte(self, reg) :
        self.Start()
        self.WriteByte( self.address)
        self.WriteByte(reg)
        self.Start()
        self.WriteByte( self.address|1)
        result = self.ReadNack()
        self.Stop()
        return (result)

    def readArray(self, reg,len) :
        result =[]
        self.Start()
        self.WriteByte( self.address)
        self.WriteByte(reg)
        self.Start()
        self.WriteByte( self.address|1)
        for i in range(len-1): result.append(self.ReadAck())
        result.append(self.ReadNack())
        self.Stop()
        return (result)


    def writeByte(self,reg,value) :
        self.Start()
        self.WriteByte( self.address)
        self.WriteByte(reg)
        self.WriteByte(value)
        self.Stop()

    def writeArray(self, reg, arr):
        self.Start()
        self.WriteByte( self.address)
        self.WriteByte(reg)
        for i in range(len): self.WriteByte(arr[i])
        self.Stop()

    def readString(self,reg, length):
        ss = ''
        for x in range(0, length):
            ss = ''.join([ss, chr(self.readByte(reg+x))])
        return ss

    def readInteger(self, reg):
        b0 = self.readByte( reg)
        b1 = self.readByte( reg+1)
        r = b0 + (b1<<8)
        return r

    def readIntegerSigned(self, reg):
        a = self.readInteger(reg)
        #signed_a = ustruct.unpack("<h", a)[0]
        return a

    def readLong(self, reg):
        b0 = self.readByte(reg)
        b1 = self.readByte(reg+1)
        b2 = self.readByte(reg+2)
        b3 = self.readByte(reg+3)
        r = b0 + (b1<<8) + (b2<<16) + (b3<<24)
        return r

    ##  Read the firmware version of the i2c device
    def GetFirmwareVersion(self,):
        ver = self.readString(0x00, 8)
        return ver

    ##  Read the vendor name of the i2c device
    def GetVendorName(self):
        vendor = self.readString(0x08, 8)
        return vendor

    ##  Read the i2c device id
    def GetDeviceId(self):
        device = self.readString(0x10, 8)
        return device


## @package SUMOEYES
# This is the SUMOEYES module for Lego education SPIKE Prime and mindsensors.com


class SUMOEYES():
    LONG = 0
    SHORT = 1
    RIGHT = 33
    LEFT = 66
    FRONT = 99
    def __init__(self, port):
        self.portS=port
        print(port.device.get())



    def selectRange(self,range):
        self.portS.device.mode(range)


    def read(self):
        return self.portS.device.get()[0]

    def GetFirmwareVersion(self):
        return self.portS.info()['fw_version']

    def GetHardwareVersion(self):
        return self.portS.info()['hw_version']





## @package DIST
# This is the DIST module for Lego education SPIKE Prime and mindsensors.com


class DIST(SPIKEi2c):

    ## Default Dist-Nx I2C Address
    DIST_ADDRESS = 0x2
    ## Command Register
    COMMAND = 0x41
    ## Distance Register. Will return an integer value
    DISTANCE = 0x42
    ## Voltage Register. Will return an integer value
    VOLTAGE = 0x44
    #    TYPE = 0x44

    ## Initialize the class with the i2c address of your Dist-Nx
    #  @param self The object pointer.
    #  @param dist_address Address of your Dist-Nx.
    def __init__(self, port, dist_address=DIST_ADDRESS):
        # the DIST address
        self.dist_address = dist_address
        self.port = port
        SPIKEi2c.__init__(self, self.port, self.dist_address)

    ## Writes a value to the command register
    #  @param self The object pointer.
    #  @param command Value to write to the command register.
    def command(self, command):

        self.writeByte(self.COMMAND, int(cmd))

    ## Reads the distance in millimeters
    #  @param self The object pointer.
    def get_distance(self):

        return self.readInteger(self.DISTANCE)

    ## Reads the distance in inches
    #  @param self The object pointer.
    def get_distance_inches(self):
        d = self.get_distance()
        return d / 25

    ## Reads the voltage of the Dist-Nx
    #  @param self The object pointer.
    def get_voltage(self):
        return self.readInteger(self.VOLTAGE)

## @package EV3FPS
# This is the EV3FPS module for Lego education SPIKE Prime and mindsensors.com

class EV3FPS(SPIKEi2c):

    ## Default EV3fps I2C Address
    EV3fps_ADDRESS = (0x62)
    ## Command Register
    COMMAND = 0x41
    ## EV3fpsMatched Register. Will return an byte value
    EV3fpsMatched = 0x42
    ## EV3fpsStatus Register. Will return an byte value
    EV3fpsStatus = 0x43
    ## EV3fpsProfileId Register. Will return an byte value
    EV3fpsProfileId = 0x44
    ## EV3fpsProfileCt Register. Will return an byte value
    EV3fpsProfileCt = 0x45
    ## EV3fpsProfileCap Register. Will return an byte value
    EV3fpsProfileCap = 0x46
    ##Supported commands
    EV3fps_delete = 0x44
    EV3fps_enroll = 0x45
    EV3fps_remove = 0x52


    ## Initialize the class with the i2c address of your EV3fps
    #  @param self The object pointer.
    #  @param EV3fps_address Address of your EV3fps.
    def __init__(self, port,EV3fps_address = EV3fps_ADDRESS):
        #the EV3fps address
        self.EV3fps_address =EV3fps_address
        self.port = port
        print(port)
        SPIKEi2c.__init__(self, self.port,self.EV3fps_address )

    ## Writes a value to the command register
    #  @param self The object pointer.
    #  @param command Value to write to the command register.
    def command(self, command):

        self.writeByte(self.COMMAND,command)

    ## Reads the EV3fpsMatched
    #  @param self The object pointer.
    def get_EV3fps_Matched(self):

        return self.readByte(self.EV3fpsMatched)


    ## Reads the EV3fpsStatus
    #  @param self The object pointer.
    def get_EV3fps_Status(self):
        return self.readByte(self.EV3fpsStatus)


    ## Reads the EV3fpsProfileId
    #  @param self The object pointer.
    def get_EV3fps_ProfileId(self):
        return self.readByte(self.EV3fpsProfileId)

    ## Reads the EV3fpsProfileCt
    #  @param self The object pointer.
    def get_EV3fps_ProfileCt(self):
        return self.readByte(self.EV3fpsProfileCt)

    ## Reads the EV3fpsProfileCap
    #  @param self The object pointer.
    def get_EV3fps_ProfileCap(self):
        return self.readByte(self.EV3fpsProfileCap)

    ## Delete all stored profiles from EV3fps
    #  @param self The object pointer.
    def get_EV3fps_Delete(self):
        return self.command(self.EV3fps_delete)

    ## Remove stored profile at ProfileId from EV3fps
    #  @param self The object pointer.
    def get_EV3fps_Remove(self,ProfileId):
        self.writeByte(self.EV3fpsProfileId,ProfileId)
        return self.command(self.EV3fps_remove)

    ## Enroll New profile to EV3fps
    #  @param self The object pointer.
    def get_EV3fps_Enroll(self):
        self.command(self.EV3fps_enroll)
        status =self.get_EV3fps_Status()
        while(status >1):
            status =self.get_EV3fps_Status()
            time.sleep_ms(100)

        return    0

## @package IRTHERMO
# This is the IRTHERMO  module for Lego education SPIKE Prime and mindsensors.com

class IRTHERMO(SPIKEi2c):

    ## Default IRthermometer I2C Address
    IRTHERMO_ADDRESS = 0x2A
    ## Command Register
    COMMAND = 0x41
    ## Ambient  Temperature in C. Will return an integer value
    AMBIENTC = 0x42
    ## Target  Temperature in C. Will return an integer value
    TARGETC = 0x44
    ## Ambient  Temperature in F. Will return an integer value
    AMBIENTF = 0x46
    ## Target  Temperature in C. Will return an integer value
    TARGETF = 0x48

    ## Initialize the class with the i2c address of your IRthermometer
    #  @param self The object pointer.
    #  @param dist_address Address of your IRthermometer.
    def __init__(self, port, irthermo_address=IRTHERMO_ADDRESS):
        # the IRTHERMO address
        self.irthermo_address = irthermo_address
        self.port = port
        SPIKEi2c.__init__(self, self.port, self.irthermo_address)

    ## Writes a value to the command register
    #  @param self The object pointer.
    #  @param command Value to write to the command register.
    def command(self, command):

        self.writeByte(self.COMMAND, int(cmd))

    ## Reads the Ambient Temperature in Celsius
    #  @param self The object pointer.
    def get_AmbientC(self):

        return self.readInteger(self.AMBIENTC) / 100

    ## Reads the Ambient Temperature in Fahrenheit
    #  @param self The object pointer.
    def get_AmbientF(self):

        return self.readInteger(self.AMBIENTF) / 100

    ## Reads the Target Temperature in Celsius
    #  @param self The object pointer.
    def get_TargetC(self):

        return self.readInteger(self.TARGETC) / 100

    ## Reads the Target Temperature in Fahrenheit
    #  @param self The object pointer.
    def get_TargetF(self):

        return self.readInteger(self.TARGETF) / 100

