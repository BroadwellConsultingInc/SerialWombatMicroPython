
import SerialWombat
import SerialWombatWS2812
import SerialWombatAnalogInput
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

WS2812_PIN =  15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS =  16
WS2812_USER_BUFFER_INDEX =  0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.


ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
pot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)





#Config:  What data source?  Comment in one
#DATA_SOURCE  = 0 #SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_PIN_0
DATA_SOURCE  = 67# SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW # Increments every 1ms
# DATA_SOURCE = 70 # SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_TEMPERATURE


def setup():
  # put your setup code here, to run once:
  
  
 
  sw.begin()

  pot.begin(0,64,0)
  ws2812.begin(WS2812_PIN,
    NUMBER_OF_LEDS,
    WS2812_USER_BUFFER_INDEX)

  ws2812.barGraph(DATA_SOURCE,
    0x00050000,   # Off value = dim red
    0x00000020,   # on value = blue
    1000,         # Min value 1000
    64000);       # Max value 64000


def loop():
  pass
  # No code in here.  


setup() #Run Setup
while (True):
    loop()  #Run Loop
