#pragma once
"""
Copyright 2024 Broadwell Consulting Inc.

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
"""! @file SerialWombatHBridge.h
"""
import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombatAbstractScaledOutput import SerialWombatAbstractScaledOutput
from SerialWombat import SW_LE16
class SerialWombatHBridgeDriverChip():
        RelayAndPWM = 0
        LG9110_HG7881 = 1
        DRV8833 = 2
        DRV8871 = 3
        L298N = 4
        MX1508 = 5
        BTS7960 = 6
        IBT4 = 7
        A4990 = 8
        TB67H420FTG = 9

"""!
@brief A class representing a Serial Wombat H Bridge Output

An instance of this class should be declared for each pair of pins
to be used as a Serial Wombat H Bridge.  

"""

class SerialWombatHBridge(SerialWombatPin):
    """!
    @brief Constructor for SerialWombatHBridge class
    @param serialWombat SerialWombat  chip on which the PWM will run
    """
    def __init__(self,serial_wombat):
                self._sw = serial_wombat

    """!
    @brief Initialize a pin that has been declared as HBridge. 
    @param pin The pin to become the first pin of the HBridge control.  
    @param secondPin The 2nd pin to become the first pin of the HBridge control.  
    @param PWMPeriod_uS A value  representing the period of the  PWM duty cycle in uS
    @param chip   The Driver chip being driven.  
    """
    def begin(self, pin, secondPin, PWMPeriod_uS, chip)
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode.PIN_MODE_HBRIDGE
        tx = [ 0xC8,self._pin,self._pinMode,secondPin,chip,0x55,0x55,0x55 ]
        self._sw.sendPacket(tx)
        tx2 = bytearray([ 220,self._pin,self._pinMode]) + SW_LE16(PWMPeriod_uS) + bytearray([0x55,0x55,0x55])
        self._sw.sendPacket(tx2)


"""!
@brief Extends the SerialWombatHBridge class with SW18AB specific functionality, including SerialWombatAbstractScaledOutput
"""
class SerialWombatHBridge_18AB( SerialWombatHBridge, SerialWombatAbstractScaledOutput):
    def __init__(self,serial_wombat):
        SerialWombatHBridge.__init__(self,serial_wombat)
        SerialWombatAbstractScaledOutput.__init__(self,serial_wombat)
        self._asosw = serial_wombat

