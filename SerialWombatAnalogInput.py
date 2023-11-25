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

import SerialWombatPin
from SerialWombat import SerialWombatPinMode_t
from SerialWombat import SW_LE16

#include <stdint.h>
#include "SerialWombat.h"

"""! @file SerialWombatAnalogInput.h
"""

class AnalogInputPublicDataOutput():
	AnalogInputPublicDataOutput_Raw = 0  # The raw A/D reading is displayed as public data (default)
	AnalogInputPublicDataOutput_Filtered = 1	# The Filtered A/D reading is displayed as public data (default)
	AnalogInputPublicDataOutput_Averaged = 2	# The Averaged A/D reading is displayed as public data (default)
	AnalogInputPublicDataOutput_Minimum = 3	# The Minimum A/D reading is displayed as public data (default)
	AnalogInputPublicDataOutput_Maximum = 4	# The Maximum A/D reading is displayed as public data (default)


"""!

@brief A class to make analog measurements with the Serial Wombat.

The SerialWombatAnalogInput class is used to make measurements on a given pin.

Any analog-capable pin may be used to make a measurement.

Averaging of samples and first order IIR filtering (1 kHz sampling) of input are available.

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

Declare and initialize a SerialWombatAnalogInput instance for each pin being used as an analog input.

The SW4B_ard_analogInput example included with the Arduino library shows how to use this class.


A Tutorial video is also avaialble:

@htmlonly
<iframe width="560" height="315" src="https://www.youtube.com/embed/self._EKlrEVaEhg" frameborder="0" allow="accelerometer autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
@endhtmlonly

https://youtu.be/self._EKlrEVaEhg

"""
class SerialWombatAnalogInput(SerialWombatPin.SerialWombatPin):

	"""!
	@brief Constructor for the SerialWombatAnalogInput class.
	
	@param SerialWombatChip a reference to the Serial Wombat chip on which the Analog Input will be measured
	"""
	def __init__(self,serial_wombat):
		self._sw = serial_wombat

	"""!
	@brief Initialize an analog input on a given pin.
	
	@param pin The Serial Wombat pin to set.  Valid values for SW4A: 0-3  SW4B: 1-3 SW18AB: 0-4 and 16-19 
	@param averageSamples Number of samples to average.  Valid values for SW4A and SW4B are 0 or 64.
	All non-zero values will be treated as 64 on these platforms.  Default is 64.
	@param filterConstant First Order IIR filter constant, expressed as 1/65536ths .  Default is 65508
	Values closer to 65536 give heavier filtering.  Sample frequency is 1kHz.
	@param publicDataOutput What to output as pin public data.  Default is raw.
	@return Returns a negative error code if initialization failed.
	"""
	def begin(self, pin,  averageSamples = 64,  filterConstant = 0xFF80,  output = AnalogInputPublicDataOutput.AnalogInputPublicDataOutput_Raw):
		self._pin = pin
		self._pinMode = SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT
		tx = [ 200,self._pin,self._pinMode,0,0,0,0,0 ]
		result,rx = self._sw.sendPacket(tx)
		if(result < 0):
			return result
		tx1 = bytearray([ 201,self._pin,self._pinMode]) + SW_LE16(averageSamples) +SW_LE16(filterConstant) + bytearray([output ])
		result, rx =  self._sw.sendPacket(tx1)
		return result
		

	"""!
	@brief Retreive a raw A/D measurement and convert it to mV
	
	Conversion is based on the most recent A/D conversion taken by the 
	Serial Wombat A/D at the command time and the last reference measurement made on the 
	Serial Wombat chip using the SerialWombatChip.readSupplyVoltage_mV() method.  
	@return A 16 bit unsigned value indicating measurement in mV
	"""
	def readVoltage_mV(self):
		reading = self._sw.readPublicData(self._pin)
		x = reading * self._sw.self._supplyVoltagemV
		returnval = x >> 16
		return (returnval)


	"""!
	@brief Retreive a raw A/D measurement
	
	Conversion is based on the most recent A/D conversion taken by the 
	Serial Wombat A/D at the command time.
	
	All Serial Wombat products will return a 16-bit value.  However
	the SW4A and SW4B products only have 10-bit A/D converters, so
	the returned value moves by 64 counts at a time, except for the topmost value.
	 For all 
	Serial Wombat products, the highest possible reading (0xFFC0 for the SW4A/SW4B, 0xFFF0 for the SW18AB)
	is changed to 0xFFFF to indicate maximum possible hardware value.
	
	@return A 16 bit unsigned value indicating the counts of the A/D conversion
	"""
	def readCounts(self):
		return (self._sw.readPublicData(self._pin))


	"""!
	@brief Retreive a filtered A/D measurement and convert it to mV
	
	Conversion is based on the most recent filtered A/D result taken by the 
	Serial Wombat A/D at the command time and the last reference measurement made on the 
	Serial Wombat chip using the SerialWombatChip.readSupplyVoltage_mV() method.  
	@return A 16 bit unsigned value indicating measurement in mV
	"""
	def readFiltered_mV(self) :
		x = self.readFilteredCounts() # Counts ranging from 0 to 65535
		x *= self._sw.self._supplyVoltagemV
		return (x >> 16)


	"""!
	@brief Retreive a filtered A/D measurement
	
	Conversion is based on the most recent filtered A/D value taken by the 
	Serial Wombat A/D at the command time.
	
	
	@return A 16 bit unsigned value indicating the filtered A/D result
	"""
	def readFilteredCounts(self):
		tx = [ 204,self._pin,self._pinMode,0x55,0x55,0x55,0x55,0x55 ]
		#TODO add other send packet parameters  --- count,rx = self._sw.sendPacket(tx, True, 3,1)
		count,rx = self._sw.sendPacket(tx)
		return(rx[5] + rx[6] * 256)


	"""!
	@brief Retreive an averaged A/D measurement and convert it to mV
	
	Conversion is based on the most recent averaged A/D result taken by the 
	Serial Wombat A/D at the command time and the last reference measurement made on the 
	Serial Wombat chip using the SerialWombatChip.readSupplyVoltage_mV() method.  
	@return A 16 bit unsigned value indicating measurement in mV
	"""
	def readAveraged_mV(self):
		x = self.readAveragedCounts() # Counts ranging from 0 to 65535
		x *= self._sw.self._supplyVoltagemV
		return (x >> 16)


	"""!
	@brief Retreive an averaged A/D measurement
	
	Conversion is based on the most recent averaged A/D value taken by the 
	Serial Wombat A/D at the command time.
	
	All Serial Wombat products will return a 16-bit value.  However
	the SW4A and SW4B products only have 10-bit A/D converters.  Averaging will potentially
	increase the effective resolution slightly for signals that have a small amount of
	randomly distributed noise.  
	
	@return A 16 bit unsigned value indicating the counts of the A/D conversion
	"""
	def readAveragedCounts(self):
		tx = [ 204,self._pin,self._pinMode,0x55,0x55,0x55,0x55,0x55 ]
		count, rx = self._sw.sendPacket(tx)
		return(rx[3] + rx[4] * 256)


	#! @brief Provides a wrapper around the readSupplyVoltage_mV() method for the SerialWombat chip hosting this pin mode
	def updateSupplyVoltage_mV(self):
		return  self._sw.readSupplyVoltage_mV()



	"""!
	@brief Retreive the maximum single sample A/D value in mV
	 
	The maximum value the Serial Wombat chip has seen on that pin since last reset of Min/Max
	
	@param resetAfterRead If True, maximum value is set to 0 after read so that subsequent values become maximum.  Also resets minimum to next sample.
	
	@return A 16 bit unsigned value indicating measurement in mV
	"""
	def readMaximum_mV(self,  resetAfterRead = False):
		tx = [ 203,self._pin,self._pinMode,0,0x55,0x55,0x55,0x55 ]	 
		if(resetAfterRead):
			tx[3] = 1
		count,rx = self._sw.sendPacket(tx)
		return(rx[5] + rx[6] * 256)


	"""!
	@brief Retreive the maximum single sample A/D value in counts
	 
	The maximum value the Serial Wombat chip has seen on that pin since last reset of Min/Max
	
	@param resetAfterRead If True, maximum value is set to 0 after read so that subsequent values become maximum.  Also resets minimum to next sample.
	
	@return A 16 bit unsigned value indicating maximum A/D Counts
	"""
	def readMaximumCounts(self, resetAfterRead = False):
		tx = [ 203,self._pin,self._pinMode,0,0x55,0x55,0x55,0x55 ]
		if(resetAfterRead):
			tx[3] = 1
		count,rx = self._sw.sendPacket(tx)
		return(rx[5] + rx[6] * 256)

	"""!
	@brief Retreive the minimum single sample A/D value in mV
	 
	The minimum value the Serial Wombat chip has seen on that pin since last reset of Min/Max
	
	@param resetAfterRead If True, minimum value is set to 0 after read so that subsequent values become minimum.  Also resets maximum to next sample.
	
	@return A 16 bit unsigned value indicating measurement in mV
	"""
	def readMinimum_mV(self, resetAfterRead = False):
		x = self.readMaximumCounts(resetAfterRead) # Counts ranging from 0 to 65535
		x *= self._sw.self._supplyVoltagemV
		return (x >> 16)


	"""!
	@brief Retreive the maximum single sample A/D value in counts
	 
	The maximum value the Serial Wombat chip has seen on that pin since last reset of Min/Max
	
	@param resetAfterRead If True, maximum value is set to 0 after read so that subsequent values become maximum.  Also resets minimum to next sample.
	
	@return A 16 bit unsigned value indicating maximum A/D Counts
	"""
	def readMinimumCounts(self, resetAfterRead = False):
		tx = [ 203,self._pin,self._pinMode,0,0x55,0x55,0x55,0x55 ]
		if(resetAfterRead):
			tx[3] = 1
		count,rx = self._sw.sendPacket(tx)
		return(rx[3] + rx[4] * 256)

	
"""#TODO
#! @brief This class extends SerialWombatAnalogInput with SW18AB specific capabilities
class SerialWombatAnalogInput_18AB : public SerialWombatAnalogInput, public SerialWombatAbstractProcessedInput

public:

	SerialWombatAnalogInput_18AB(SerialWombatChip& serialWombat):SerialWombatAnalogInput(serialWombat),SerialWombatAbstractProcessedInput(serialWombat){}

	 pin() { return self._pin }
	 swPinModeNumber() { return self._pinMode }
}
"""

