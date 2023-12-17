"""
This example builds on Example 1.  It sets the Serial Wombat Input Processor to average 100 pulses, and return that average.

Serial Wombat 18AB Firmware 2.1 or later is needed to use this example.

An HC_SR04 sensor needs to be powered by 5V, and outputs a 5V signal.  The echo pin should be connected to one of the 
Serial Wombat 18AB chip's 5V tolerant pins (9,10,11,12, 14 and 15)


A video demonstrating the use of the UltrasonicDistanceSensor pin mode on the Serial Wombat 18AB chip is available at:
TODO

Documentation for the SerialWombatUltrasonicDistanceSensor class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_ultrasonic_distance_sensor.html
"""

import SerialWombat
from ArduinoFunctions import delay

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the paramter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")


#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
import machine
import SerialWombat_mp_i2c
sclPin = 21
sdaPin = 20
swI2Caddress = 0x6B
i2c = machine.I2C(0,
            scl=machine.Pin(sclPin),
            sda=machine.Pin(sdaPin),
            freq=100000,timeout = 50000)
sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
sw.address = 0x6B

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
#import machine
#import SerialWombat_mp_UART
#txPin = 12
#rxPin = 14
#UARTnum = 2
#uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
#sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)


#Interface independent code starts here:

import SerialWombatUltrasonicDistanceSensor
distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
  

def setup():
  # put your setup code here, to run once:
  sw.begin()
  distanceSensor.begin(10, # Echo pin is on pin 10
		        0, # HC_SR04 driver
			11) # Trigger pin on pin 11.    no parameters for autoTrigger (true) and pullUp (false)
  distanceSensor.writeAveragingNumberOfSamples(100); #Inherited from SerialWombatAbstractProcessedInput


lastMeasurement = 0;

# In the loop we will constantly read the I2C value, and print it to Serial When it changes
def loop(): 
  global lastMeasurement
  newMeasurement = distanceSensor.readAverage()
  if (newMeasurement != lastMeasurement):
   print(f"{newMeasurement} mm");
   lastMeasurement = newMeasurement;
	

setup()
while(True):
    loop()


