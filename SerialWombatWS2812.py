#pragma once
"""
Copyright 2021 Broadwell Consulting Inc.

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

#from enum import IntEnum
import SerialWombatPin
from SerialWombat import SW_LE16
from SerialWombat import SW_LE32


class SWWS2812Mode():
	ws2812ModeBuffered = 0  #!< Standard buffered mode.  Colors are uploaded by the host
	ws2812ModeAnimation = 1	#!< Multiple arrays with delays are uploaded by the host and displayed over time by the Serial Wombat chip
	ws2812ModeChase = 2 #!< A single lit LED cycles through all of the LEDs.


"""!
@brief A Class representing a WS2812 or compatible RGB LED string connected to a Serial Wombat pin

This class is only supported on the Serial Wombat SW18AB chip.  It is not supported on the
Serial Wombat 4X line.  This pin mode can only be used on enhanced capability pins (WP0-4, WP7, or WP9-19)

This class controls a State Machine driven driver for a WS2812 compatible RGB LED string.

Each instance of this class uses an average of approximately TBD% of the SW18's processing time.
This varies by configuration options and usage.

The Serial Wombat WS2812 driver can be configured in a number of ways:
* The driver lights up the LEDs one at a time in sequence
* The driver shows colors as commanded by the host
* The driver cycles through arrays of colors at a specified rate


See the available examples in the Arduino Library for usage.

@warning Different WS2812 pcbs behave differently based on how the manufacturer routed the LEDs on the PCB Board.
For instance a square 4x4 matrix may not light in the order expected.  This is not an issue with the library.

@warning An array of WS2812 LEDs can pull lots of current.  Lighting multiple LEDs at full brightness may consume
more power than your supply can provide, causing the system voltage to become unstable.  An unstable system voltage
can cause unreliable operation of the Serial Wombat chip.

The Serial Wombat WS2812 driver is extremely efficient in terms of processor time since it uses
the PIC24FJ256GA702's DMA and SPI hardware to generate the WS2812 signal.  This allows the Serial
Wombat firmware to easily clock out WS2812 signals while doing other thigns.  However, this method
is very RAM intensive, requiring about 50 bytes of ram for each LED.  

The RAM used for buffering this signal is stored in the User Buffer RAM, an array available for the
user to allocate to various PIN modes' uses.  In Version 2.0.3 of the Serial Wombat 18AB firmware
there is 8k of RAM allocated to User Buffer, allowing about 160 LEDs to be used if all RAM is
allocated to the WS2812.  

A number of frames to be shown in rotation with configurable delays inbetween can also be stored
in the User Buffer.  This is in additional to the rendering buffer.  Each animation frame requires
2+3*NumberOfLEDs bytes.

The Update rate is variable with the number of LEDs so that rendering of colors into the User Buffer
is spread across multiple Serial Wombat 1mS execution frames.  The LEDs will be updated approximately every
X mS, where X is the number of LEDs plus 20.

A tutorial is available here:

https://youtu.be/WoXvLBJFpXk

@htmlonly
<iframe width = "560" height = "315" src = "https://youtu.be/WoXvLBJFpXk" title = "YouTube video player"
frameborder = "0" allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; 
picture - in - picture" allowfullscreen></iframe>
@endhtmlonly
"""

class SerialWombatWS2812(SerialWombatPin.SerialWombatPin):
	"""!
	@brief Constructor for SerialWombatWS2812 class
	@param serialWombat SerialWombat chip on which the driver will run
	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat
		self._numLEDS = 0
		self._userBufferIndex=0


	"""!
	@brief Initialize a WS2812 LED driver object

	This function initializes hardware and data arrays for the WS2812 driver.
	It requires about 30uS per LED to initialize the data array.  During this
	time pin processing is suspended.  This can cause glitches in other pins.
	It is recommended that this pin mode be initialized once near the beginning of
	at power up and 
	that begin() not be called during real-time operation.
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	@param pin  The pin connected to the WS2812.  This must be an enhanced capability pin ( WP0-4, WP7, or WP9-19)
	@param numberOfLEDs The number of LEDs connected in series to the pin
	@param userBufferIndex The index in bytes into the User Buffer area where the signal train to be sent to the LEDs is stored.  
	The amount of data bytes required for the configured number of LEDs can be queried with readBufferSize.  This area must not
	be used by other pins, and cannot extend past the end of the 8k of space.
	"""
	def begin(self,  pin,  numberOfLEDs,  userBufferIndex):
		self._pin = pin
		self._numLEDS = numberOfLEDs
		self._userBufferIndex = userBufferIndex

		tx = bytearray([ 200,self._pin,12 ]) + SW_LE16(userBufferIndex) + bytearray([self._numLEDS,0x55,0x55 ])
		result,rx = self._sw.sendPacket(tx)
		return (result);

	"""!
	@brief Set an LED color
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	@param led The index of the LED to be set to color
	@param color The color of the LED in 0x00RRGGBB format
	"""
	def write(self,  led,  color):
		tx = bytearray([ 201,self._pin,12,led]) + SW_LE32(color) + bytearray([0x55])
		result,rx = self._sw.sendPacket(tx)
		return result

	"""
	@brief Set a number of LEDs to colors based on an array of uint32_t colors
	
	@param led  The index of the first led to set
	@param length The number of LEDs to set, and the number of entires in colors array
	@param  colors An array of uint32_t integer colors in the format 0x00RRGGBB format
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writearray(self,  led,  length, colors):
		for i in range(length):
			result = self.write(led + i, colors[i])

			if (result < 0):
				return (result)

		return(0)

	"""
	@brief set the color of one LED in an animation frame
	
	@param frame The Frame index of the color being set
	@param led The LED index in that frame of the color being set
	@param color The color of the LED in 0x00RRGGBB format
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writeAnimationLED(self,  frame,  led,  color):
		tx = [ 203,self._pin,12,frame,led,(int(color) >>16 ) & 0xFF,(color >> 8) & 0xFF,color & 0xFF]
		result,rx = self._sw.sendPacket(tx)
		return result

	"""!
	@brief Store an array of colors for an entire animation frame
	
	@param frame The index of the frame being stored
	@param colors an array of uint32_t colors in 0x00RRGGBB format to be stored in the frame.  The length of the array must match the number of LEDs
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writeAnimationFrame(self,  frame, colors):
		for i in range( self._numLEDS):
			result =  self.writeAnimationLED(frame, i, colors[i])
			if (result < 0):
				return (result)
		return(0)
		

	"""!
	@brief Set how long an animation frame should be displayed before moving to the next frame
	@param frame The index of the frame being set
	@param dealy_mS the amount of time to display the frame in mS
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writeAnimationFrameDelay(self,  frame,  delay_mS):
		tx = bytearray([ 205,self._pin,12,frame]) + SW_LE16(delay_mS) + bytearray([0x55,0x55])
		result, rx = self._sw.sendPacket(tx)
		return (result)

	"""!
	@brief set the location in UserBuffer where the animation array will be stored and number of frames
	
	@param index The index into UserBuffer
	@param numberOfFrames The number of frames that make up the animation
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writeAnimationUserBufferIndex(self,  index,  numberOfFrames):
		tx = bytearray([ 204,self._pin,12]) + SW_LE16(index) + bytearray([numberOfFrames,0x55,0x55 ])
		result, rx = self._sw.sendPacket(tx)
		return (result)

	"""!
	@brief returns the number of bytes of UserBuffer required to service the configured number of LEDs
	
	This number does not include any animation frames.
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def readBufferSize(self ):
		tx = [ 202,self._pin,12,self._numLEDS,0x55,0x55,0x55,0x55 ]
		result, rx =  self._sw.sendPacket(tx)
		if (result >= 0):
			return (rx[3] + rx[4] * 256)
		else:
			return (result);


	"""!
	@brief Sets the mode of the WS2812 LED Driver
	@return 0 or higher for success or a negative number indicating an error code from the Serial Wombat chip.
	"""
	def writeMode(self,  mode):
		tx = [ 206,self._pin,12,mode,0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx)
		return (result)

	"""!
	@brief Display a bargraph using the configured ws2812 class
	
	@param sourcePin  The data source to use for the bargraph
	@param offRGB The color to use for LEDs beyond the bargraph level
	@param onRGB The color to use for LEDs lit by the bargraph
	@param min The public data value (or below) to be treated as the beginning of the bargraph
	@param max The public data value (or above) to be treated as the end of the bargraph
	"""
	def barGraph(self,  sourcePin,  offRGB,  onRGB,  min,  max):
		tx = [ 206,self._pin,12,3,sourcePin,0x55,0x55,0x55 ]
		result,rx =  self._sw.sendPacket(tx);  
		if (result < 0) :
			return result
		result =  self.write(0, offRGB); 
		if (result < 0) :
			return result
		result =  self.write(1, onRGB)  
		if (result < 0):
			return result

		minMax = bytearray([ 207,self._pin,12])+SW_LE16(min)+ SW_LE16(max)+ bytearray([0x55 ])
		result, rx = self._sw.sendPacket(minMax)
		return (result)
		

	 