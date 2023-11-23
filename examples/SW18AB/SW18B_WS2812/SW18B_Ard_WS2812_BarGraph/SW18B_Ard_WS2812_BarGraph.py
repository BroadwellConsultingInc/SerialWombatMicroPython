import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombat
import SerialWombatUART
import SerialWombatWS2812
import SerialWombatAnalogInput
from ArduinoFunctions import delay

WS2812_PIN =  15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS =  16
WS2812_USER_BUFFER_INDEX =  0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
pot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)





#Config:  What data source?  Comment in one
#DATA_SOURCE  = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_PIN_0
DATA_SOURCE  = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW # Increments every 1ms
# DATA_SOURCE = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_TEMPERATURE


def setup():
  # put your setup code here, to run once:
  
  
 
  sw.begin()

  pot.begin(0,64,0)
  ws2812.begin(WS2812_PIN,
    NUMBER_OF_LEDS,
    WS2812_USER_BUFFER_INDEX)

  ws2812.barGraph(DATA_SOURCE,
    0x00050000,   # Off value = dim red
    0x00000020,   # on value = blue
    1000,         # Min value 1000
    64000);       # Max value 64000


def loop():
  pass
  # No code in here.  


setup() #Run Setup
while (True):
    loop()  #Run Loop
