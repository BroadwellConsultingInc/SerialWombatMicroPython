PENNY_PIN = 0  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 19 #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19


"""
  This example shows how to configure two Serial Wombat 18AB pins to Touch input and use the
  SerialWombat18CapTouchCounter class to implement a two touch sensor interface to increment
  a counter at various speeds by two different increments.

  The example was created using a Serial Wombat 18AB chip in I2C mode with a Node MCU clone Arduino
  and a penny and quarter both covered with electrial tape wired to pins WP16 and WP17.

  When the penny is touched briefly the total will increment by 1 cent.  When the quarter is touched
  the total will increment by 25 cents.  If a finger is held on them then they will increment slowly, then
  more quickly, then very quickly.  This type of interface could be easily integrated into a complete solution
  for user configuration of parameters.

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


DIGIT_PIN = 0  #Touch Sensor Pin
INCREMENT_PIN = 19 #Touch Sensor Pin
DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin


import SerialWombatTM1637
import SerialWombat18CapTouch
import SerialWombatDebouncedInput
from ArduinoFunctions import delay

myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
digit = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
increment = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
incrementCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(increment)

displayString = [0x30,0x30,0x30,0x30,0x30,0x30]
currentDigit = 6  # 6 means none, 0-5 are the displayed digits

def setup():
 # put your setup code here, to run once:
  sw.begin()



  # Initialize the digit sensor
  #9000 based on previous calibration of this pin with this wire using the Calibration example
  digit.begin(DIGIT_PIN, 9000, 0)

  # Initialize the Penny sensor
  #9250 based on previous calibration of this pin with this wire using the Calibration example
  increment.begin(INCREMENT_PIN, 9250, 0)

  delay(500)

  digit.makeDigital(53985, 57620, 1, 0, 0, 0); #Low and High limits based on previous calibration of this pin 
  increment.makeDigital(54349, 57792, 1, 0, 0, 0); #Low and High limits based on previous calibration of pin 
  delay(250)

  incrementCounter.begin(1,  #Increment by 1
                       500,#Every 500 ms
                       2000, # for 2000ms, then...
                       1,  # by 1
                       250, # every 250ms
                       5000, # for 5000 ms, then
                       1,    # by 1
                       100); # every 100ms


  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN, # Data Pin
  4, # Number of digits
  2, #SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, # Mode enumeration
  0x55, # Source pin Not used in tm1637CharArray mode
  4);   # Brightness 
  #myDisplay.writeDigitOrder(2,1,0,5,4,3)
  myDisplay.writeArray(displayString)


def nextDigit():
  global currentDigit
  currentDigit += 1
  if (currentDigit > 6):
    currentDigit = 0

  if (currentDigit < 6):
    
      myDisplay.writeBlinkBitmap(0x01 << currentDigit); # Update which digit blinks
      
  elif (currentDigit == 6):
      myDisplay.writeBlinkBitmap(0) # Turn off blinking.
  else:
      myDisplay.writeBlinkBitmap(0) # Turn off blinking.      


def loop():


  if (digit.readTransitionsState() and digit.transitions > 0):

    # The digit was touched.  Move to next digit
    nextDigit()


 
  if (currentDigit < 6 ):
    state, displayString[currentDigit] = incrementCounter.update(displayString[currentDigit]) 
    if (displayString[currentDigit] > ord('z')):
      displayString[currentDigit] = ord(' ')
   
    if (displayString[currentDigit] < ord(' ')):
      displayString[currentDigit] = ord('z')

  myDisplay.writeArray(displayString);


setup()
while(True):
    loop()