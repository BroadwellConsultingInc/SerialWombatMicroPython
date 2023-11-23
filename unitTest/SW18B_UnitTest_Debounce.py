import SW18B_UnitTest_globals
import SerialWombatPWM
import SerialWombatDebouncedInput
import time
from SW18B_UnitTest_globals import delay

def debounceTest():
    SW18B_UnitTest_globals.resetAll()
    SW6B = SW18B_UnitTest_globals.SW6B
    SW6D = SW18B_UnitTest_globals.SW6D
    DBPWM5 = SerialWombatPWM.SerialWombatPWM_4AB(SW6D)
    DBPWM5.begin(SW18B_UnitTest_globals.SW18B_5_MATCH_PIN);
    DBPWM5.setFrequency_SW4AB(DBPWM5.SW4AB_PWMFrequency_125_Hz)
    DBPWM5.writeDutyCycle(0x8000)
    debouncedInput = SerialWombatDebouncedInput.SerialWombatDebouncedInput(SW6B)
    debouncedInput.begin(5,6,False,False) # 6ms time
    delay(500)
    debouncedInput.readTransitionsState()
    if (debouncedInput.transitions < 2):
        SW18B_UnitTest_globals.testPassed(1)
    else:
       SW18B_UnitTest_globals.testFailed(1)

    DBPWM5.setFrequency_SW4AB(DBPWM5.SW4AB_PWMFrequency_63_Hz);
    DBPWM5.writeDutyCycle(0x8000); #8 ms
    delay(500)
    debouncedInput.readTransitionsState()
    if (debouncedInput.transitions < 15):
       SW18B_UnitTest_globals.testFailed(2)
    else:
       SW18B_UnitTest_globals.testPassed(2)


    DBPWM5.begin(SW18B_UnitTest_globals.SW18B_5_MATCH_PIN)
    DBPWM5.setFrequency_SW4AB(DBPWM5.SW4AB_PWMFrequency_125_Hz)
    DBPWM5.writeDutyCycle(0xF000)
    delay(100)
    if (debouncedInput.readTransitionsState()):
               SW18B_UnitTest_globals.testPassed(3)
    else:
       SW18B_UnitTest_globals.testFailed(3)


    DBPWM5.writeDutyCycle(0x1000); 
    delay(100);
    if (debouncedInput.readTransitionsState()):
       SW18B_UnitTest_globals.testFailed(4)
    else:
       SW18B_UnitTest_globals.testPassed(4)

