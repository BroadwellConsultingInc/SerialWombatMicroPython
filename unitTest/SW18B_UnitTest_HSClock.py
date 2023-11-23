import SW18B_UnitTest_globals
import SerialWombatHSClock
import time



def hsClockTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    HSClock = SerialWombatHSClock.SerialWombatHSClock (SW6B)

    SW18B_UnitTest_globals.resetAll()
    HSClock.begin(15,2000)
    SW18B_UnitTest_globals.initializePulseReaduS(15)
    SW18B_UnitTest_globals.delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(15)
    SW18B_UnitTest_globals.test("HSCLOCK_00", highTime, 250,10);  # Should be a 250 uS high time (500us period)

    SW18B_UnitTest_globals.resetAll()
  