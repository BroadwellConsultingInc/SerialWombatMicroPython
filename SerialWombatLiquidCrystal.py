"""
Copyright 2022-2023 Broadwell Consulting Inc.

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



"""! @file SerialWombatLiquidCrystal.h
"""

"""! @brief A Class which connects to HD44780 / 1602 / 4002 / 2004   or similar interface Character LCDs


  This pin mode has nearly identical interfaces to the classic Arduino LiquidCrystal library and can be used
  with similar parallel character LCDs.  This pin mode is only intended for use with character LCDs that are connected in
  4 bit parallel (E, RS, D4, D5, D6, D7) with the Serial Wombat  chip.  RW pin on the LCD must be grounded.

  In addition to the classic LiquidCrystal interfaces, this pin mode has a more advanced mode avaialble through the
 initializeBufferCopy() interface which allows displays to be updated from data stored in the Serial Wombat Chip's
User Buffer.  The Serial Wombat chip will handle getting the right data to the right location on the display.  This
is convenient for displays such as 20x4 displays which alternate lines when addressing.  When combined with a shifting
queue initialized with SerialWombatQueueType::QUEUE_TYPE_RAM_BYTE_SHIFT, the display can be treated like any other
Stream Class under Arduino.  See the Arduino examples directory for an example of this.

This class also supports buffer copying to large 40x4 character LCDs that have two E lines.  These displays are essentially two 44780 controllers
connected to a single piece of glass.  See the example in the Arduino examples directory.

E and E2 lines must be exclusive to a single LCD display.  If multiple LCDs are attached to a single Serial Wombat Chip then RS, D4, D5, D6, and D7
can be shared by both displays.

When in buffer mode the class updates one character per mS.  

A video Tutorial on this pin mode is available:

\htmlonly
#TODO
\endhtmlonly

#TODO https://youtu.be/


"""
import SerialWombat
from ArduinoFunctions import delay
from SerialWombatPin import SerialWombatPin

class SerialWombatLiquidCrystal(SerialWombatPin):
	"""!
	@brief Class constructor for SerialWombatLiquidCrystal
	@param serialWombat The Serial Wombat chip on which the SerialWombatLiquidCrystal pin mode will run
	@param rs  The Serial Wombat Pin connected to the LCD rs pin.
	@param enable The Serial Wombat pin connected to the LCD e pin.
	@param d4 The Serial Wombat pin connected to the LCD d4 pin.
	@param d5 The Serial Wombat pin connected to the LCD d5 pin.
	@param d6 The Serial Wombat pin connected to the LCD d6 pin.
	@param d7 The Serial Wombat pin connected to the LCD d7 pin.
	"""
	def __init__(self,serial_wombat , rs, enable, d4, d5, d6, d7):
		self._sw = serial_wombat
		self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_LIQUIDCRYSTAL
		self._pin = enable
		self._rs = rs
		self._d4 = d4
		self._d5 = d5
		self._d6 = d6
		self._d7 = d7
		self._rows = 2
		self._columns = 40
		self._offsets = [ 0,64,20,84,0,64,20,84 ]


	"""!	
	@brief Initialization routine for SerialWombatLiquidCrystal
	
	@param cols  The width of the LCD in characters
	@param  rows The height of the LCD in character rows
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def begin(self,cols = 80, rows = 1):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
						self._pin,
						self._pinMode,
						self._rs,
						self._d4,
						self._d5,
						self._d6,
						self._d7 ]
		result, rx = self._sw.sendPacket(tx)
		if (result < 0):
			return (result)
		self._rows = rows
		self._columns = cols
		result = self.setRowOffsets(0, 0x40, cols, 0x40 + cols)
		if (result < 0):
			return (result)

		return(0)

	"""!
	@brief Clear the LCD display
	
	By default this function delays 2 to 3 mS after issuing the command to be compatible with LiquidCrystal::clear
	This library adds an optional parameter that eliminates this delay.
	
	@param delay Whether or not to block for 2mS after issuing the command
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def clear(self,delayAfterClear = True):
		result = self.command(0x01);  # Clear display
		if (delayAfterClear):
			delay(2)
		return result


	"""!
	@brief Set the LCD cursor / entry position to the 0,0 position
	
	By default this function delays 2 to 3 mS after issuing the command to be compatible with LiquidCrystal::home
	This library adds an optional parameter that eliminates this delay.

	@param delay Whether or not to block for 2mS after issuing the command

	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def home(self,delayAfterHome = True):
		result =  self.command(0x02);  # Home
		if (delayAfterHome):
			delay(2)
		return result

	"""!
	@brief Set the cursor / next entry position 
	
	@param col Column to set
	@param row Row to set

	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def setCursor(self,col, row):
		if (row >= self._rows):
			return -1

		if (col >= self._columns):
			return -1
		return self.command(0x80 + self._offsets[row] + col)

	"""!
	@brief Makes the cursor invisible
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def noCursor(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
						0, # DisplayControl
						~0x02, # And Mask
						0, # OR MASK
						0x55,0x55]
		
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Makes the cursor visible
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def cursor(self):
	
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
								0, # DisplayControl
						0xFF, # And Mask
						0x02, # OR MASK
						0x55,0x55]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Makes the cursor blink
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def blink(self):
		tx= [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
								0, # DisplayControl

						0xFF, # And Mask
						0x01, # OR MASK
						0x55,0x55]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Makes the cursor not blink
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def noBlink(self):
		tx = [SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
								0, # DisplayControl

						~0x01, # And Mask
						0, # OR MASK
						0x55,0x55]
		result,rx =  self._sw.sendPacket(tx)
		return result


	"""!
	@brief Enables LCD display
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def display(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
							self._pin,
							self._pinMode,
								0, # DisplayControl

							0xFF, # And Mask
							0x04, # OR MASK
							0x55,0x55]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Disables LCD display
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def noDisplay(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
								0, # DisplayControl

						~0x04, # And Mask
						0, # OR MASK
						0x55,0x55 ]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Display moves left when scrolling
	
	 Note that this command has no effect in initializeBufferCopy() mode.

	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def scrollDisplayLeft(self):
		return self.command(0x18); # Display Move left LCD
		
	"""!
	@brief Display moves right when scrolling
	
	 Note that this command has no effect in initializeBufferCopy() mode.

	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def scrollDisplayRight(self):
		return self.command(0x1C); # Display Move right LCD

	"""!
	@brief Turn on autoscrolling mode on the LCD display (not in the Serial Wombat chip)
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def autoscroll(self):

		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
						self._pin,
						self._pinMode,
								1, # DisplayMode
						0xFF, # And Mask
						0x01, # OR MASK
						0x55,0x55]
		
		result,rx =  self._sw.sendPacket(tx)
		return result
	


	"""!
	@brief Turn off autoscrolling mode on the LCD display (not in the Serial Wombat chip)
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def noAutoscroll(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
					self._pin,
					self._pinMode,
							1, # DisplayMode
					~0x01, # And Mask
					0x00, # OR MASK
					0x55,0x55]
		result,rx =  self._sw.sendPacket(tx)
		return result


	"""!
	@brief LCD Display entry occurs left to right
	
	 Note that this command has no effect in initializeBufferCopy() mode.
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def leftToRight(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
					self._pin,
					self._pinMode,
							1, # DisplayMode
					0xFF, # And Mask
					0x02, # OR MASK
					0x55,0x55 ]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief LCD Display entry occurs right to left
	
	 Note that this command has no effect in initializeBufferCopy() mode.
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def rightToLeft(self):
		tx  = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
					self._pin,
					self._pinMode,
							1, # DisplayMode
					~0x02, # And Mask
					0x00, # OR MASK
					0x55,0x55 ]
		result,rx =  self._sw.sendPacket(tx)
		return result

	"""!
	@brief Write a byte of data directly to the LCD
	
	 Use this command if using the LCD like a classic LiquidCrystal display.  Do not use this 
	command if in initializeBufferCopy() mode.
	
	@param data A byte of data to write to the display
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def write(self,data):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE4,
			self._pin,
			self._pinMode,
		2, # Data
		data,
		0x55,
		0x55,
		0x55 ]
		result,rx = self._sw.sendPacket(tx)
		if (result >= 0):
			return 1;


	"""!
	@brief Write an array of data directly to the LCD
	
	 Use this command if using the LCD like a classic LiquidCrystal display.  Do not use this 
	command if in initializeBufferCopy() mode.
	
	@param buffer address of a buffer to be written to the display
	@param count number of bytes to write to the display
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	#TODO size_t write(uint8_t* buffer, size_t count)

	"""!
	@brief Write bitmap data to the display for custom characters
	
	@param index The character to be written.  Valid values are typically 0-7
	@param bitmap An array of 7 bytes which represent the character.  bitmap[0] is the top, Least significant bit is the rightmost pixel.  1 is black pixel
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def createChar(self,index, bitmap):
		if (index >= 8):
			return (-1)
		result = self.command((0x40 | (index << 3))); # Set character ram location
		if (result < 0):
			return result
		for i in range(8):
			result = self.write(bitmap[i])
			if (result < 0):
				return result
		return 0

	"""!
	@brief Set the offsets in the LCD on-board memory for the beginning of each row
	
	These values are used for the setCursor() and initializeBufferCopy() functions and
	should be set before these functions are called.  
	An Arduino example is avaiable which displays addresses on the LCD which correspond to
	the parameters to this function to help the user determine proper values.
	
	@param row1 The offset of the top first row
	@param row2 The offset of the second row
	@param row3 The offset of the third row
	@param row4 The offset of the fourth row
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def setRowOffsets(self,row1, row2, row3, row4):
		self._offsets[0] = row1
		self._offsets[1] = row2
		self._offsets[2] = row3
		self._offsets[3] = row4
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE8,
					self._pin,
					self._pinMode,
						0,row1,0x55,0x55,0x55]
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return result
		tx[3] = 1
		tx[4] = row2
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return result
		tx[3] = 2 
		tx[4] = row3
		result,rx = self._sw.sendPacket(tx)
		if (result < 0): 
			return result
		tx[3] = 3
		tx[4] = row4
		result,rx = self._sw.sendPacket(tx)
		if (result < 0):
			return result
		return(0)

	"""!
	@brief send a command directly to the LCD
	
	@param cmd Byte to be sent to the LCD while the RS line is set to command
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def command(self,cmd):
		tx= [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE4,
		self._pin,
		SerialWombat.SerialWombatPinMode_t.PIN_MODE_LIQUIDCRYSTAL,
			1, # Command
			cmd, 
			0x55,
			0x55,
			0x55]
		return self._sw.sendPacket(tx)

	"""!
	@brief returns the e pin number.  Override for use with classes that require this as a virtual function
	
	@return Pin number of the e pin
	"""
	def pin(self):
		return self._pin

	"""!
	@brief returns the pin mode number.  Override for use with classes that require this as a virtual function
	
	@return Pin mode of the current pin
	"""
	def swPinModeNumber(self):
		return self._pinMode

	"""!
	@brief kicks off the Serial Wombat chip state machine that copies one character to the LCD each second from a buffer
	
	 This function extends the LiquidCrystal functionality by adding a state machine that runs on the Serial Wombat chip
	This state machine copies a byte every ms from an index into the User Buffer area to the LCD.  It uses the offsets
	set using setRowOffsets() and the width parameter to automatically format the data from the User Buffer into lines in
	the proper order.  When used with the SerialWombatQueueType::QUEUE_TYPE_RAM_BYTE_SHIFT type queue to create a FIFO 
	style display.  
	@param bufferIndex Index into the User Buffer where data copy starts.  When using a shifted Queue, this is the queue address + 8.
	@param width The width data to copy on each line.  Defaults to the number of columns specified in begin() if not provided.
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def initializeBufferCopy(self,bufferIndex, width = 255):
	
		if (width == 255):
			width = self._columns
		tx  = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
			self._pin,
			SerialWombat.SerialWombatPinMode_t.PIN_MODE_LIQUIDCRYSTAL,
			bufferIndex & 0xFF,
			bufferIndex >>8,
			width,
			0x55,
			0x55]
		return self._sw.sendPacket(tx)
#TODO	int16_t dataMonitor(pin, col, row, index, bool hex=false)

	"""!
	@brief Add a second e pin for use wtih 40x4 LCD displays
	
	This commands causes the Serial Wombat chip to do a second initialization of a display.  This is commonly required
	for 40x4 LCDs which are essenctially two LCD drivers attached to the same glass, one driver per two 40 character lines.
	
	This is only used when using the initializeBufferCopy() mode of this pin mode.  When this value is not set 80 bytes
	are copied to the display attached to the e pin.  When this value is set, 80 bytes are copied to the display attached
	to the e pin, followed by an additional 80 bytes attached to the e2 pin. 
	
	@return returns a number 0 or greater for success, negative numbers indicate an error occured.
	"""
	def beginE2(self,e2Pin):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE7,
		self._pin,
		SerialWombat.SerialWombatPinMode_t.PIN_MODE_LIQUIDCRYSTAL,
			e2Pin,
			0x55,
			0x55,
			0x55,
			0x55,
		]
		return self._sw.sendPacket(tx)

	#using Print::write;  #Inherit the write commands from print.


