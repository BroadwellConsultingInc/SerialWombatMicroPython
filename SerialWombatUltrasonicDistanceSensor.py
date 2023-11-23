import SerialWombatPin

class SerialWombatUltrasonicDistanceSensor (SerialWombatPin.SerialWombatPin):

    def __init__(self,sw):
        self._sw = sw

    def begin(self,echoPin, driver, triggerPin, autoTrigger = True, pullUp = False):
        self._pin = echoPin
        self._pinMode =  27 # Ultrasonic Distance

        tx = [200, self._pin, self._pinMode,driver, triggerPin, pullUp, autoTrigger, 0x55]
        self._sw.sendPacket(tx)

    def readPulseCount(self):
        tx = [202, self._pin, self._pinMode,0x55,0x55,0x55,0x55,0x55]
        count,rx= self._sw.sendPacket(tx)
        if (count >= 0):
            return (rx[5] + 256*rx[6])
        else:
            return(0)

    def manualTrigger(self):
        tx = [201, self._pin, self._pinMode,1,0x55,0x55,0x55,0x55]
        self._sw.sendPacket(tx)

    



