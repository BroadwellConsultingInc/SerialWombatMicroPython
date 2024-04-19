"""
Copyright 2023 Broadwell Consulting Inc.

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



"""! @file serialWombatHSCounter.h
"""


"""! @brief

This class is used to measure the frequency or cycles of a high speed input.  On the Serial Wombat 18AB
chip this class can be used two times, as two clock inputs are avaialble.  An enhanced digital capability
pin must be used.

This pin mode has been tested on inputs up to 4MHz on the 18AB.

For frequency measurements a number of counts is divided by a time.  The time in mS can be specified.
The frequency is updated every X ms.  In order to get a good value, X should be an even divisor of 1000.

The counter can be retreived and optionally be reset on reading.

The public data buffer for this pin mode can be based either on the count of cycles or the frequency.

Since the public data buffer is limited to 16 bits a divisor is available that's applied to the
counter or frequency before it's copied to the public data buffer.  That way a varying high speed
frequency can still create a varying public data buffer rather than saturating at 65535.

A video Tutorial on this pin mode may be available in the future:

@htmlonly
TODO - Video coming Soon
@endhtmlonly
//TODO - Video coming soon
"""

import SerialWombat
from SerialWombatPin import SerialWombatPin
import SerialWombatAbstractProcessedInput
#from enum import IntEnum
from SerialWombat import SW_LE16


class SWHSCounterPublicDataOutput():
		PULSE_COUNT = 2 #< The number of pulses that have occured since initialization. 
		FREQUENCY_ON_LTH_TRANSITION = 5 #< The frequency of the pulse in Hz


class SerialWombatHSCounter ( SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput):

	"""!
	@brief Class constructor for SerialWombatHSCounter
	@param serialWombat The Serial Wombat chip on which the SerialWombatHSCounter pinmode will be run
	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat
		self.PULSE_COUNT = 2 #< The number of pulses that have occured since initialization. 
		self.FREQUENCY_ON_LTH_TRANSITION = 5 #< The frequency of the pulse in Hz
		SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput.__init__(self,serial_wombat)

	"""!	
	@brief Initialization routine for SerialWombatHSCounter
	
	@param pin 
	@param 
	@param 
	"""
	def begin(self, pin, publicDataOutput = 5,#FREQUENCY_ON_LTH_TRANSITION
              framesBetweenUpdates = 100, publicOutputDivisor = 1):
		self._pin = pin
		self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_HS_COUNTER
		self.abstractProcessedInputBegin(pin,self._pinMode)

		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
		self._pin,
		self._pinMode]) + SW_LE16(framesBetweenUpdates) + SW_LE16(publicOutputDivisor) + bytearray([publicDataOutput])
		result, rx = self._sw.sendPacket(tx)
		return result


	def readCounts(self,resetCounts = False):
		resetCountsInt = 0
		if resetCounts:
			resetCountsInt = 1

		tx= [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE1,
		self._pin,
		self._pinMode,
		resetCountsInt,
		0x55,
		0x55,
		0x55,
		0x55]
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return 0

		returnval = ((rx[6]) << 24) + ((rx[5]) << 16) + ((rx[4]) << 8) + rx[3];
		return(returnval)

	def readFrequency(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE2,
		self._pin,
		self._pinMode,
		0x55,
		0x55,
		0x55,
		0x55,
		0x55 ]
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return 0

		returnval = ((rx[6]) << 24) + ((rx[5]) << 16) + ((rx[4]) << 8) + rx[3]
		return(returnval)

	"""!
	@brief Disables the high speed clock output
	"""
	def disable (self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE_DISABLE,
		self._pin,
		self._pinMode,
		0x55,0x55,0x55,0x55,0x55
		]
		result, rx = self.self._sw.sendPacket(tx)
		return result


