"""
Copyright 2021 Broadwell Consulting Inc.

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


"""! @file SerialWombatAbstractProcessedInput.h
"""

import SerialWombat
import SerialWombatPin
from SerialWombat import SW_LE16
from SerialWombat import SW_LE32
#from enum import IntEnum

"""! @brief SerialWombatAnalogInput, SerialWombatPulseTimer, SerialWombatResistanceInput and others inherit from this class

This class allows a common set of services to be applied to Serial Wombat inputs which inherit from it.  These include
SerialWombatAnalogInput, SerialWombatPulseTimer,  SerialWombatResistanceInput and will include others in the future.

This class is only applicable to the Serial Wombat 18AB firmware.

This class allows various transformations and filters to be performed on incoming measurements within the Serial Wombat
firmware using the Serial Wombat chip's cpu cycles.   Since this class is processed every 1mS for each self._pin configured to
an input class, it can do tasks like filtering or averaging much more quickly and consistently than could be achieved by
sampling the value over I2C or UART and doing the computation on the host device.  Minimum and Maximum measured values 
are also tracked for retreival by the host

Additionally, this class is capable of limiting input (for example any value below 10000 is processed as 10000, and any
value above 62331 is processed as 62331), scaling input (e.g. an expected input range of 3000 to 7000 is scaled linearly to the full 
Serial Wombat Range of 0 to 65535), mx+b linear transformations,  exclusion of outlier data (e.g. any value over 50000 is ignored, and
the previous valid measurement is substituted in its place). 

Inputs can be inverted (scaled from 0-65535 to 65535-0 by substracting the raw value from 65535).  This is useful for reversing the
direction of things like analog measured potentiometers.

The final output of the SerialWombatAbstractProcessedInput operations can be queued in a User Memory Area queue on a periodic basis.
This allows synchronsous sampling and storage of input data for retreival and processing by the host.  This allows waveforms to be
stored and processed.  Sampling period is an enumerated type ranging from 1mS to 1024mS in power of 2 intervals

Data processing happens in the following order each 1mS for any enabled feature:

- The pin mode measures the physical input
- Any outlier values are excluded.  if a value is excluded the last valid measured raw input is substituted in its place
- Inversion of input (subtraction of value from 65535)
- Transformation of output value (Scale of smaller input range (e.g. 8000-12000 to 0-65535) or mx+b linear transformation
- Averaging and filtering of the result of prior steps and storage of averaged / filtered values for access by the host.  
- Selection of the result to be passed to the next steps.  The unfiltered value, the averaged value, or the filtered value
can be selected to be the pin's public data output
- Updating the minimum and maximum recorded value for retreival by the host
- Sampling the data into a queue in the user buffer
- Placement of the value into the pin's 16-bit public data buffer for access by the host or other pin modes that react to a pin's public data buffer.


To use this class first configure the pin to its mode using the normal begin() call for that pin mode (the derived class).
Then call any configuratioon commands ( writeInverted, writeTransformLinearMXB, etc)
then call writeProcessedInputEnable(True) to enable processing.


"""


class SerialWombatAbstractProcessedInput (SerialWombatPin.SerialWombatPin):
	"""!
	@brief Constructor for the SerialWombatAbstractScaledOutput Class
	
	@param sw A reference to a previously declared SerialWombatPin to which the output is connected.
	"""
	def __init__(self,serial_wombat):
		self._pisw = serial_wombat
		self._pin = 0
		self._swPinModeNumber = 0
		self.PERIOD_1mS = 0
		self.PERIOD_2mS = 1
		self.PERIOD_4mS = 2
		self.PERIOD_8mS = 3
		self.PERIOD_16mS = 4
		self.PERIOD_32mS = 5
		self.PERIOD_64mS = 6
		self.PERIOD_128mS = 7
		self.PERIOD_256mS = 8
		self.PERIOD_512mS = 9
		self.PERIOD_1024mS = 10
		self.OUTPUT_RAW = 0  #<   Use the unfiltered signal for the self._pin's public data 
		self.OUTPUT_FIRST_ORDER_FILTERED = 1 #< Use a first order filtered signal for the self._pin's public data 
		self.OUTPUT_AVERAGE = 2 #< Use an averaged signal for the self._pin's public data (updates less often)
		self.TRANSFORM_NONE = 0  #< Don't transform the input signal
		self.TRANSFORM_SCALE_RANGE = 1  #< Scale the input signal to a 0-65535 value based on input high and low limits
		self.TRANSFORM_LINEAR_MXB = 2  #< Scale the input signal based on a linear mx+b equation

	def abstractProcessedInputBegin(self,pin,pinModeNumber):
		self._swPinModeNumber = pinModeNumber
		self._pin = pin
		self._pisw = self._sw

	"""!
	@brief if enabled subtract the input value from 65535 before doing any other processing.
	
	@param inverted False - input value isn't changed.  True- input value is subtracted from 65535
	
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeInverted(self,inverted):
		invertedInt = 0
		if (inverted):
			invertedInt = 1

		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			3,
			 invertedInt,
			0x55,0x55,0x55]

		result,rx = self._pisw.sendPacket(tx)

		return(result)

	"""!
	@brief Set a first order filtering constant to be applied to the signal  Higher is heavier filtering
	
	The filter samples at 1kHz.
	For a good explanation of 1st order IIR filter calculations, see:
	https://www.monocilindro.com/2017/04/08/how-to-implement-a-1st-order-iir-filter-in-5-minutes/

	Some filter cut-off (3dB down) frequency and constant values:
	- 0.5 Hz  65417
	- 1 Hz 65298   
	- 2 Hz 65062
	- 5 Hz 64358
	- 10 Hz 63202

	Filtering adds lag.  The higher the filter constant value, the longer it takes for the filter to settle 
	when given a steady input.
	
	@param constant  The first order filter constant from 0 to 65535.  Larger constant is heavier filtering
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeFirstOrderFilteringConstant(self, constant):
		tx =bytearray( [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			11]) + SW_LE16(constant) + bytearray([0X55,0X55])
		result,rx = self._pisw.sendPacket(tx)

		return(result)

	"""!
	@brief Set a number of samples to average for each update of the downstream signal
	
	The average is a typical average, not a moving average so the more samples comprise the averaged value
	the less often the downstream value will update.
	
	@param A number of samples to include in each output average.  Samples are typically taken each mS, although
	some modes such as SerialWombatUltrasonicDistanceSensor sample at other periods.
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeAveragingNumberOfSamples(self, numberOfSamples):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			1]) + SW_LE16(numberOfSamples) + bytearray([ 0x55,0x55])

		result,rx = self._pisw.sendPacket(tx)

		return(result)


	"""!
	@brief Sets input value ranges which are discarded rather than processed
	
	Input values that are below the low parameter  or above the high parameter are not processed.
	The last valid input value is repeated instead.  This feature is designed to reject 
	outlier values, not to act as a high or low limiting clamp
	
	@param low input values below this value will not be processed
	@param high input values above this value will not be processsed.
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeExcludeBelowAbove(self, low,  high):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			2]) + SW_LE16(low) + SW_LE16(high)

		result,rx = self._pisw.sendPacket(tx)

		return(result)

	"""!
	@brief Sets up the queueing feature for this self._pin mode.  Queue must have been initialized prior to this queue
	
	Allows periodic storage of the public data value into a previously initialized queue in the user memory buffer.
	The high byte, the low byte, or both can be stored into the queue.  This is useful to increase the number of 
	Samples that can be stored and transferred if 8 bit resolution is sufficent.   
	
	Note that the sampling period is an enumerated type, not a numerical value
	
	@param queue The index into the User Memory Buffer where the queue is located
	@param period The sampling period.  See the enumerated type for values
	@param queueHighByte  Whether to put the high byte of the sample into the queue
	@param queueLowByte Whether to put the low byte of the sample into the queue
	@return returns 0 or higher if success, or a negative error code
	"""
	def configureQueue(self, queue, period,  queueHighByte = True,  queueLowByte = True):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			5]) + SW_LE16(queue.startIndex) + bytearray([ period, ((( queueHighByte) << 1) | queueLowByte)])
		result,rx = self._pisw.sendPacket(tx)
		return(result)

	"""!
	@brief Configures whether the self._pin's public data value is averaged, filtered, or neither
	
	@param outputValue An enumerated type for filtered, averaged, or raw
	"""
	def configureOutputValue(self,outputValue):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			4,
			outputValue,
			0x55,0x55,0x55]

		result,rx = self._pisw.sendPacket(tx)

		return(result)

	"""!
	@brief Scale incoming values to a range of 0 to 65535
	
	This function allows configuration of an input scaling range that maps to 0-65535.  
	For example, if a sensor returns a range from 2000 to 5000, setting the minimum to 2000 and
	maximum to 5000 will cause values below 2000 to be 0, values above 5000 to be 65535, and values
	in between will be scaled accordingly.  This allows a sensor or other input device to scale to the
	Serial Wombat philosophy of using a 16 bit resolution number to represent the the possible range of values
	
	Calling this feature disables writeTransformLinearMXB until the self._pin is reinitialized with begin().
	
	@param min The minimum value of the input range.  Input values less than or equal to that will be scaled to 0
	@param max The maximum value of the input range.  Input values greater or equal to that will be scaled to 65535
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeTransformScaleRange(self, min,  max):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			6]) + SW_LE16(min)+ SW_LE16(max)
		result,rx = self._pisw.sendPacket(tx)
		return(result)

	"""!
	@brief Scale incoming values based on an mx+b linear equation
	
	Allows scaling of an input by multiplying by m, dividing by 256, and adding b.
	The m value can be thought of as a fraction with a divisor of 256.  This allows the scaling
	value to make the input bigger or smaller.  After the multiplication, division and addition
	the result is limited to the range of 0 to 65535.
	Calling this feature disables writeTransformScaleRange until the self._pin is reinitialized with begin().
	
	@param m A value between -16777215 and +1677215 representing the number of 256th by which to multiply the input 
	@param b A value between -65535 and 65535 to add to the result of the multiplication
	@return returns 0 or higher if success, or a negative error code
	"""
	def writeTransformLinearMXB(self,m, b):
		tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			7]) + SW_LE32(m)

		result,rx = self._pisw.sendPacket(tx)

		if (result < 0):
			return(result)

		tx2 = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			8]) + SW_LE32(b)
		result,rx = self._pisw.sendPacket(tx2)

		return(result)

	"""!
	@brief Sort incoming data into one of 5 ranges, and integrate based on linear interpolation in those ranges.

	This funciton is designed to allow a binary or analog input to proportionally increment or decrement a value, such as allowing a joystick to control the position of a servo by changing it over time proportional to the position of the stick.	

	@return Returns a negative value if the configuration caused an error.

	"""

	def configureIntegrator(self, negativeMaxIndex, #!< Values more negative than this will decrement the output value by maxIncrement per sample.
				negativeMidIndex, #!< Values more negative than this will be linearly scaled with negativeMaxIndex, maxIncrement and midIncrement.
						negativeDeadZone, #!< Values between negativeDeadZone and positiveDeadZone will not affect the output value.  Values between negativeDeadZone and negativeMidIndex will be scaled linearly based on 0 and midIncrement
				positiveDeadZone, #!< Values between negativeDeadZone and positiveDeadZone will not affect the output value.  Values between positiveDeadZone and positiveMidIndex will be scaled linearly based on 0 and midIncrement
				positiveMidIndex,#!< Values more positive than this will nearly increment the value scaled with negativeMaxIndex, maxIncrement and midIncrement.
						positiveMaxIndex,#!< Values more positive than this will increment the output value by maxIncrement per sample. 
				midIncrement,  #!< forms a line for scaling between 0 and midIncrement for values between negative or positive deadzone and negative or positive MidIndex
				maxIncrement,  #!< forms a line for scaling between midIncrement and maxIncrement for values between negative or positive midIncrement and negative or positive maxIncrement
				initialValue) : #!< intial integrator value
			
		tx = bytearray( [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
				12]) +  SW_LE16(negativeMaxIndex) +  SW_LE16(negativeMidIndex)
                
		result,rx  = self._pisw.sendPacket(tx)

		if (result < 0):
			return (result)

		tx = bytearray( [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
		self._pin,
		self._swPinModeNumber,
			13]) +                 SW_LE16(negativeDeadZone) +                 SW_LE16(positiveDeadZone)
			
		result,rx = self._pisw.sendPacket(tx)

		if (result < 0):
			return (result)
		tx = bytearray([SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
		self._pin,
		self._swPinModeNumber,
			14]) +                 SW_LE16(positiveMidIndex) +           SW_LE16(positiveMaxIndex)

		result,rx = self._pisw.sendPacket(tx)

		if (result < 0):
				return (result)

		tx = bytearray( [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
		self._pin,
		self._swPinModeNumber,
                15]) +  SW_LE16(initialValue) + bytearray([ 0,0 ])
		result,rx = self._pisw.sendPacket(tx)
		if (result < 0):
			return (result)
                
		tx = bytearray( [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
		self._pin,
		self._swPinModeNumber,
                16]) +   SW_LE16(midIncrement) +                 SW_LE16(maxIncrement)
                
		result,rx = self._pisw.sendPacket(tx)

		return (result)

	"""!
	@brief Enables or disables all input processing functions
	If disabled, the raw input value is placed directly in the self._pin's 16 bit public data buffer
	"""
	def writeProcessedInputEnable(self, enabled):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			0,
			enabled,
			0x55,0x55,0x55]

		result,rx = self._pisw.sendPacket(tx)
		return(result)

	"""!
	@brief Retreive the maximum public data output  value since the last call with reset= True
	
	@param resetAfterRead If True, maximum value is set to 0 after read so that subsequent values become maximum.  
	
	@return A 16 bit unsigned value indicating the maximum value
	"""
	def  readMinimum(self,resetAfterRead = False):
		resetAfterReadInt = 0
		if resetAfterRead:
			resetAfterReadInt = 1
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			9,
			resetAfterReadInt,
			0x55,0x55,0x55]
		result,rx = self._pisw.sendPacket(tx)
		if (result < 0):
			return (65535)
		return(rx[4] + 256*rx[5])

	"""!
	@brief Retreive the maximum public data output  value since the last call with reset= True
	
	@param resetAfterRead If True, maximum value is set to 0 after read so that subsequent values become maximum.  
	
	@return A 16 bit unsigned value indicating the maximum value
	"""
	def readMaximum(self, resetAfterRead = False):
		resetAfterReadInt = 0
		if resetAfterRead:
			resetAfterReadInt = 1
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			10,
			resetAfterReadInt,
			0x55,0x55,0x55]
		
		result,rx = self._pisw.sendPacket(tx)
		if (result < 0):
			return (0)
		return(rx[4] + 256 * rx[5])

	"""!
	@brief Retreive the last completed averaged value
	
	@return The last completed result of the averaging.  Note that because the average is a normal average and not
	a moving average, this value is unlikely to include the most recent raw samples.
	"""
	def readAverage(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			11,
			0x55,0x55,0x55,0x55]
		result,rx =  self._pisw.sendPacket(tx)
		if (result < 0):
			return (0)
		return(rx[4] + 256 * rx[5])

	"""!
	@brief Retreive the filtered value
	
	@brief A 16 bit value representing the First Order IIR filtered result of the input
	"""
	def readFiltered(self):
		tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_INPUTPROCESS,
			self._pin,
			self._swPinModeNumber,
			11,
			0x55,0x55,0x55,0x55]
		result,rx = self._pisw.sendPacket(tx)
		if (result < 0):
			return (0)
		return(rx[6] + 256 * rx[7])
