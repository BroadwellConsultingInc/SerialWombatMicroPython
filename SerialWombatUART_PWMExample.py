import time
import SerialWombatUART
import SerialWombatPWM

sw = SerialWombatUART.SerialWombatChipUART("COM19")

sw.begin(True)

print(sw.version)
print(sw.model)
print(sw.fwVersion)


pwm = SerialWombatPWM.SerialWombatPWM(sw)




print("Source Voltage mv: ",sw.readSupplyVoltage_mV())

time.sleep(2)

pwm.begin(18)
pwm.writeDutyCycle(0x8000)
