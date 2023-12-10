"""
This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the 
Serial Wombat 18AB chip'sSerialWombatMatrixKeypad class, and add a queue mask
to allow only certain digits to be entered in the queue

Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
button presses.

This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13 
and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin 
statement to fit your circuit.

This example uses default modes for the SerialWombatMatrixKeypad.  The default values 
send ASCII to the queue assuming a standard 

123A
456B
789C
*0#D

keypad format.   See the pin mode documentation (link below) for more information on the 
possible buffer and queue modes It is assumed that the Serial Wombat chip is at I2C 
address 0x6B.


A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
https://youtu.be/hxLda6lBWNg

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details

"""
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

import SerialWombatMatrixKeypad
import SerialWombatTM1637

keypad = SerialWombatMatrixKeypad.SerialWombatMatrixKeypad(sw)
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)

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

  keypad.writeQueueMask(0x2777); # Bit mask with 1's for positions 0,1,2,4,5,6,8,9,0,13 corresponding to keypad marked positions 0-9.

  myDisplay.begin(1,  #Clk Pin
                  2, #Data Pin
                  6, # Number of digits
                  2, # SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, # Mode enumeration
                  0x55, # Source pin Not used in tm1637CharArray mode
                  4);   # Brightness
  myDisplay.writeDigitOrder(2, 1, 0, 5, 4, 3);


def loop():

  i = keypad.read() # returns a byte, or -1 if no value is avaialble
  if (i >0):
    myDisplay.write(i );  # We got a keypress.  Dump it to the Display
  
setup()
while (True):
    loop()