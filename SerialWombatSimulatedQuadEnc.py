import SerialWombat
from SerialWombatPin import SerialWombatPin
#from SerialWombat import SW_LE32
#from enum import IntEnum
import time

#include <stdint.h>
#include "SerialWombat.h"


SIMQE_IDLE = 0,
SIMQE_1ST_TRANSITION_1ST_PIN_COMPLETED =1 ,
SIMQE_1ST_TRANSITION_2ND_PIN_COMPLETED = 2,
SIMQE_2ND_TRANSITION_1ST_PIN_COMPLETED = 3,
SIMQE_2ND_TRANSITION_2ND_PIN_COMPLETED = 4,
SIMQE_2ND_TRANSITION_COMPLETED = 4


"""! \brief A class for testing SerialWombatQuadEnc inputs.

This class uses digital IO calls to simulate the output of a quadrature encoder.  This is used to unit test
the SerialWombatQuadEnc class.  All processing occurs on the Arduino side.  This class does not currently
wrap a pin mode on the Serial Wombat chip.  See the Unit Test example sketch for usage.

"""
class SerialWombatSimulatedQuadEnc:
	def __init__(self, serialWombat0, serialWombat1, _pin0, _pin1, _openDrain, _doubleTransition): 

		self.doubleTransition = False
		self.state = SIMQE_IDLE

		self.currentPosition = 0
		self.targetPosition = 0
		self.delayAfterFirstPinFirstTransition_mS = 20
		self.delayAfterSecondPinFirstTransition_mS = 20
		self.delayAfterFirstPinSecondTransition_mS = 20
		self.delayAfterSecondPinSecondTransition_mS = 20
		self.openDrain = True
		self.lastTransitionTime_millis = 0

		self.pin0State = True
		self.pin1State = True
		self.pin0 = _pin0
		self.pin1 = _pin1
		self.openDrain = _openDrain
		self.doubleTransition = _doubleTransition

		self.sw0 = serialWombat0
		self.sw1 = serialWombat1

		self.millisStart = time.ticks_ms()
		self.initialize()


	def millis(self):
		return(int(time.ticks_ms() - self.millisStart))
	def bothPinsHigh(self):
		self.pin0High()
		self.pin1High()

	def togglePin0(self):
		if (self.pin0State):
			self.pin0Low()
		else:
			self.pin0High()

	def togglePin1(self):
		if (self.pin1State):
			self.pin1Low()
		else:
			self.pin1High()

	def pin0High(self):
		self.sw0.digitalWrite(self.pin0, 1)
		self.pin0State = True

	def pin1High(self):
		self.sw1.digitalWrite(self.pin1, 1)
		self.pin1State = True


	def pin0Low(self):
		self.sw0.digitalWrite(self.pin0, 0)
		self.pin0State = False

	def pin1Low(self):
		self.sw1.digitalWrite(self.pin1, 0)
		self.pin1State = False

	def service(self):
		if (self.currentPosition != self.targetPosition):
			if (self.state == SIMQE_IDLE):
				if (self.currentPosition != self.targetPosition):
					self.lastTransitionTime_millis = self.millis()
					if (self.currentPosition < self.targetPosition):
						self.togglePin0()
					else :
						self.togglePin1()					
					self.state = SIMQE_1ST_TRANSITION_1ST_PIN_COMPLETED

			if (self.state == SIMQE_1ST_TRANSITION_1ST_PIN_COMPLETED):
				if (self.millis() > self.lastTransitionTime_millis + self.delayAfterFirstPinFirstTransition_mS):
					self.lastTransitionTime_millis = self.millis()
					if (self.currentPosition < self.targetPosition):
						self.togglePin1()
						if (not self.doubleTransition):
							self.currentPosition += 1
					else:
						self.togglePin0()
						if (not self.doubleTransition):
							self.currentPosition -= 1

					
					
					self.state = SIMQE_1ST_TRANSITION_2ND_PIN_COMPLETED

			if (self.state == SIMQE_1ST_TRANSITION_2ND_PIN_COMPLETED):
				if (self.millis() > self.lastTransitionTime_millis + self.delayAfterFirstPinSecondTransition_mS):
					if (self.doubleTransition):
						self.lastTransitionTime_millis = self.millis()
						if (self.currentPosition < self.targetPosition):
							self.togglePin0()
						else:
							self.togglePin1()
						
							self.state = SIMQE_2ND_TRANSITION_2ND_PIN_COMPLETED
					else:
						self.state = SIMQE_IDLE
			if (self.state == SIMQE_2ND_TRANSITION_1ST_PIN_COMPLETED):
				if (self.millis() > self.lastTransitionTime_millis + self.delayAfterSecondPinFirstTransition_mS):
					self.lastTransitionTime_millis = self.millis()
					if (self.currentPosition < self.targetPosition):
						self.togglePin1()
						self.currentPosition += 1
					else:
						self.togglePin0()
						self.currentPosition -= 1

					self.state = SIMQE_1ST_TRANSITION_2ND_PIN_COMPLETED

			if (self.state == SIMQE_2ND_TRANSITION_2ND_PIN_COMPLETED):
				if (self.millis() > self.lastTransitionTime_millis + self.delayAfterFirstPinSecondTransition_mS):
						self.state = SIMQE_IDLE
		return (self.state == SIMQE_IDLE)


	def initialize(self):
			self.sw0.pinMode(self.pin0, 1, False, self.openDrain)
			self.sw1.pinMode(self.pin1, 1, False, self.openDrain)
			self.bothPinsHigh()
			self.currentPosition = 0
			self.targetPosition = 0
			self.lastTransitionTime_millis = 0
