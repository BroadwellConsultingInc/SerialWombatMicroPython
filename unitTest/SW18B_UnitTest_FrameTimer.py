import SW18B_UnitTest_globals
import SerialWombat
import SerialWombatThroughputConsumer
import SerialWombatPWM
import time
from ArduinoFunctions import delay
from ArduinoFunctions import millis



def frameTimerTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    tc = SerialWombatThroughputConsumer.SerialWombatThroughputConsumer(SW6B)
    tc.begin(17)
    tc.writeAll(200)
    SW6B.writeFrameTimerPin(15)
    SW18B_UnitTest_globals.initializePulseReaduS(15);
    delay(2000)
    highTime = SW18B_UnitTest_globals.pulseRead(15);
    systemUtilization = SW6B.readPublicData(74) #SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_SYSTEM_UTILIZATION)
    SW18B_UnitTest_globals.test("FrameTimer_00", highTime, (systemUtilization * 1000 ) >>16 ,50);  

    tc.writeAll(400);
    delay(2000);
    highTime = SW18B_UnitTest_globals.pulseRead(15);
    systemUtilization = SW6B.readPublicData(74)#SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_SYSTEM_UTILIZATION)
    SW18B_UnitTest_globals.test("FrameTimer_01", highTime, (systemUtilization * 1000 ) >>16 ,50);  


    SW18B_UnitTest_globals.resetAll()
  