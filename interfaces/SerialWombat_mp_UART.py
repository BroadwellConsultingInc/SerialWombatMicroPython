import SerialWombat
import time
import machine



class SerialWombatChipUART(SerialWombat.SerialWombatChip):
    ser  = 0
    def __init__(self,port):
        self.ser = port


    def sendPacket (self,tx):
        if (isinstance(tx,list)):
            tx = bytearray(tx);
        clear = bytearray([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55])
        self.ser.write(clear)
        self.ser.flush()

        rx = self.ser.read(8) 
        while (rx != None):
            rx = self.ser.read(1)
        self.ser.write(tx)
        #self.ser.write([self.address])  #TODO this is for I2C Bridge.  Remove
        rx = self.ser.read(8)
        if (rx== None):
            rx = bytearray()
        delaycount = 0
        while (len(rx) < 8 and delaycount < 25):
            newBytes = self.ser.read(8 - len(rx))
            if (newBytes != None and len(newBytes) > 0):
                rx += newBytes
            time.sleep(.002)
            delaycount +=1
        return 8,rx  #TODO add error check, size check

