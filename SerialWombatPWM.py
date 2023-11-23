"""
Copyright 2020-2021 Broadwell Consulting Inc.

"Serial Wombat" is a registered trademark of Broadwell Consulting Inc. in
the United States.  See SerialWombat.com for usage guidance.

Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
"""


#include <stdint.h>
#include "SerialWombat.h"
"""! @file SerialWombatPWM.h
"""
import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE32
#from enum import IntEnum
from SerialWombatAbstractScaledOutput import SerialWombatAbstractScaledOutput
"""
class Wombat4A_B_PWMFrequencyValues_t(IntEnum):
    SW4AB_PWMFrequency_1_Hz = 0x76
    SW4AB_PWMFrequency_2_Hz = 0x66
    SW4AB_PWMFrequency_4_Hz = 0x56
    SW4AB_PWMFrequency_8_Hz = 0x46
    SW4AB_PWMFrequency_16_Hz = 0x75
    SW4AB_PWMFrequency_32_Hz = 0x65
    SW4AB_PWMFrequency_63_Hz = 0x55
    SW4AB_PWMFrequency_125_Hz = 0x45
    SW4AB_PWMFrequency_244_Hz = 0x71
    SW4AB_PWMFrequency_488_Hz = 0x61
    SW4AB_PWMFrequency_976_Hz = 0x51
    SW4AB_PWMFrequency_1952_Hz = 0x41
    SW4AB_PWMFrequency_3900_Hz = 0x31
    SW4AB_PWMFrequency_7800_Hz = 0x21
    SW4AB_PWMFrequency_15625_Hz = 0x11
    SW4AB_PWMFrequency_31250_Hz = 0x01
"""

"""!
@brief A class representing a Serial Wombat PWM output

An instance of this class should be declared for each pin
to be used as a Serial Wombat PWM.  

SW4A / SW4B PWMs are initialized to a frequency of 31250 Hz at startup.
This frequency can be changed using the setFrequency_SW4AB method.
All PWM outputs use the same clock divider, so a change in frequency
to one PWM output will affect other outputs.

SW4A/4B PWM inputs are either 8 or 10 bit resolution, depending on frequency
selection.  The duty cycle parameter of methods that set duty cycle
take a 16 bit value ranging from 0 to 65535 as an input regardless of
resolution, with 0 being
always low, and 65535 being always high.

Serial Wombat 18AB PWM outputs are driven either by hardware peripherals
or by a DMA based software PWM scheme.  Up to 6 hardware PWM outputs are avaialble
on Enhanced Digital Performance pins (0-4,7,9-19).  The first six Enhanced Digitial
Performance pins configured after reset will claim hardware resources.  Any additional
pins configured for PWM will use DMA based output.  Hardware capable pins can 
generate high resolution signals up to about 100kHz.  DMA based output is limited
to transitions every 17uS, so a 1kHz output will have about 6 bits of resolution and
a 100 Hz output will have about 9 bit resolution.
"""

class SerialWombatPWM(SerialWombatPin):
    def __init__(self,serial_wombat):
      self._sw = serial_wombat
    """!
    @brief Initialize a pin that has been declared as PWM. 
    @param pin The pin to become a PWM.  Valid values for SW4A: 0-3  SW4B: 1-3 
    @param dutyCycle A value from 0 to 65535 representing duty cycle
    @param invert if true, internally adjust duty cycle to 65535-duty cycle
    """
    def begin(self,pin, dutyCycle = 0, invert = False):
      self._pin = pin
      self._pinMode = 16#SerialWombat.SerialWombatPinMode_t.PIN_MODE_PWM
      tx= [ 0xC8,self._pin,self._pinMode,self._pin,(dutyCycle & 0xFF),(dutyCycle >> 8),invert,0x55 ]
      self._sw.sendPacket(tx)
    SW4AB_PWMFrequency_1_Hz = 0x76
    SW4AB_PWMFrequency_2_Hz = 0x66
    SW4AB_PWMFrequency_4_Hz = 0x56
    SW4AB_PWMFrequency_8_Hz = 0x46
    SW4AB_PWMFrequency_16_Hz = 0x75
    SW4AB_PWMFrequency_32_Hz = 0x65
    SW4AB_PWMFrequency_63_Hz = 0x55
    SW4AB_PWMFrequency_125_Hz = 0x45
    SW4AB_PWMFrequency_244_Hz = 0x71
    SW4AB_PWMFrequency_488_Hz = 0x61
    SW4AB_PWMFrequency_976_Hz = 0x51
    SW4AB_PWMFrequency_1952_Hz = 0x41
    SW4AB_PWMFrequency_3900_Hz = 0x31
    SW4AB_PWMFrequency_7800_Hz = 0x21
    SW4AB_PWMFrequency_15625_Hz = 0x11
    SW4AB_PWMFrequency_31250_Hz = 0x01

    """
    @brief Set PWM duty cycle
    @param dutyCycle A value from 0 to 65535 representing duty cycle
    """
    def writeDutyCycle(self,dutyCycle):
      tx= [ 0x82,self._pin,(dutyCycle & 0xFF),(dutyCycle >>8),255,0x55,0x55,0x55 ]
      self._sw.sendPacket(tx);



#! @brief Extends the SerialWombatPWM class with SW4A/SW4B specific functionality
class SerialWombatPWM_4AB (SerialWombatPWM):

    def __init__(self,serial_wombat):
        SerialWombatPWM.__init__(self,serial_wombat)

        self.SW4AB_PWMFrequency_1_Hz = 0x76
        self.SW4AB_PWMFrequency_2_Hz = 0x66
        self.SW4AB_PWMFrequency_4_Hz = 0x56
        self.SW4AB_PWMFrequency_8_Hz = 0x46
        self.SW4AB_PWMFrequency_16_Hz = 0x75
        self.SW4AB_PWMFrequency_32_Hz = 0x65
        self.SW4AB_PWMFrequency_63_Hz = 0x55
        self.SW4AB_PWMFrequency_125_Hz = 0x45
        self.SW4AB_PWMFrequency_244_Hz = 0x71
        self.SW4AB_PWMFrequency_488_Hz = 0x61
        self.SW4AB_PWMFrequency_976_Hz = 0x51
        self.SW4AB_PWMFrequency_1952_Hz = 0x41
        self.SW4AB_PWMFrequency_3900_Hz = 0x31
        self.SW4AB_PWMFrequency_7800_Hz = 0x21
        self.SW4AB_PWMFrequency_15625_Hz = 0x11
        self.SW4AB_PWMFrequency_31250_Hz = 0x01

    """
    @brief Set PWM Frequency (Adjusts all PWM outputs' frequency on a SerialWombat 4A/B chip)
    @param frequency  A value of the #Wombat4A_B_PWMFrequencyValues_t enumeration
    
    This function changes the Serial Wombat 4A and 4B PWM output frequncy by adjusting
    the clock divisor for the PWM generation hardware.  By default the value is 31250Hz.
    Changing the frequency may reduce PWM resolution from 10 bits to 8 bits for some
    frequencies.  However, the input value for duty cycle for methods of this class
    continue to be 0 to 65535 and are scaled accordingly.
    
    @warning This function will likely not be compatible with other models in the Serial Wombat
    family based on other hardware that are released in the future because it is tightly coupled to the
    PIC16F15214 hardware.
    """
    def setFrequency_SW4AB(self, frequency):
      tx= [ 220, # SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE_HW_0,
            self._pin,self._pinMode,frequency,0x55,0x55,0x55,0x55 ]
      self._sw.sendPacket(tx)

#! @brief Extends the SerialWombatPWM class with SW18AB specific functionality, including SerialWombatAbstractScaledOutput
class SerialWombatPWM_18AB(SerialWombatPWM, SerialWombatAbstractScaledOutput):
    def __init__(self,serial_wombat):
		SerialWombatPWM.__init__(self,serial_wombat)
		SerialWombatAbstractScaledOutput.__init__(self,serial_wombat)
		self._asosw = serial_wombat

    """!
    @brief Set the PWM frequency on a Serial Wombat 18AB chip's PWM

    @param frequency_Hz  Frequency in Hz.  Note that actual frequency may vary based on hardware capabilities of the pin.
    """
    def writeFrequency_Hz(self,frequency_Hz):
        tx= [ 220,self._pin,self._pinMode]+SW_LE32(1000000 / frequency_Hz)+[0x55 ]
        self._sw.sendPacket(tx)


    """!
    @brief Set the PWM period on a Serial Wombat 18AB chip's PWM

    @param period_uS  Period in microseconds.  Note that actual period may vary based on hardware capabilities of the pin.
    """
    def writePeriod_uS(self,period_uS):
        tx= bytearray([ 220,self._pin,self._pinMode])+SW_LE32(period_uS)+bytearray([0x55 ])
        self._sw.sendPacket(tx)

    """!
    @brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
    @return current pin number
    """
    def pin(self):
        return self._pin
    """!
    @brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
    @return current pin mode number
    """
    def swPinModeNumber(self):
        return self._pinMode

