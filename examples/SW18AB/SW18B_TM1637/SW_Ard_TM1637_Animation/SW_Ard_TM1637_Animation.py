"""
This example shows how to display an animation on a TM1637 display.  The animation is loaded to the Serial Wombat 18AB chip
from the Arduino board.  The Serial Wombat chip then outputs the animation to the display without any intervention from
the Arduino board.

If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
4 digit displays should use settings to display 0123 in that test to work properly with this sketch.

You can choose an animation to show by commenting in one of the options below //CONFIG:

A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
https://youtu.be/AwW12n6o_T0

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details

Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
"""

DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin

import SerialWombat
from ArduinoFunctions import delay

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the paramter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")


#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
#import machine
#import SerialWombat_mp_i2c
#sclPin = 22
#sdaPin = 21
#swI2Caddress = 0x6B
#i2c = machine.I2C(0,
#            scl=machine.Pin(sclPin),
#            sda=machine.Pin(sdaPin),
#            freq=100000,timeout = 50000)
#sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
#sw.address = 0x6B

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
import machine
import SerialWombat_mp_UART
txPin = 12
rxPin = 14
UARTnum = 2
uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)


#Interface independent code starts here:
import SerialWombatTM1637
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)






#CONFIG:
#SPEED =  1000  # Slow -  delay 1000mS after updates
SPEED =  100  # Medium - delay 100mS after updates
#SPEED  = 10  # Fast -   delay 10ms after updates


SEG_A = 0x1 #TOP 
SEG_B = 0x2 # UPPER RIGHT
SEG_C = 0x4 # BOTTOM RIGHT
SEG_D = 0x8 # BOTTOM
SEG_E = 0x10 #BOTTOM LEFT
SEG_F = 0x20 #TOP LEFT
SEG_G = 0x40 # CENTER
SEG_POINT = 0x80
OFF__ = 0



VERTRIGHT = (SEG_B | SEG_C)
VERTLEFT =  (SEG_E | SEG_F)
TOP = (SEG_A)
MID = (SEG_G)
BOT = (SEG_D)

LeftToRight = [ [VERTLEFT, 0,0,0,0,0],  #All arrays are 6 bytes wide, regardless of display width.
  [VERTRIGHT, 0,0,0,0,0],
  [0,VERTLEFT, 0,0,0,0],
  [0,VERTRIGHT, 0,0,0,0],
  [0,0,VERTLEFT, 0,0,0],
  [0,0,VERTRIGHT, 0,0,0],
  [0,0,0,VERTLEFT, 0,0],
  [0,0,0,VERTRIGHT, 0,0],
  [0,0,0,0,VERTLEFT, 0],
  [0,0,0,0,VERTRIGHT, 0],
  [0,0,0,0,0,VERTLEFT ],
  [0,0,0,0,0,VERTRIGHT],
  [0,0,0,0,0,0],            # putting multiple frames the same in looks like a delay
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0]]
   
snake_6_digit =[ [TOP,0,0,0,0,0],
  [0,TOP,0,0,0,0],
  [0,0,TOP,0,0,0],
  [0,0,0,TOP,0,0],
  [0,0,0,0,TOP,0],
  [0,0,0,0,0,TOP],

  [0,0,0,0,0,SEG_B],

  [0,0,0,0,0,MID],
  [0,0,0,0,MID,0],
  [0,0,0,MID,0,0],
  [0,0,MID,0,0,0],
  [0,MID,0,0,0,0],
  [MID,0,0,0,0,0],

  [SEG_E,0,0,0,0,0],

  [BOT,0,0,0,0,0],
  [0,BOT,0,0,0,0],
  [0,0,BOT,0,0,0],
  [0,0,0,BOT,0,0],
  [0,0,0,0,BOT,0],
  [0,0,0,0,0,BOT],

  [0,0,0,0,0,SEG_C],

  [0,0,0,0,0,MID],
  [0,0,0,0,MID,0],
  [0,0,0,MID,0,0],
  [0,0,MID,0,0,0],
  [0,MID,0,0,0,0],
  [MID,0,0,0,0,0],

  [SEG_F,0,0,0,0,0]]


snake_4_digit = [ [TOP,0,0,0,0,0],
  [0,TOP,0,0,0,0],
  [0,0,TOP,0,0,0],
  [0,0,0,TOP,0,0],

  [0,0,0,SEG_B,0,0],

  [0,0,0,MID,0,0],
  [0,0,MID,0,0,0],
  [0,MID,0,0,0,0],
  [MID,0,0,0,0,0],

  [SEG_E,0,0,0,0,0],

  [BOT,0,0,0,0,0],
  [0,BOT,0,0,0,0],
  [0,0,BOT,0,0,0],
  [0,0,0,BOT,0,0],

  [0,0,0,SEG_C,0,0],

  [0,0,0,MID,0,0],
  [0,0,MID,0,0,0],
  [0,MID,0,0,0,0],
  [MID,0,0,0,0,0],

  [SEG_F,0,0,0,0,0]]

# CONFIG: pick one
#ANIMATION_ARRAY = snake_6_digit
ANIMATION_ARRAY = snake_4_digit
#ANIMATION_ARRAY =  LeftToRight

def setup():
 # put your setup code here, to run once:
  sw.begin()

  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN, # Data Pin
  6, # Number of digits
  4, #SerialWombatTM1637.SWTM1637Mode.tm1637Animation, # Mode enumeration
  0x55, # Source pin Not used in tm1637CharArray mode
  4);   # Brightness 
  #myDisplay.writeDigitOrder(2,1,0,5,4,3)

  

  
  myDisplay.writeAnimation(0x180, # Place array at index 0x180 in the user buffer
        SPEED,
        len(ANIMATION_ARRAY),  #Number of frames.  Suggest using sizeof like this to calculate.
        ANIMATION_ARRAY); # Array to load.

def loop():
  pass

setup()
while(True):
    loop()
