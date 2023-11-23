"""
This example shows how to configure two Serial Wombat 18AB pins to Touch input and use the
SerialWombat18CapTouchCounter class to implement a two touch sensor interface to increment
a counter at various speeds by two different increments.

The example was created using a Serial Wombat 18AB chip in I2C mode with a Node MCU clone Arduino
and a penny and quarter both covered with electrial tape wired to pins WP16 and WP17.  

When the penny is touched briefly the total will increment by 1 cent.  When the quarter is touched
the total will increment by 25 cents.  If a finger is held on them then they will increment slowly, then
more quickly, then very quickly.  This type of interface could be easily integrated into a complete solution
for user configuration of parameters.

SerialWombat18CapTouch class documentation can be found here:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details

A demonstration video of this class can be found here:
https://youtu.be/c4B0_DRVHs0

"""
import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombat
import SerialWombatUART
import SerialWombat18CapTouch
import SerialWombatDebouncedInput
from ArduinoFunctions import delay
from ArduinoFunctions import millis

PENNY_PIN = 0  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 19 #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
penny = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarter = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)


quarterCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(quarter)
pennyCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(penny)


moneyCount = 0  #Place to keep track of total money count in pennies

def setup():
  sw.begin()


  delay(1000)

  sw.queryVersion()

  if (sw.fwVersion[0] == '2' and sw.fwVersion[1] == '0' and sw.fwVersion[2] == '5'):
    
    print("Firmware Version 2.0.5 detected.  This version has a bug which prevents transition from analog to digital touch reporting.  Update firmware to latest version (Tutorial video: https://youtu.be/q7ls-lMaL80  )");
    while (True):
        delay(100)

  # Initialize the Penny sensor
  #9000 based on previous calibration of this penny on this pin with this wire using the Calibration example
  penny.begin(PENNY_PIN,9000,0);  

  # Initialize the Penny sensor
  #9250 based on previous calibration of this quarter on this pin with this wire using the Calibration example
  quarter.begin(QUARTER_PIN,9250,0)
     
  delay(500)
  
  penny.makeDigital(53985,57620,1,0,0,0);#Low and High limits based on previous calibration of this penny on this pin with this wire
  quarter.makeDigital(54349,57792,1,0,0,0);#Low and High limits based on previous calibration of this quarter on this pin with this wire
  delay(250)

  pennyCounter.begin(    1, #Increment by 1
    500,#Every 500 ms 
    2000, # for 2000ms, then...
    1,  # by 1 
    250, # every 250ms 
    5000, # for 5000 ms, then
    1,    # by 1
    100) # every 100ms

    #Initialization of the quarter Counter is the same, but incrments by 25.
  quarterCounter.begin(25,500,2000,25,250,5000,25,100)

  print("Touch or hold the penny or the quarter:")



lastCount = -1;  # A copy of moneyCount so we can send a Serial update on changes.
def loop():
  global moneyCount
  global lastCount
  pressed, moneyCount = quarterCounter.update(moneyCount);  #Service the counter periodically
  pressed, moneyCount = pennyCounter.update(moneyCount);    #Serivce the counter periodically
  
  if (lastCount != moneyCount):  # Did the counter change the moneyCount variable?

    #Yes, the counter changed
    lastCount = moneyCount;  #Make a copy for comparison

    #Then build a string and send it.
    
    print(f"{moneyCount // 100}.{ moneyCount%100:02}");

setup() #Run Setup
while (True):
    loop()  #Run Loop
