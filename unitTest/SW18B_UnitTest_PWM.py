import SW18B_UnitTest_globals
import SerialWombatPWM
import time




PWM_TEST_INCREMENTS = 100


PWM_FIRSTPIN = 0
PWM_LASTPIN = 19

def pwmTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SWPWM0 = SerialWombatPWM.SerialWombatPWM_18AB(SW6B)
    PWM_NUM_TEST_PINS = SW18B_UnitTest_globals.NUM_TEST_PINS
    SW18B_UnitTest_globals.resetAll()
    for pin in range(PWM_FIRSTPIN,PWM_LASTPIN + 1):
        if (not SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
            continue
        SW18B_UnitTest_globals.initializePulseReaduS(pin)
    
    for period in range(2500,60000,1000):
        for reverse in range(0,2):
            for i in range(1000,65535,5000):
                for pin in range(PWM_FIRSTPIN, PWM_LASTPIN + 1):
                    if (not SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
                        continue               
                    setting = (i + (pin * 63000 // PWM_NUM_TEST_PINS) ) & 0xFFFF
                    expected = (period * setting // 65536) & 0xFFFF
                    if (expected < 30 or period - expected < 30):
                        continue
                    SWPWM0.begin(pin)
                    SWPWM0.writePeriod_uS(period)
                    SWPWM0.writeDutyCycle(setting)
                time.sleep(0.100)
                for pin in range(PWM_FIRSTPIN, PWM_LASTPIN + 1):
                    if (not SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
                        continue   
                    result = SW18B_UnitTest_globals.pulseRead(pin)
                    setting = (i + (pin * 63000 // PWM_NUM_TEST_PINS) ) & 0xFFFF
                    expected = (period * setting // 65536) & 0xFFFF
                    if (expected < 30 or period - expected < 30):
                        continue
                    SW18B_UnitTest_globals.test(f"PWM pin: {pin} period:{period} reverse:{reverse} i: {i}",result,expected,20,4)


