"""
This example shows how to configure two pins to work together to connect to an IBM PS2 Keyboard.

This example assumes a Serial Wombat 18AB chip is attached to the Arduino board via I2C.

The goal of this example is to read keystrokes in ASCII from the Keyboard / Serial Wombat 18AB chip and output it 
to serial.

Keyboard data and clock lines should be pulled up to +5v using a 2k resistor.  5V tollerant pins (9-12, 14, 15) should 
be used.

A video demonstrating the use of the PS2 Keyboard pin mode on the Serial Wombat 18AB chip is available at:
TODO

Documentation for the SerialWombatTM1637 Arduino class is available at:
TODO
"""

import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombatUART
import SerialWombatPS2Keyboard

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
myKeyboard = SerialWombatPS2Keyboard.SerialWombatPS2Keyboard(sw)



PS2_CLK_PIN = 10  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Clock Pin
PS2_DATA_PIN = 11  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Data Pin

def setup():
  # put your setup code here, to run once:
  
  sw.begin()

  myKeyboard.begin(PS2_CLK_PIN,  #Clk Pin
  PS2_DATA_PIN)   # Data Pin 

def loop():

  x = myKeyboard.read()  # Read the keyboard queue.  Returns -1 if no characters available
  while (x > 0):
    c = chr(x)  # Convert the value to a character
    print(c)    # Send the character to the serial interface
    x = myKeyboard.read() # Read the keyboard queue.  Returns -1 if no characters available


setup()
while(True):
    loop()

