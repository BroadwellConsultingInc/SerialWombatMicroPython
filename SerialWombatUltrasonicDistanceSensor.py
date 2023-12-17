#pragma once
"""
Copyright 2020-2021 Broadwell Consulting Inc.

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
import SerialWombatAbstractProcessedInput
from SerialWombat import SW_LE16

"""! @file SerialWombatUltrasonicDistanceSensor.h
"""

"""! @brief A Class which uses one or two Serial Wombat 18AB pins to measure distance using an Ultrasonic distance sensor.  


A video Tutorial on this pin mode is available:

@htmlonly
//TODO
@endhtmlonly

//TODO https://youtu.be/


"""

class SerialWombatUltrasonicDistanceSensor ( SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput):
	"""
	@brief Class constructor for SerialWombatPulseTimer
	@param serialWombat The Serial Wombat chip on which the SerialWombatPulseTimer pinmode will be run
	"""
	def __init__(self,serial_wombat):
		super().__init__(serial_wombat)
		self._sw = serial_wombat
		self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_ULTRASONIC_DISTANCE

	#enum driver {
	#HC_SR04 = 0,  < Standard buffered mode.  Colors are uploaded by the host
	#}

	"""	
	 @brief Initialization routine for SerialWombatUltrasonicDistanceSensor
	 
	 @param echoPin Pin used to time input pulses.  For 5V sensors, 5V tolerant pins 9,10,11,12, 14 and 15 are good choices
	 @param driver Chip used for distance measurement.  Currently only HC_SR04 is supported.
	 @param triggerPin Pin used for triggering the sensor.  If same as echo pin (e.g. 3 pin sensors) set equal to echoPin
	 @return 0 or higher if successful, negative error code if not successful.
	"""	

	def begin(self,echoPin, driver, triggerPin,autoTrigger = True,  pullUp = False):
		self._pin = echoPin
		tx = [ 200,self._pin,self._pinMode,driver, triggerPin, pullUp,autoTrigger, 0x55 ]
		result,rx = self._sw.sendPacket(tx)
		self.abstractProcessedInputBegin(self._pin,self._pinMode)
		return(result)

	"""	
	 @brief get the number of pulses that have been sent.  
	
	 @return The number of pulses that have been sent.  Rolls over at 65536
	"""	
	def	 readPulseCount(self):
		tx = [ 202,self._pin,self._pinMode,0x55,0x55,0x55,0x55, 0x55 ]
		result,rx = self._sw.sendPacket(tx)
		if(result  >= 0):
				return (rx[5] + 256 * rx[6])
		else:
				return 0



	"""	
	 @brief Manually trigger a distance reading
	
	 Use this interface to trigger a reading if begin was called with autoTrigger = false
	 @return 0 or higher if successful, negative error code if not successful.
	"""	
	def manualTrigger(self):
		tx = [ 201,self._pin,self._pinMode,1,0x55,0x55,0x55, 0x55 ]
		
		result,rx = self._sw.sendPacket(tx)
		return(result)

