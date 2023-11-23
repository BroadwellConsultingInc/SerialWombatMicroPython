import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombatUART
import SerialWombatQueue
import SerialWombatLiquidCrystal
from ArduinoFunctions import delay


ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
testString = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789One Two Three Four Five Six Seven Eight Nine Ten Uno Dos Tres Quatro Cinco Seis Siete Ocho Nueve 0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x09 0x0A 0x0B 0x0C 0x0D 0x0E 0x0F 0x10 0x11".encode('ascii')#The Quick Brown Fox Jumped over the Lazy Dog.The Early bird gets the worm.Never eat soggy waffles.Righty Tighty Lefty Loosey";

lcd0 = SerialWombatLiquidCrystal.SerialWombatLiquidCrystal(sw, 18, 19, 17, 16,15, 14)
q = SerialWombatQueue.SerialWombatQueue(sw)

def setup():
	#put your setup code here, to run once:
	sw.begin()

	lcd0.begin(20, 4)
  
	lcd0.setRowOffsets(0, 0x40, 0x14, 0x54)
	lcd0.initializeBufferCopy(8, 20)
 

	q.begin(0, 80, SerialWombatQueue.SerialWombatQueueType.QUEUE_TYPE_RAM_BYTE_SHIFT)

i = 0
def loop():
	global i
	# put your main code here, to run repeatedly:
	q.write(testString[i])
	delay(250)
	i += 1
	if (i >= len(testString)):
		i = 0

setup()
while(True):
    loop()

