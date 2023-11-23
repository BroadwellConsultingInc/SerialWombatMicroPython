"""
This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the 
Serial Wombat 18AB chip's SerialWombatMatrixKeypad class.

Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
button presses.

This example shows how to treat the matrix keypad as if it were 16 separate digital
inputs by creating 16 instances of SerialWombatMatrixButton from a single instance of
SerialWombatMatrixKeypad.  The SerialWombatMatrixKeypad instance scans the keys and
the SerialWombatMatrixButton class abstracts each one into a single digital input.

After initialization the SerialWombatMatrixButton class has the same interfaces and 
is conceptually interchangable with instances of SerialWombatDebouncedInput and 
digitally configured SerialWombat18CapTouch instances.

This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13 
and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin 
statement to fit your circuit.

A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
https://youtu.be/hxLda6lBWNg 

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details

"""

import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombatUART
import SerialWombatMatrixKeypad

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
keypad = SerialWombatMatrixKeypad.SerialWombatMatrixKeypad(sw)
button0 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,0)
button1 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,1)
button2 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,2)
button3 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,3)
button4 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,4)
button5 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,5)
button6 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,6)
button7 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,7)
button8 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,8)
button9 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,9)
button10 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,10)
button11 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,11)
button12 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,12)
button13 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,13)
button14 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,14)
button15 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,15)

def setup():
  sw.begin()
  keypad.begin(10, # Command pin, typically the same as the row0 pin
  10, #row 0
  11, # row 1
  12, # row 2
  13, # row 3
  16, # column 0
  17, # column 1
  18, # column 2
  19); # column 3

def loop():
	# put your main code here, to run repeatedly:
	
	# If any of the 16 keys is pressed, print its index number.
  if (button0.digitalRead()):
    print("0 ", end = " ")
  if (button1.digitalRead()):
    print("1 ", end = " ")
  if (button2.digitalRead()):
    print("2 ", end = " ")
  if (button3.digitalRead()):
    print("3 ", end = " ")
  if (button4.digitalRead()):
    print("4 ", end = " ")
  if (button5.digitalRead()):
    print("5 ", end = " ")
  if (button6.digitalRead()):
    print("6 ", end = " ")
  if (button7.digitalRead()):
    print("7 ", end = " ")
  if (button8.digitalRead()):
    print("8 ", end = " ")
  if (button9.digitalRead()):
    print("9 ", end = " ")
  if (button10.digitalRead()):
    print("10 ", end = " ")
  if (button11.digitalRead()):
    print("11 ", end = " ")
  if (button12.digitalRead()):
    print("12 ", end = " ")
  if (button13.digitalRead()):
    print("13 ", end = " ")
  if (button14.digitalRead()):
    print("14 ", end = " ")
  if (button15.digitalRead()):
    print("15 ", end = " ")

  #Print how many times the lower right key has been pressed or released
  print(button15.transitions, end = " ");  

  #Print how long the lower right key has been held down (0 if not pressed)
  print(button15.readDurationInTrueState_mS())

setup()
while(True):
    loop()
