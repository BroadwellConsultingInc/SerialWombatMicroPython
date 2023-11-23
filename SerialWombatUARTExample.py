import time
import SerialWombatUART
import SerialWombatWS2812

sw = SerialWombatUART.SerialWombatChipUART("COM19")

sw.begin(False)

print(sw.version)
print(sw.model)
print(sw.fwVersion)


led = SerialWombatWS2812.SerialWombatWS2812(sw)

led.begin(19, 
                     4, 
                     0) # Trigger pin





print("Source Voltage mv: ",sw.readSupplyVoltage_mV())

time.sleep(2)
led.write(0,0x0F0000)
led.write(1,0x000F00)
led.write(2,0x00000F)
led.write(3,0x0F0F0F)

