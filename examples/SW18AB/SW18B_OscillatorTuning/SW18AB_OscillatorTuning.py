"""
This example shows how to tune the Serial Wombat 18AB chip's internal FRC oscillator against 
the host's millis() function to reduce the error in the FRC from as much as +/- 1.5% at room
temperature to less than 0.1% .

This sketch runs for 1 minute to profile and display the nominal error in the FRC vs. millis()
then begins calling the update function of SerialWombat18ABOscillatorTuner.  The system then displays
the improvement in accurary as the oscillator is tuned.

A video demonstrating the use of the SerialWombat18ABOscillatorTuner class on the Serial Wombat 18AB chip is available at:
TBD

Documentation for the SerialWombat18ABOscillatorTuner Arduino class is available at:
TBD

"""

import SerialWombat
from ArduinoFunctions import delay
from ArduinoFunctions import millis

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the paramter of SerialWombatChip_cpy_serial to match the name of your Serial port
import SerialWombat_cpy_serial
sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")


#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
#import machine
#import SerialWombat_mp_i2c
#sclPin = 21
#sdaPin = 20
#swI2Caddress = 0x6B
#i2c = machine.I2C(0,
#            scl=machine.Pin(sclPin),
#            sda=machine.Pin(sdaPin),
#            freq=100000,timeout = 50000)
#sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
#sw.address = 0x6B

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

oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)

millisStart = 0
framesStart = 0
nextUpdate = 0; 

def setup():
  global framesStart
  global millisStart
  global nextUpdate
  # put your setup code here, to run once:
  sw.begin()
  framesStartmsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
  framesStartlsb = sw.readPublicData(SerialWombat.SerialWombatDataSourcelSW_DATA_SOURCE_FRAMES_RUN_LSW)
  if (framesStartmsb != sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)):
  
   framesStartlsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW);
   framesStartmsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW); 
  
  framesStart = framesStartmsb <<16;
  framesStart += framesStartlsb;
  millisStart = millis()
  nextUpdate = millis() + 60000

  print("System will test Serial Wombat frame count for 1 minute, then start tuning algorithm, and show results every minute.")



# In the loop we will constantly read the I2C value, and print it to Serial When it changes
def loop(): 
        global framesStart
        global millisStart
        global nextUpdate
        # put your main code here, to run repeatedly:
        m = millis()
        if (m > nextUpdate):
        
                frameslsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
                frames = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
                if (frames != sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)):
                        frameslsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
                        frames = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
                frames <<= 16
                frames += frameslsb
                print (f"millis elapsed: {(m - millisStart)} frames run: {(frames-framesStart)}  d: {(m - millisStart) - (frames-framesStart)} % (+ is SW too slow): {((m - millisStart) - (frames-framesStart)) / (m - millisStart) * 100}")
                nextUpdate = millis() + 60000
                framesStart = frames
                millisStart = m
        if (millis() > 70000):
                oscTun.update();  # Start tuning after the first minute.
	

setup()
while(True):
    loop()

