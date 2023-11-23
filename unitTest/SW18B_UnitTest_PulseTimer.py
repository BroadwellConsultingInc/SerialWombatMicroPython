import SW18B_UnitTest_globals
import SerialWombatPulseTimer
import SerialWombatPWM
import time
import machine
import SW18B_UnitTest_globals
from ArduinoFunctions import delay
from ArduinoFunctions import millis


def pulseTimerTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW6D = SW18B_UnitTest_globals.SW6D
    SW6E = SW18B_UnitTest_globals.SW6E
    SW18B_UnitTest_globals.resetAll()
    SWPWM5 = SerialWombatPWM.SerialWombatPWM_4AB (SW6D)
    SWPWM19 = SerialWombatPWM.SerialWombatPWM_4AB (SW6E)
    SWPulseTimer5 = SerialWombatPulseTimer.SerialWombatPulseTimer (SW6B);
    SWPulseTimer19 = SerialWombatPulseTimer.SerialWombatPulseTimer (SW6B)
    
    setting = 0x2000

    SWPWM5.begin(2)
    SWPWM19.begin(1)


    SWPWM5.setFrequency_SW4AB(SWPWM5.SW4AB_PWMFrequency_16_Hz)
    SWPWM19.setFrequency_SW4AB(SWPWM19.SW4AB_PWMFrequency_16_Hz)
    SWPWM5.writeDutyCycle(setting)

    SWPulseTimer5.begin(5)
    SWPulseTimer19.begin(19)
    startTime_millis = millis();
    for setting in range(2000,65535,1000):
    
      SWPWM5.writeDutyCycle(setting);
      SWPWM19.writeDutyCycle(setting);

      delay(100)

      pt5h = SWPulseTimer5.readHighCounts();
      pt19h = SWPulseTimer19.readHighCounts();
      pt5l = SWPulseTimer5.readLowCounts();
      SW18B_UnitTest_globals.test(f"Pulse A5: ",pt5h,setting,20,3)
      """
      if ( (pt5h > setting + setting / 20) or (pt5h < setting - setting / 20)):
        fail(setting);
        Print("FailA 5: ");
        Serial.print(setting);
        Serial.print(" ");
        Serial.println(SWPulseTimer5.readHighCounts());
      }
      else
      {
        pass(0);
      }
      """
      SW18B_UnitTest_globals.test(f"Pulse A19: ",pt19h,setting,20,3)
      """      if ( (pt19h > setting + setting / 20u) || (pt19h < setting - setting / 20u))
      {
        fail(setting);
        Serial.print("FailB 19: ");
        Serial.print(setting);
        Serial.print(" ");
        Serial.println(SWPulseTimer19.readHighCounts());
      }
      else
      {
        pass(0);
      }
    """
      measuredDuty5 = 0;

      if ((pt5h + pt5l) > 0):
        measuredDuty5 = (pt5h * 65536) // (pt5h + pt5l)

        SW18B_UnitTest_globals.test(f"Pulse D5: ",measuredDuty5
                                    ,setting,20,3)
        """
      if ( (measuredDuty5 > setting + setting / 20u) || (measuredDuty5 < setting - setting / 20u))
      {
        fail(setting);
        Serial.print("FailC 5 duty: ");
        Serial.print(setting);
        Serial.print(" ");
        Serial.println(measuredDuty5);
      }
      else
      {
        pass(0);
      }
      """

     
      if (pt5h + pt5l) > 0:
        measuredDuty19 = pt5h * 65536 // (pt5h + pt5l)
        SW18B_UnitTest_globals.test(f"Pulse D19: ",measuredDuty19
                                    ,setting,20,3)
        """
      if ( (measuredDuty19 > setting + setting / 20u) || (measuredDuty19 < setting - setting / 20u))
      {
        fail(setting);
        Serial.print("FailD 19 duty: ");
        Serial.print(setting);
        Serial.print(" ");
        Serial.println(measuredDuty19);
      }
      else
      {
        pass(0);
      }

    }
    """
    pulses5 = SWPulseTimer5.readPulses();
    pulses19 = SWPulseTimer19.readPulses();
    endTime_millis = millis();

    expectedPulses = (endTime_millis - startTime_millis) * 16 // 1000
    SW18B_UnitTest_globals.test(f"Pulse PC5: ",pulses5,expectedPulses,2,3)
    """
    if ( (pulses19 > (expectedPulses + expectedPulses / 20 + 2u)) || (pulses19 < (expectedPulses - expectedPulses / 20u - 2u))):
    {
      fail(setting);
      Serial.print("FailE Pulses 19: ");
      Serial.print(expectedPulses);
      Serial.print(" ");
      Serial.println(pulses19);
    }
    else
    {
      pass(0);
    }
    """
    SW18B_UnitTest_globals.test(f"Pulse PC19: ",pulses19,expectedPulses,2,3)
    """
    if ( (pulses5 > (expectedPulses + expectedPulses / 20u + 2u)) || (pulses19 < (expectedPulses - expectedPulses / 20u - 2u)))
    {
      fail(setting);
      Serial.print("FailF Pulses 5: ");
      Serial.print(expectedPulses);
      Serial.print(" ");
      Serial.println(pulses19);
    }
    else
    {
      pass(0);
    }
    """

    SW18B_UnitTest_globals.resetAll()
    setting = 0x2000;

    SWPWM5.begin(2)
    SWPWM19.begin(1)


    SWPWM5.setFrequency_SW4AB(SWPWM5.SW4AB_PWMFrequency_1_Hz)
    SWPWM19.setFrequency_SW4AB(SWPWM5.SW4AB_PWMFrequency_1_Hz)
    SWPWM5.writeDutyCycle(setting)

    SWPulseTimer5.begin(5, 1, #SW_PULSETIMER_mS,
                         False);
    SWPulseTimer19.begin(19, 1, #SW_PULSETIMER_mS, 
                         False);
    for setting in range(2000,65535,5000):
      SWPWM5.writeDutyCycle(setting);
      SWPWM19.writeDutyCycle(setting);

      delay(3200);

      pt5h = SWPulseTimer5.readHighCounts();
      pt19h = SWPulseTimer19.readHighCounts();
      pt19l = SWPulseTimer19.readLowCounts();
      pt5l = SWPulseTimer5.readLowCounts();
  
      expected = (1000 * setting) >> 16;
      SW18B_UnitTest_globals.test(f"Pulse Ph5ms: ",pt5h,expected,20,3)
      SW18B_UnitTest_globals.test(f"Pulse Ph19ms: ",pt19h,expected,20,3)

      measuredDuty5  = 0;
      if ((pt5h + pt5l) > 0):
        measuredDuty5 = pt5h * 65536 // (pt5h + pt5l)
        SW18B_UnitTest_globals.test(f"Pulse D5ms: ",measuredDuty5,expected,20,3)


      measuredDuty19  = 0;
      if ((pt19h + pt19l) > 0):
        measuredDuty19 = pt19h * 65536 // (pt19h + pt19l)
        SW18B_UnitTest_globals.test(f"Pulse Ph19ms: ",pt19h,expected,20,3)

    