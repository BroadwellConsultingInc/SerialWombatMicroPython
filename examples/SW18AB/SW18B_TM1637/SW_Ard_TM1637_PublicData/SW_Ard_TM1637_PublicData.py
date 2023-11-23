"""
This example shows how to display a number on a TM1637 display based on the public data of a Serial Wombat pin or other
data source within the Serial Wombat chip.

If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
For four digit displays, you'll likely want to use writeDigitOrder(2,3,4,5,0,1) in order to show the least
significant digits.

This sketch assumes a potentiometer output dividing ground and 3.3v  is connected to pin 0 as an analog input.

This sketch is designed to be experimented with.  Comment in #define's in the  CONFIG sections below to try out different options and how they affect the display

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
import SerialWombat
import SerialWombatUART
import SerialWombatTM1637
import SerialWombatAnalogInput
ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)

potentiometer = SerialWombatAnalogInput.SerialWombatAnalogInput (sw)

DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
#CONFIG:  Which mode... Hex or decimal?  Comment in one...
TM1637_MODE = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
#TM1637_MODE  = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16


#Config:  What data source?  Comment in one
#DATA_SOURCE = SW_DATA_SOURCE_PIN_0
DATA_SOURCE = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_INCREMENTING_NUMBER
#DATA_SOURCE =  SW_DATA_SOURCE_TEMPERATURE


#Config:  blank leading zeros?   Make True or false
SURPRESS_LEADING_ZEROS = True


def setup():
  # put your setup code here, to run once:
  sw.begin()

  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN, # Data Pin
  6, # Number of digits
  TM1637_MODE, # Mode enumeration
  DATA_SOURCE, # Source pin 
  4)   # Brightness 
  myDisplay.writeDigitOrder(2,1,0,5,4,3)


  myDisplay.suppressLeadingZeros(SURPRESS_LEADING_ZEROS);

  potentiometer.begin(0,64,0);


def loop():
  pass

setup()
while(True):
    loop()

