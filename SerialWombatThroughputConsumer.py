"""
Copyright 2021-2023 Broadwell Consulting Inc.

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
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE16

"""!
@brief A Class that consumes CPU time on the Serial Wombat chip in order to facilitate testing 

This class is only supported on the Serial Wombat SW18AB chip.  It is not supported on the
Serial Wombat 4X line.

This class provides a means to consume throughput inside of a pin in order to test different CPU loading secenarios.  

This class provides an array of 16 delays measured in uS.  When each
frame runs the cumulative frame counter is taken mod 16 to determine
which delay to use.  During this delay the pin goes high and waits in a 
loop for approximately the specified number of uS. 

"""
class SerialWombatThroughputConsumer(SerialWombatPin):

	"""!
	@brief Constructor for SerialWombatThroughputConsumer class
   @param serialWombat SerialWombatChip on which the ThroughputConsumer will run
   	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat
	"""
	@brief Initialize an instance of the Throughput Conumer class.  All delays are set to 0.
	@return Returns a negative error code if initialization failed.
	"""
	def begin(self, pin):
		self._pin = pin
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,pin,
					pin, SerialWombat.SerialWombatPinMode_t.PIN_MODE_THROUGHPUT_CONSUMER,
						0x55,0x55,0x55,0x55,0x55 ]
		result,rx = self._sw.sendPacket(tx)
		return result


	"""!
	/// @brief Set all delay times to a specified number of uS
	///
	/// @param delay  The number of uS to delay in each frame
	/// @return Returns a negative error code if errors occur during configuration 
	"""
	def writeAll(self, delay):
		for i in range(16):
			tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE1,
							self._pin,
							SerialWombat.SerialWombatPinMode_t.PIN_MODE_THROUGHPUT_CONSUMER,
							i]) + SW_LE16(delay) + bytearray([ 0x55,0x55])
			result,rx = self._sw.sendPacket(tx);
			if (result < 0):
				return (result)
			return 0

	"""!
	@brief Set a frame delay time to a specified number of uS
	
	@param frame The frame number (0-15) to set
	@param delay  The number of uS to delay in each frame
	@return Returns a negative error code if errors occur during configuration 
	
	"""
	def write(self, frame,  delay):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE1,
			self._pin,
                         SerialWombat.SerialWombatPinMode_t.PIN_MODE_THROUGHPUT_CONSUMER,
							frame])+ SW_LE16(delay) + bytearray([0x55,0x55])
		result,rx = self._sw.sendPacket(tx)
		return result



	"""!
	@brief Delay a specified number of uS within the packet processing routine

	@param delay  The number of uS to delay in each frame
	@return Returns a negative error code if errors occur during configuration 
	
	"""
	def delayInCommProcessing(self, delay):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE2,
							self._pin,
                            4]) + SW_LE16(delay) + bytearray([ 0x55,0x55, 0x55])
		result,rx = self._sw.sendPacket(tx)
		return result


