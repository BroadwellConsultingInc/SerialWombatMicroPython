import SerialWombat
import pigpio
import time



class SerialWombatChipPigpioI2c(SerialWombat.SerialWombatChip):
    i2cAddress = 0
    sda = 17
    scl = 27
    freq = 100000
    pi = pigpio.pi()    
    def __init__(self,sda,scl,i2cAddress,freq = 100000):
        self.sda = sda
        self.scl = scl
        self.freq = freq
        self.i2cAddress = i2cAddress


    def sendPacket (self,tx):
        self.pi.bb_i2c_open(self.sda,self.scl,self.freq)
        self.pi.bb_i2c_zip(self.sda,[4, self.i2cAddress, 2, 7, 8] + tx+ [3,0])
        time.sleep(0.002)
        rx = self.pi.bb_i2c_zip(self.sda,[4, self.i2cAddress, 2, 6, 8, 3,0])
        self.pi.bb_i2c_close(self.sda)
        return rx[0],rx[1]  #TODO add error check, size check

