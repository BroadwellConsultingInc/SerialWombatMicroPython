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



"""! @file SerialWombatHSClock.h
"""

"""! @brief A Class which outputs a high speed clock signal suitable for clocking other devices 


  This pin mode provides a high speed clock (in the case of the SW18AB Chip up to 32 MHZ).  The number of pins that support this mode and the resolution and frequency options will vary by base microcontroller. 

  In the case of the SW18AB chip only one pin may be configured to this pin mode, as the mode uses the hardware Reference Clock Output, and there is only one reference clock available on the PIC24FJ256GA702.  The selected pin must be an enhanced digital capability pin.

  The pin mode takes a 32 bit unsigned integer and outputs that frequency (or the chip's best approximation of it).  
  
In the case of the SW18AB chip, the output frequency is determined by a hardware clock divider that either outputs 32MHZ or 32Mhz / 2 * an integer.  So 32MHz and 16MHz are possible, but 24MHz (for example) is not.  The divisor can range from 1 *2 to 32767 * 2, so the minimum output frequency is 32000000 / 32767 / 2 = 488 Hz

@warning The SW18AB uses an internal oscillator which has an accuracy of +/- 2 percent.  So the accuracy of the output frequency can vary with the accuarcy of the internal oscillator.

If assigning a new pin mode to a pin in HS Clock mode, call the disable method first. 

A video Tutorial on this pin mode is available:

@htmlonly
//TODO  - Video coming soon
@endhtmlonly

//TODO https://youtu.be/


"""
import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE32

class SerialWombatHSClock(SerialWombatPin ):

	"""!
	@brief Class constructor for SerialWombatHSClock pin mode 
	@param serialWombat The Serial Wombat chip on which the SerialWombatLiquidCrystal pin mode will run SerialWombatHSClock(SerialWombatChip& serialWombat); 
	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat

	"""!
	/// @brief Begin outputing a clock at a frequency on a specified pin
	/// @param  pin The pin used to output the High Speed Clock.  On the Serial Wombat 18AB chip this must be an enhanced digital capability pin.
	/// @param frequency_Hz The frequency in Hz of the output.  The hardware may not be able to exactly produce the commanded frequency
	/// @return The frequency that is output based on the chip's hardware capabilities, or a negative number if an error occured.
	"""
	def begin(self,pin, frequency_Hz):

		self._pin = pin;
		self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_HS_CLOCK

		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
		self._pin,
		self._pinMode]) + SW_LE32(frequency_Hz) + bytearray([0x55])
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return (result)

		returnval = ((rx[5]) << 16) + ((rx[4]) << 8) + rx[3];
		return (returnval)

	"""!
	@brief Disables the high speed clock output
	"""
	def disable (self):
		tx = [
		SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE_DISABLE,
		self._pin,
		self._pinMode,
		0x55,0x55,0x55,0x55,0x55]
		result,rx = self._sw.sendPacket(tx)
		return result
