"""
This example shows how to configure pins 14-18 of the Serial Wombat 18AB chip to output VGA.
It changes the TFT Pong example from:
http://www.arduino.cc/en/Tutorial/TFTPong

To output VGA instead.  Some of the TFT calls are left in and commented out for reference.

Serial Wombat 18AB Firmware 2.1 or later is needed to use this example.

This example assumes a Serial Wombat 18AB chip is attached to the Arduino board via I2C.
In this case we're assuming an ESP-01 module with I2C Data and Clock lines on ESP-02 pins 2 and 0.

Since we only draw rectangles and that functionality is supported by the SerialWombat18ABVGA class,
there's no need to pull in the SerialWombat18ABVGADriver library and class and AdafruitGFX library.

Connections:
Potentiometers that divide VCC and Gnd to Serial Wombat pins 0 and 1.
VGA VSYNC (VGA Pin 14) -> 100 ohm Resistor -> SW Pin 18
VGA HSYNC (VGA Pin 13) -> 100 ohm Resistor ->SW Pin 17
VGA Red   (VGA Pin 1) -> 280 ohm Resistor -> SW Pin 16
VGA Green (VGA Pin 2) -> 280 ohm Resistor -> SW Pin 15
VGA Blue (VGA Pin 3) -> 280 ohm Resistor -> SW Pin 14

A video demonstrating the use of the VGA pin mode on the Serial Wombat 18AB chip is available at:
TODO

Documentation for the VGA class is available at:
TODO


The original TFT Pong Header:
  TFT Pong

  This example for the Arduino screen reads the values
  of 2 potentiometers to move a rectangular platform
  on the x and y axes. The platform can intersect
  with a ball causing it to bounce.


  http://www.arduino.cc/en/Tutorial/TFTPong

"""

import sys
import os

swPath = os.getcwd()
for i in range(4):
   swPath = os.path.dirname(swPath)

sys.path.append(swPath)   # Add the directory with SerialWombat.py to the path for import

import serial
import SerialWombatUART
import SerialWombat18ABVGA
import SerialWombatAnalogInput
from ArduinoFunctions import millis

ser = serial.Serial("COM19",115200,timeout = 0)
sw = SerialWombatUART.SerialWombatChipUART(ser)

vgaDriver = SerialWombat18ABVGA.SerialWombat18ABVGA(sw)
xInput = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
yInput = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)


# variables for the position of the ball and paddle
paddleX = 0
paddleY = 0
oldPaddleX = 0 
oldPaddleY = 0
ballDirectionX = 1
ballDirectionY = 1

ballSpeed = 50; # lower numbers are faster

nextBallMove = 0

ballX = 0
ballY = 0
oldBallX = 0
oldBallY = 0

def setup():
  # initialize the display
  

  xInput.begin(0)
  yInput.begin(1)
  vgaDriver.begin(18, 0x0000)
  nextBallMove = millis() + ballSpeed


def loop():
  global oldPaddleX
  global oldPaddleY
  global nextBallMove
  # save the width and height of the screen
  myWidth = 160;
  myHeight = 120;

  # map the paddle's location to the position of the potentiometers
  x = xInput.readAveragedCounts();
  y = yInput.readAveragedCounts();
  x *= myWidth
  y *= myHeight
  x >>= 16
  y >>= 16
  paddleX =  x - 20 // 2
  paddleY = y - 5 // 2

  # set the fill color to black and erase the previous
  # position of the paddle if different from present


  if (oldPaddleX != paddleX or oldPaddleY != paddleY):

    #TFTscreen.rect(oldPaddleX, oldPaddleY, 20, 5);
    vgaDriver.fillRect(oldPaddleX, oldPaddleY, 20, 5, 0);


  # draw the paddle on screen, save the current position
  # as the previous.
  vgaDriver.fillRect(paddleX, paddleY, 20, 5, 1)

  oldPaddleX = paddleX
  oldPaddleY = paddleY

  # update the ball's position and draw it on screen
  if (nextBallMove >= millis()):
    nextBallMove += ballSpeed
    moveBall()
  


# this function determines the ball's position on screen
def moveBall():
  # if the ball goes offscreen, reverse the direction:
  if (ballX > 160  or ballX < 0):
    ballDirectionX = -ballDirectionX


  if (ballY > 120 or ballY < 0) :
    ballDirectionY = -ballDirectionY
  

  # check if the ball and the paddle occupy the same space on screen
  if (inPaddle(ballX, ballY, paddleX, paddleY, 20, 5)):
    ballDirectionX = -ballDirectionX
    ballDirectionY = -ballDirectionY
  

  # update the ball's position
  ballX += ballDirectionX;
  ballY += ballDirectionY;

  # erase the ball's previous position
  if (oldBallX != ballX or oldBallY != ballY) :
    vgaDriver.fillRect(oldBallX, oldBallY, 5, 5, 0)


  # draw the ball's current position
  vgaDriver.fillRect(ballX, ballY, 5, 5, 1)

  # Draw a line across the top and bottom to show screen boundaries
  vgaDriver.fillRect(0, 0, 160, 1, 1)
  vgaDriver.fillRect(0, 119, 160, 1, 1)

  oldBallX = ballX
  oldBallY = ballY


# this function checks the position of the ball
# to see if it intersects with the paddle
def inPaddle( x,  y,  rectX,  rectY,  rectWidth,  rectHeight) :
  result = False

  if ((x >= rectX and x <= (rectX + rectWidth)) and
      (y >= rectY and y <= (rectY + rectHeight))):
    result = True
  

  return result

setup()
while(True):
    loop()