"""
This example shows how to use the writeDecimalBitmap command to write decimal points on a TM1637 display.
When properly configured with a properly wired display it will light up the decimal points in a binary-counting
fashion, with the left-most digit changing state most frequenly.

If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.

There is a good chance that this example will not work as expected.  The manufacturers of hobbiest TM1637
displays often do not connect the decimal point line as expected.  In some cases it may be connected to 
one or both of the dots in a colon ':' for time display.  In other conditions it may be connected incorrectly
or not at all.

This sketch and the writeDecimalBitmap has been verified to work properly on  properly wired TM1637 6-digit and
4-digit display.  If it behaves oddly on your display, it's probably your display.  The most popular 4 digit TM1637
display on Amazon from diymore as of October 2021 connects a colon rather than decimals.  The most popular 6 digit display from
diymore has a couple of decimal points connected and the remainder cause the display to malfunction when set.

A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
https://youtu.be/AwW12n6o_T0

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details

Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
"""

DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin

import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombatUART
import SerialWombatTM1637
from ArduinoFunctions import delay

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)

DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin

def setup():
  # put your setup code here, to run once:
  sw.begin()

  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN, # Data Pin
  6, # Number of digits
  SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, # Mode enumeration
  0x55, # Source pin Not used in tm1637CharArray mode
  4);   # Brightness 
  myDisplay.writeDigitOrder(2,1,0,5,4,3)

  test = "      ".encode('ascii')
  myDisplay.writeArray(test)

count = 0
def loop():
  global count
  myDisplay.writeDecimalBitmap(count)
  count += 1
  if (count >= 0x40):
    count = 0
  delay(250)

setup()
while(True):
    loop()

