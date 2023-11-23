"""
This example shows how to configure a Serial Wombat 18AB pin to Touch input and determine working
calibration constants for the touch sensor.

SerialWombat18CapTouch class documentation can be found here:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details


NOTE!   VERSION 2.0.5 of the SW18AB firmware has a bug which prevents configuration of digital mode for the
Touch input.  You must upgrade if you have version 2.0.5 and want to use this feature.


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
from ArduinoFunctions import delay
from ArduinoFunctions import millis


TOUCH_PIN  =  19      #<<<<<< MODIFY THIS BASED ON WHICH PIN YOUR TOUCH SENSOR IS RUNNING ON
ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
capTouch = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)

lastDigitalRead = 0

def setup():
  delay(5000)

  sw.begin()


  delay(1000)

  sw.queryVersion()

  if (sw.fwVersion[0] == '2' and sw.fwVersion[1] == '0' and sw.fwVersion[2] == '5'):
    
    print("Firmware Version 2.0.5 detected.  This version has a bug which prevents transition from analog to digital touch reporting.  Update firmware to latest version (Tutorial video: https://youtu.be/q7ls-lMaL80  )");
    while (True):
        delay(100)
      
    

  #Iterate through increasing amounts of charge until we find a value that 90% saturates the sensor.
  print("Determining charge time.  Do not touch the sensor.")

  noTouchReading = 0
  chargeTime = 250
  capTouch.begin(TOUCH_PIN,chargeTime,0)
  delay(500)
  noTouchReading = sw.readPublicData(TOUCH_PIN)

  while (noTouchReading < 60000):
    if (noTouchReading < 30000):
      chargeTime += 250
    else:
      chargeTime += 250

    capTouch.begin(TOUCH_PIN,chargeTime,20)
    delay(500)
    noTouchReading = sw.readPublicData(TOUCH_PIN)
    print(f"{chargeTime} : {noTouchReading}")
    
  recommendedChargeTime = chargeTime

  print(f"Recommended charge time: {recommendedChargeTime}")


  # Now take a bunch of samples at that charge to see how much varation you get.  Find the
  # smallest returned value over 5 seconds.
  print("Calibrating High Limit...")
  HighLimit = 65535
  start = millis()
  while (start + 5000 > millis()):
    result = sw.readPublicData(TOUCH_PIN)

    if (result < HighLimit):
      HighLimit = result
      print(HighLimit)
    delay(0)



  print("Lightly Hold finger on sensor until told to remove...")
  # Wait for the user to touch the sensor  
  while (sw.readPublicData(TOUCH_PIN) > HighLimit - 1500):
    delay(250)
    print(".")
  print()


  #Now take 5 seconds worth of samples to determine the maximum value you're likely to see
  # while touched.
  LowLimit = 0
  start = millis()
  while (start + 5000 > millis()):
    result = sw.readPublicData(TOUCH_PIN)

    if (result > LowLimit):
      LowLimit = result
      print(LowLimit)


  print("Remove Finger.")
  print("Recommended charge time: ")
  print(recommendedChargeTime)
  print("Recommended High Limit: ")
  print (LowLimit + (HighLimit - LowLimit)*3 // 4)  
  print("Recommended Low Limit: ")
  print(LowLimit + (HighLimit - LowLimit) // 4) 

  print("Done.")

  print()
 # print("Configuring Touch in digital mode using calibrations.  Code is:");
  print()
#  print(" capTouch.begin(TOUCH_PIN,");Serial.print(recommendedChargeTime);Serial.println(",0);")
#  print("capTouch.makeDigital("); Serial.print(LowLimit);Serial.print(",");Serial.print(HighLimit);Serial.println(",1,0,0,0);")
  print()

  capTouch.makeDigital(LowLimit,HighLimit,1,0,0,0)
  delay(250)
  lastDigitalRead = sw.readPublicData(TOUCH_PIN)
  

count = 0
#In the loop look for a change in state on the sensor and print a 0 or 1
def loop():
  global lastDigitalRead
  global count

  newValue = sw.readPublicData(TOUCH_PIN);
  if (newValue != lastDigitalRead):
    print(newValue); 
    print(" ")
    lastDigitalRead = newValue

    count += 1
    if (count > 20):
      count = 0
      print()


setup() #Run Setup
while (True):
    loop()  #Run Loop
  
