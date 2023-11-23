"""
Copyright 2020-2023 Broadwell Consulting Inc.

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
import SerialWombat
import SerialWombatAbstractProcessedInput
from SerialWombatPin import SerialWombatPin



"""! @file SerialWombatProcessedInputPin.h
"""

"""! @brief A Class which reads data from another pin's public data and runs it through SerialWombatAbstractInputProcessing .  No physical output.  Designed for testing. 

"""

class SerialWombatProcessedInputPin(SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput):
	"""
	@brief Class constructor for SerialWombatPulseTimer
	@param serialWombat The Serial Wombat chip on which the SerialWombatPulseTimer pinmode will be run
        """
	def __init__(self,serial_wombat):
		self._sw = serial_wombat
		SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput.__init__(self,serial_wombat)

	"""
	@brief Initialize by providing the pin or public data source to read data from.
	
	This initialization takes a Serial Wombat pin as a parameter, sets units to uS and disables pull-ups
	@param pin pin or public data source to read data from.
        """
	def begin(self, pin,  dataSourcePin):
		self._pin = pin
		self._pinMode = 14 #SerialWombat.SerialWombatPinMode_t.PIN_MODE_INPUT_PROCESSOR;
		self.abstractProcessedInputBegin(pin,self._pinMode)
		tx = [ 200, #SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
		self._pin,
		self._pinMode,
		dataSourcePin,
		0x55,
		0x55,
		0x55,
		0x55 ]
		result,rx = self._sw.sendPacket(tx)
		return (result)


