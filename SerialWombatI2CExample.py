import time
import RPi.GPIO as GPIO
import SerialWombatPigpioI2c
import SerialWombatServo
import SerialWombatAnalogInput
import SerialWombatQuadEnc


GPIO.setwarnings(False)

sw = SerialWombatPigpioI2c.SerialWombatChipPigpioI2c(17,27,0x6D)

sw.begin(False)

print(sw.version)
print(sw.model)
print(sw.fwVersion)

servo = SerialWombatServo.SerialWombatServo(sw)
servo.attach(3)

analog = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog.begin(2)

knob = SerialWombatQuadEnc.SerialWombatQuadEnc(sw)
knob.begin(0,1,10)

print("Pin 2 analog: ",analog.readPublicData())

print("Source Voltage mv: ",sw.readSupplyVoltage_mV())

time.sleep(2)
while(True):
    print(knob.read()," ",analog.readCounts())
    servo.write16bit(analog.readCounts())