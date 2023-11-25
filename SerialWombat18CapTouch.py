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
from SerialWombat import SW_LE32
from SerialWombat import SW_LE16


"""!
@brief A class that controls a Cap Touch Pin on the Serial Wombat 18AB chip

This class allows a metalic plate with a thin insulating layer to be used
as a capacitive touch surface.  Items like a coin, PCB board, metal plate, etc
can be connected directly to the pin and covered by a thin insulating layer.
A finger touch can be detected by the change in capacitance caused by its presence.

The mode can output either analog or digital values back to the host and as public
data to other pins.  In analog mode the A/D reading at the end of a charge cycle is
presented.  This value gets smaller when a finger or item causes the capacitance of
the sensor to increase.  (Smaller A/D values when finger present, higher values when
absent).

In digital mode the class is configured with a high and low limit which cause a
digital change in hysteresis manner.  This is useful when treating the touch
sensor like a button.   In digital mode the class implements the same interfaces
as the SerialWombatDebouncedInput class so that physical buttons and cap touch
inputs can be treated equivalently.    Settign the high and low limits further apart
will decrease the chance of false transitions but will also typically decrease the
responsiveness of the sensor.



Output public data values for touched and not touched are configurable.  This allows
other pin modes to react based on touch.  For instance, the touch and not touched
values might be set to 0x4000 and 0xC000 so that a servo set to monitor that public
data would move back and forth between 25% and 75% of its range depending on
whether or not a touch is present.

The final touch value is the result of 8 averaged samples in firmware remove noise. 

For particularly noisy signals a debounce option is also avaialble.  This requires
the specified number of samples to match before a transition is detected.  This
can help eliminate false transitions but makes the system less reponsive in terms of time
to transition after a touch is made or removed.

The Cap touch pin mode in the firmware takes exclusive access to the Microcontroller's
A/D hardware for a few milliseconds at a time.  This isn't an issue for most users
if the default 5ms delay between samples is used.  However, it should be considered
if multiple Cap Touch pins are being used simultaneously or if the delay is
decreased as they may combine to
starve other analog chanels and make conversions sporadic, affecting filtering and
averaging.  This may also 
impact performance of real-time control pin modes run on the Serial Wombat chip
such as PID control.

A Tutorial video is also avaialble:
https://youtu.be/c4B0_DRVHs0
@htmlonly
<iframe width = "560" height = "315" src = "https://www.youtube.com/embed/c4B0_DRVHs0" frameborder = "0" allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>< / iframe>
@endhtmlonly

"""
class SerialWombat18CapTouch(SerialWombatPin):

	def __init__(self,serial_wombat):
		self._sw = serial_wombat
		self._trueOutput = 1
		self._falseOutput = 1
		self.transitions = 0


	"""!	
	@brief Initialize the SerialWombat18CapTouch instance with a given charge Time in uS
	
	Required Charge time will vary by touch plate size, insulation and material.  See
	YouTube video and example for usage.
	
	@param pin The pin on which the Cap Touch should run.  Needs to be an Analog Capable pin
	@param chargeTime Charge time in uS for capacitive charging.  
	@param delay Sets how long to wait between samples in mS.  This may be useful since the
	Cap Touch pin mode monopolizes the A/D converter while a measurement is in progress.
	"""
	def begin(self,  pin, chargeTime, delay = 10):
		self._pin = pin
		self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_SW18AB_CAPTOUCH

		tx = bytearray([ 200,self._pin, 22]) + SW_LE16(chargeTime) +  SW_LE16(delay) + bytearray([0x55 ])

		result, rx = self._sw.sendPacket(tx)
		return result


	"""!
	@brief Make a cap touch behave like a digital button
	
	This method sets limits for touch present and absent, and makes the 
	pin report digitally rather than analog.  See video and example
	for calibration routine.
	
	@param touchLimit The calibrated value below which an A/D reading indicates touch present
	@param noTouchLimit The calibrated value above which an A/D reading indicates no touch present
	@param invert Invert the touch result
	@param debounceCount number of consecutive digital samples that must match to change state
	"""
	def makeDigital(self,  touchLimit,  noTouchLimit,  touchValue = 1,  noTouchValue = 0,  invert = False, debounceCount = 0):
		tx1 = bytearray([ 201,self._pin,22]) + SW_LE16(touchLimit) + SW_LE16(noTouchLimit) + bytearray([0x55 ])
		result,rx = self._sw.sendPacket(tx1)
		if (result < 0):
			return (result)

		self._trueOutput = touchValue
		self._falseOutput = noTouchValue
		tx2 = bytearray([ 202,self._pin,22 ]) + SW_LE16(touchValue) + SW_LE16(noTouchValue) + bytearray([0x55 ])
		result,rx = self._sw.sendPacket(tx2)
		if (result < 0):
			return (result)
		tx3 = bytearray([ 203,self._pin,22,1])
		if (invert):
			tx3 += bytearray([1])
		else:
			tx3 += bytearray([0])
		tx3 += SW_LE16(debounceCount) + bytearray([0x55 ])
		result,rx = self._sw.sendPacket(tx3)
		if (result < 0):
			return (result)
		return(0)

	def makeAnalog(self):
		tx3 = [ 203,self._pin,22,0, 0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx3)
		return result

	"""!
	@brief Returns the debounced state of the input
	
	This function reads from the public data of the pin which 
	indicates the debounced and invert adjusted state of the
	input
	@return TRUE or FALSE.  Meaning depends on inversion setting
	"""
	def digitalRead(self ):
		tx = [ 204,self._pin,22,0,0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx)
		if (result >= 0):
			return(rx[3] > 0)
		return(False)

	"""!
	@brief return the number of mS that the debounced input has been in true state
	
	Note that this value starts incrementing after the debounce period, not after the physical pin transition.
	
	@return returns a value in mS which saturates at 65535.  Returns 0 if currently false.
	"""
	def readDurationInTrueState_mS(self):
		tx = [ 204,self._pin,22,1,0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx)

		self.transitions += (256 * rx[5] + rx[4])
		if (rx[3] == 0):
			return (0)
		return(256 * rx[7] + rx[6])

	"""!
	@brief return the number of mS that the debounced input has been in false state
	
	Note that this value starts incrementing after the debounce period, not after the physical pin transition.
	
	@return returns a value in mS which saturates at 65535.  Returns 0 if currently true.
	"""
	def readDurationInFalseState_mS(self ):
		tx = [ 204,self._pin,22,1,0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx)

		self.transitions += (256 * rx[5] + rx[4])

		if (rx[3] == 1):
			return (0)
		return(256 * rx[7] + rx[6])



	"""!
	@brief Queries the number of transistions that have occured on the debounced input
	
	This function queries the debounced input for current state and transitions since last call.
	transition count is put in the global member transitions.  The debounced input in the Serial
	Wombat resets its count to zero after this call.
	
	@return TRUE or FALSE, current status of debounced input
	"""
	def readTransitionsState(self ):
		tx = [ 204,self._pin,22,1,0x55,0x55,0x55,0x55 ]
		result, rx = self._sw.sendPacket(tx)
		self.transitions = (256 * rx[5] + rx[4])
		return (rx[3] > 0)
