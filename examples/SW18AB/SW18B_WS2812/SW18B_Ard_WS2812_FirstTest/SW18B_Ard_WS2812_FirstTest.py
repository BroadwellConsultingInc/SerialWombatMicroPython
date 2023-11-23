#include "SerialWombat.h"

"""
This example shows how to initialize and test a strip/board of WS2812b or equivalent LEDs.  This sketch uses
the SerialWombat18AB's SerialWombatWS2812 class to configure a pin to drive the LEDs.  The
selected pin must be an enhanced performance pin.

When executed this sketch will configure the Serial Wombat chip to cycle through the indicated number of LEDs
on the strip in order in various colors.

Change the WS2812_PIN and NUMBER_OF_LEDSs below to fit your circuit.

A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
//TODO

Documentation for the SerialWombatTM1637 Arduino class is available at:
https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details

"""
import SerialWombat
import SerialWombat_mp_i2c
import SerialWombatWS2812
import machine


i2c = machine.I2C(0,
#RP2040              scl=machine.Pin(1),
#RP2040              sda=machine.Pin(0),
            scl=machine.Pin(22),
            sda=machine.Pin(21),
            freq=100000,timeout = 50000)


sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6B)
sw.address = 0x6B
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)

WS2812_PIN =  15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 16
WS2812_USER_BUFFER_INDEX =  0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.




def setup():
  sw.begin()
  #TODO delay(500);
  

  ws2812.begin(WS2812_PIN,
    NUMBER_OF_LEDS,
    WS2812_USER_BUFFER_INDEX);

  ws2812.writeMode( 2) # 2 = SerialWombatWS2812.SWWS2812Mode.ws2812ModeChase)


def loop() :
  # No code in here.  The Serial Wombat chip handles generating the LED sequence with no additional 
  # help from the host.  In fact, you could unplug the I2C lines and it would continue working until
  # powered down.
  pass

setup()
while (True):
    loop()