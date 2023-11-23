"""
This example shows how to initialize more than one WS2812 LED array.

Change the WS2812_PIN below to fit your circuit.

A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
https://youtu.be/WoXvLBJFpXk
The video targets Arduino, but the same interfaces are used in Python.

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
import SerialWombatWS2812
from ArduinoFunctions import delay


ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
ws2812_2 = SerialWombatWS2812.SerialWombatWS2812(sw)

WS2812_PIN =  15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS =  3
WS2812_USER_BUFFER_INDEX =  0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.


# Define colors.  prefix them with SW_ so we don't conflict with any other libraries, such as a graphic display library.
SW_RED =  0x000F0000   # Red, changed from 0x00FF0000 to reduce power
SW_GREEN =  0x0000F00
SW_WHITE =  0x000F0F0F
SW_YELLOW =  0x000F0F00
SW_BLUE =  0x0000000F
SW_OFF =  0x00000000
SW_PURPLE =  0x000F000F

NUMBER_OF_FRAMES =  3
Frames = [[SW_OFF,SW_OFF,SW_GREEN],
    [SW_OFF,SW_YELLOW,SW_OFF],
    [SW_RED,SW_OFF,SW_OFF]]
  





def setup():
  # put your setup code here, to run once:

  sw.begin()
  delay(500)

  ws2812.begin(WS2812_PIN,  # The Pin connected to WS2812 array
    NUMBER_OF_LEDS,         # The number of LEDs being used
    WS2812_USER_BUFFER_INDEX);  # A location in the Serial Wombat chip's user RAM area where LED output signals will be buffered

  offset = ws2812.readBufferSize();  # We have a second location in the Serial Wombat chip's user buffer.  This is where
                                               # The animation frames are stored.  The readBufferSize() method gets the length of
                                               # buffer used by the configured number of LEDs.

  ws2812.writeAnimationUserBufferIndex(WS2812_USER_BUFFER_INDEX + offset,  # Location in memory to store the animation frames, after the main WS2812 buffer
                                        NUMBER_OF_FRAMES );      # Number of frames


  for i in range(NUMBER_OF_FRAMES):
    ws2812.writeAnimationFrame(i,Frames[i]);    # Transfer the frame to the animation buffer on the Serial Wombat chip
    ws2812.writeAnimationFrameDelay(i,5000);# Initalize All Frames 5000 mS delay

    
  ws2812.writeAnimationFrameDelay(1,1000);#Make the yellow frame (index 1 )  only 1000 mS instead of 5000.

  ws2812.writeMode(SerialWombatWS2812.SWWS2812Mode.ws2812ModeAnimation)

  ws2812_2.begin(14,16,2000)
  ws2812_2.writeMode(SerialWombatWS2812.SWWS2812Mode.ws2812ModeChase)



def loop():
  pass
  # No code in here.  The Serial Wombat chip handles generating the LED sequence with no additional 
  # help from the Arduino.  In fact, you could unplug the I2C lines and it would continue working until
  # powered down.


setup() #Run Setup
while (True):
    loop()  #Run Loop
#include "SerialWombat.h"




