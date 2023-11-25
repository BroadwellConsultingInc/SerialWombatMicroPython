"""
This example shows how to configure two pins to work together to drive a TM1637 seven-segment
LED display with a Serial Wombat 18AB chip.

The goal of this example is to display "012345" on the display.  Ideally, "012345" will be displayed
on a 6-segment display, and "0123" will be displayed on a 4 digit display.

However, some displays may have the digits connected to the display in a different order than expected.
For instance, the 6 segment diymore display I bought on Amazon in September of 2021 displayed "210543"
indicating that each of the 3-segment LED displays used to make up the 6 digits was wired backwards.

In the example below, note the call to writeDigitOrder().  This function is used to correct digit order.
Simply enter the number displayed on the display by default as parameters and the display will show
correctly.  For example for the diymore display:
writeDigitalOrder(2,1,0,5,4,3);

A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
https://youtu.be/AwW12n6o_T0

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
"""



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
DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)


def setup():
  # put your setup code here, to run once:
  sw.begin()

  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN, # Data Pin
  6, # Number of digits
  2, # SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, # Mode enumeration
  0x55, # Source pin Not used in tm1637CharArray mode
  4);   # Brightness 
  #myDisplay.writeDigitOrder(2,1,0,5,4,3)


  test = "012345".encode('ascii')
  myDisplay.writeArray(test)


  
def loop():
  pass

setup()
while(True):
    loop()



