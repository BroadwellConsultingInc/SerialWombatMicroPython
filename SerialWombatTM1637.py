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
#from enum import IntEnum


class SWTM1637Mode ():
	tm1637Decimal16 = 0  #!< Get the number to display from a pin or data source and display in decimal
	tm1637Hex16 = 1	#!< Get the number to display from a pin or data source and display in hex
	tm1637CharArray = 2 #!< Display a string sent by the host
	tm1637RawArray = 3 #!<Display raw LED segments sent by the host
	tm1637Animation = 4 #! < Display an animation loaded by the host and clocked out by the Serial Wombat chip

"""!
@brief A Class representing a TM1637 Seven-Segment Display connected to two Serial Wombat pins

This class is only supported on the Serial Wombat SW18AB chip.  It is not supported on the
Serial Wombat 4X line.

This class controls a State Machine driven driver for a TM1637 Seven Segment LED Display.

Each instance of this class uses an average of approximately 5% of the SW18's processing time.
This varies by configuration options and usage.

The Serial Wombat TM1637 driver can be configured in a number of ways:
* The Display shows the current value in Hex or decimal of a Pin's public data (including values written to the pin used to control the display)
* The Display shows an array of characters (as best they can be shown on a seven segment display) commanded by the host
* The Display shows raw 7-segment bitmaps commanded by the host
* The Display shows an animation downloaded to the Serial Wombat chip by the host.

See the available examples in the Arduino Library for usage.

\warning Different TM1637 displays behave differently based on how the manufacturer routed the LED matrix pins to the 
TM1637 outputs on the PCB.  This can cause digits to be displayed in the wrong order, or cause decimal points or 
clock colons to malfunction.  This is a display issue, not an issue with this library or the Serial Wombat firmware.
Display order issues can be corrected with the orderDigits() command.


A tutorial is available here:

https://youtu.be/AwW12n6o_T0

\htmlonly
<iframe width = "560" height = "315" src = "https://www.youtube.com/embed/AwW12n6o_T0" title = "YouTube video player"
frameborder = "0" allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope
picture - in - picture" allowfullscreen></iframe>
\endhtmlonly

"""
class SerialWombatTM1637(SerialWombatPin):
	"""!
	@brief Constructor for SerialWombatTM1637 class
	@param serialWombat SerialWombatChip on which the PWM will run
	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat
	"""!
	@brief Initialize an instance of the TM1637 class
	
	@return Returns a negative error code if initialization failed.
	@param clkPin The primary pin for this pin mode, the Serial Wombat pin connected to the clk pin of the TM1637
	@param dioPin The Serial Wombat pin connected to the DIO/data pin of the TM1637
	@param digits The number of digits in the display.  This is used to optimze displays shorter than 6 digits
	@param mode  The mode (decimal, hex, char array, raw or animation) of the display driver
	@param dataSourcePin if in decimal or hex mode, the pin from which the 16 bit data will be read.  Set this to the clkPin setting if you want to be able to write 16 bit (5 digit) numbers using the SerialWombat.writePublicData() function.  Numbers larger than 65535 must be written as strings using the Character Mode
	@param Brightness - a value from 0 (dimmest) to 7 (brightest) based on the TM1637 hardware.  This scale is not linear.
	"""
	def begin(self, clkPin,  dioPin,  digits, mode,  dataSourcePin,  brightness0to7):
		self._pin = clkPin
		tx_200= [ 200, # Pin Set command
			clkPin,
			11, # TM1637
			dioPin,
			digits,
			mode,
			dataSourcePin,
			brightness0to7]
		retval,rx = self._sw.sendPacket(tx_200)
		return retval

	"""
	@brief Used to reorder the digits of the display to match display hardware.
	
	TM1637 displays do not have a standardized wiring of LED module to the TM1637 driver pins.
	This can cause numbers to appear in the wrong order.
	This can be fixed by displaying the string "012345" on the display.  If it appears out of
	order, then issue this command with the parameters matching what is displayed on the screen.
	
	For instance, if a Six digit display showed 210543 when commanded to show "012345", calling
	\code
	orderDigits(2,1,0,5,4,3)
	\endcode
	after begin() would cause the driver to reorder the output to make the display appear in the desired order.
	
	@return Returns a negative error code if errors occur during configuration
	"""
	def writeDigitOrder(self, first,  second,  third,  fourth,  fifth,  sixth ):
		tx_201= [ 201, # Pin Set command
			self._pin,
			11, # TM1637
			first,
			second,
			third,
			fourth,
			fifth]
		retval,rx = self._sw.sendPacket(tx_201)
		if (retval < 0):
			return retval
		tx_202= [ 202, # Pin Set command
			self._pin,
			11, # TM1637
			sixth,
			0x55,
			0x55,
			0x55,
			0x55]
		result,rx = self._sw.sendPacket(tx_202)
		return result

	"""
	@brief Used to send data to the data array of the driver.  
	
	@param data  A 6 byte array that is sent to the display driver
	@return Returns a negative error code if errors occur during configuration 
	
	The meaning of this data varies based on mode.  See examples.
	"""
	def writeArray(self, data):
		for i in range(6):
			if (data[i] == None):
				data[i] = ord('0')
		tx_204= [ 204, # Pin Set command
			self._pin,
			11, # TM1637
			data[0],
			data[1],
			data[2],
			data[3],
			data[4]]
		retval,rx = self._sw.sendPacket(tx_204)
		if (retval < 0):
			return retval
		tx_205 = [ 205, # Pin Set command
			self._pin,
			11, # TM1637
			data[5],
			0x55,
			0x55,
			0x55,
			0x55]
		result,rx = self._sw.sendPacket(tx_205)
		return result
	

	"""
	@brief Set a bitmap of the MSB of each digit to control decimal points
	
	Note that TM1637 decimal point implementation varies greatly depending on the
	display manufacturer.  Setting bits may or may not cause decimal points to display,
	the clock colon to display, or other undefined behavior.  Unexpected behavior is likely
	the result of display pcb implementation, not an issue with this library or the Serial Wombat
	firmware.
	@param decimalBitmapLSBleftDigit A bitmap indicating if the decimal for each digit should be lit.  LSB is first digit  Valid values are 0 - 0x3F
	@return Returns a negative error code if errors occur during configuration
	
	"""
	def writeDecimalBitmap(self, decimalBitmapLSBleftDigit):
		tx_206 = [
			206, # Pin Set command
			self._pin,
			11, # TM1637
			decimalBitmapLSBleftDigit,
			0x55,
			0x55,
			0x55,
			0x55,
			]
		result,_rx = self._sw.sendPacket(tx_206)
		return result

	"""
	@brief Changes the brightness of the display
	
	@param Brightness - a value from 0 (dimmest) to 7 (brightest) based on the TM1637 hardware.  This scale is not linear.
	@return Returns a negative error code if errors occur during configuration
	"""
	def writeBrightness(self, brightness0to7):
		tx_203 = [ 203, # Pin Set command
			self._pin,
			11, # TM1637
			brightness0to7,
			0x55,
			0x55,
			0x55,
			0x55,
		]
		return self._sw.sendPacket(tx_203)

	"""
	@brief Loads an animation to the Serial Wombat user buffer area and initializes the animation
	
	The pin should have previously been initialized with the begin() command an animation mode prior to
	this call.
	
	@param bufferIndex The index into the User Buffer where the data for the animation should be stored
	@param delay How long the animation display driver should wait between loading new data
	@param Number of Frames to be displayed before returning to the first frame.  This should be the number of lines in data
	@param data A 2 dimensional array of width 6 and arbitrary length.
	@return Returns a negative error code if errors occur during configuration
	"""
	def writeAnimation(self,bufferIndex, delay,  numberOfFrames,  data):
		lineardata = bytearray()
		for x in data:
			lineardata += bytearray(x)
		result = self._sw.writeUserBuffer(bufferIndex, lineardata, numberOfFrames * 6)

		if (result < 0):
			return result
		settings =   SW_LE16(bufferIndex) +  SW_LE16(delay) + bytearray( [numberOfFrames, 0]) 
		return self.writeArray(settings)

	"""
	@brief Whether or not to suppress leading zeros in decimal mode
	
	@return Returns a negative error code if errors occur during configuration
	@param supress  true:  suppress leading zeros   false:  Do not suppress leading zeros
	"""
	def suppressLeadingZeros(self, suppress):
		tx_203 = [ 203, # Pin Set command
			self._pin,
			11, # TM1637
			0x55, # Don't change brightness
			1,  #supress
			0x55,
			0x55,
			0x55,
		]
		if (not suppress):
				tx_203[4] = 0
		return self._sw.sendPacket(tx_203)

	"""	
	@brief Set a bitmap of the digits that should blink at 2Hz with 7/8 duty cycle
	
	This function is useful for creating user interfaces where the user increments or decrements
	one digit of a number at a time. The blinking digit indicates the digit that will change.
	
	@param blinkBitmap A bitmap indicating if the decimal for each digit should be lit.  LSB is first digit  Valid values are 0 - 0x3F. 1 = blink
	@return Returns a negative error code if errors occur during configuration
	
	"""
	def writeBlinkBitmap(self, blinkBitmapLSBleftDigit):
		tx_207 = [ 207, # Pin Set command
			self._pin,
			11, # TM1637
			blinkBitmapLSBleftDigit,
			0x55,
			0x55,
			0x55,
			0x55,
			]
		result, _rx = self._sw.sendPacket(tx_207)
		return result

	"""
	@brief Write a byte to String mode, shifting other characters
	
	This function allows the TM1637 mode to use Arduino Print statements.
	
	@param data Byte to be written to display
	@return Number of bytes written
	
	"""
	def write(self, data):
		tx = [
			SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE8, # Pin Set command
			self._pin,
			SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637, # TM1637
			1,
			data,
			0x55,
			0x55,
			0x55,
                ]
		result, _rx = self._sw.sendPacket(tx)
		if ( result < 0):
			return 0
		else:
			return 1

	def writeBuffer(self,  buffer,  size):
		initialSize = size
		if (size > 6): # We can only display 6 characters.  Skip the first ones if more than 6
			buffer += size - 6
			size = 6
		if (size > 4):
			tx = [208,# SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE8, # Pin Set command
			self._pin,
			11, # TM1637SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637, # TM1637
			4,
			buffer[0],
			buffer[1],
			buffer[2],
			buffer[3],
			]
			self._sw.sendPacket(tx)
			size -= 4
			buffer += 4

		tx = [ 208,#SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE8, # Pin Set command
                self._pin,
                11, # TM1637SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637, # TM1637
                size,
                0x55,
                0x55,
                0x55,
                0x55,
                ]
		for i in range(size):
			tx[i+4] = buffer[i]
		self._sw.sendPacket(tx)
		return initialSize


