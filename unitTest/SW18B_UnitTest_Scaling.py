import SW18B_UnitTest_globals
import SerialWombatServo
import SerialWombatAbstractScaledOutput
import time
from SW18B_UnitTest_globals import millis,delay

def scalingTest():
    SW18B_UnitTest_globals.resetAll()
    #TODO scalingTimeoutTest()
    #TODO scalingInputScalingTest()
    #TODO scalingInvertScalingTest()
    #TODO scalingOutputScalingTest()
    scalingRateControl16HzTest()
    scaling1stOrderTest()
    scalingHysteresisTest()

def scalingTimeoutTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)
    scalingOutput.writeScalingEnabled(False, 18);
    scalingOutput.writeScalingEnabled(False, 19);
    scalingOutput.writeScalingEnabled(True, 19);
    SW6B.writePublicData(19, 0x0000); 
    scalingOutput.writeTimeout(1000, 0x8000);
    startTime = millis()
    while (millis() < startTime + 900):
        if (scalingOutput.readLastOutputValue() == 0):
            SW18B_UnitTest_globals.testPassed(0);
        else:
            SW18B_UnitTest_globals.testFailed(0)
            print("Scaling Test Timeout Failed 0")
        delay(100)
    delay(200)
    v = scalingOutput.readLastOutputValue()
    x = 0x8000
    if ( v == x):
     SW18B_UnitTest_globals.testPassed(0)
    else:
        SW18B_UnitTest_globals.testFailed(0)
        print("Scaling Test Timeout Failed 0x8000")

def scalingInputScalingTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)

    lowLimit = 3000
    highLimit = 50000

    scalingOutput.writeScalingEnabled(False, 18)
    scalingOutput.writeScalingEnabled(True, 18)

    for i in range(0,65536, 10):
      SW6B.writePublicData(18, i)
      scalingOutput.writeInputScaling(lowLimit, highLimit)
      delay(10)
      expected = 0
      if (i > lowLimit):
        if (i > highLimit):
            expected = 65535
        else:
          expected = int( (((i - lowLimit) / (float)(highLimit - lowLimit)) * 65535)) & 0xFFFF;
      value = SW6B.readPublicData(19)

      if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 1)):
        SW18B_UnitTest_globals.testPassed(1)
      else:
        SW18B_UnitTest_globals.testFailed(1)
        print(f"F1. i: {i } V: {value} X: {expected}")

def scalingInvertScalingTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)

    lowLimit = 3000
    highLimit = 50000

    scalingOutput.writeScalingEnabled(False, 18)
    scalingOutput.writeScalingEnabled(True, 18)
    scalingOutput.writeScalingInvertedInput(True)

    for  i in range(0,  65536, 10):
        SW6B.writePublicData(18, i);
        scalingOutput.writeOutputScaling(lowLimit, highLimit);
        delay(10);
        expected = 0;
        expected = int( ((highLimit - lowLimit) * (float)(65535 - i) / 65535 + lowLimit)) & 0xFFFF

        value = SW6B.readPublicData(19)

        if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 1)):
            SW18B_UnitTest_globals.testPassed(1)
        else:
            SW18B_UnitTest_globals.testFailed(1);
            print(f"F1. i: {i } V: {value} X: {expected}")


def scalingOutputScalingTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)
    lowLimit = 3000
    highLimit = 50000
    scalingOutput.writeScalingEnabled(False, 18)
    scalingOutput.writeScalingEnabled(True, 18)

    for  i in range(0,  65536, 10):
        SW6B.writePublicData(18, i)
        scalingOutput.writeOutputScaling(lowLimit, highLimit)
        delay(10)
        expected = 0


        expected = int((highLimit - lowLimit) * i // 65535 + lowLimit) & 0xFFFF

        value = SW6B.readPublicData(19)

        if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 1)):
            SW18B_UnitTest_globals.testPassed(1)
        else:
            SW18B_UnitTest_globals.testFailed(1);
            print(f"F2. i: {i } V: {value} X: {expected}")

def scalingRateControl16HzTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)
    SW6B.writePublicData(19, 0)

    scalingOutput.writeScalingEnabled(False, 18)
   
    scalingOutput.writeRateControl(scalingOutput.PERIOD_64mS, 100)
    scalingOutput.writeScalingEnabled(True, 18)
    SW6B.writePublicData(18, 1000)
    while (SW6B.readPublicData(19) == 0):
       pass

    starttime = millis()
    for i in range(1,10):
        value = SW6B.readPublicData(19)
        expected = i * 100
        if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 0)):
                SW18B_UnitTest_globals.testPassed(1)
        else:
                SW18B_UnitTest_globals.testFailed(1)
                print(f"F8. i: {i } V: {value} X: {expected}")
        while ((millis() - starttime)< (64 * i)):
               pass

    starttime = millis()
    for i in range(1,10):
        value = SW6B.readPublicData(19)
        expected = 1000
        if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 0)):
                SW18B_UnitTest_globals.testPassed(1)
        else:
                SW18B_UnitTest_globals.testFailed(1)
                print(f"F9. i: {i } V: {value} X: {expected}")
        while ((millis() - starttime)< (64 * i)):
               pass
    

    SW6B.writePublicData(18, 500)
    expected = 1000;
    starttime = millis()
    for i in range(0,5):
        value = SW6B.readPublicData(19)

        if (SW18B_UnitTest_globals.withinRange(value, expected, 0, 0)):
                    SW18B_UnitTest_globals.testPassed(1)
        else:
                    SW18B_UnitTest_globals.testFailed(1)
                    print(f"F10. i: {i } V: {value} X: {expected}")
        expected -= 100
        while(millis() < starttime + ((i + 1) * 64)):
            pass
        

    for i in range(1,10):
        value = SW6B.readPublicData(19);

        if (SW18B_UnitTest_globals.withinRange(value, 500, 0, 0)):
                    SW18B_UnitTest_globals.testPassed(1)
        else:
                    SW18B_UnitTest_globals.testFailed(1)
                    print(f"F11. i: {i } V: {value} X: {expected}")
        delay(64)
def scaling1stOrderTest():
    #1stOrderFiltering, different pins
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)
    SW6B.writePublicData(19, 0)

    scalingOutput.writeScalingEnabled(False, 18);
    scalingOutput.write1stOrderFiltering(scalingOutput.PERIOD_8mS, 65000)
    scalingOutput.writeScalingEnabled(True, 18)
    SW6B.writePublicData(18, 10000)
    

    value = SW6B.readPublicData(19)
    startTime = millis()
    while (value < 9700):
      value = SW6B.readPublicData(19)
      delay(0)

    endTime = millis()
    elapsed = endTime - startTime; # Should take about 3400mS


    SW18B_UnitTest_globals.test("F12.  Critical! ",elapsed, 3400, 0, 200)

def scalingHysteresisTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW18B_UnitTest_globals.resetAll()
    scalingInput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingOutput = SerialWombatServo.SerialWombatServo_18AB(SW6B)
    scalingInput.attach(18)
    scalingOutput.attach(19)

    scalingOutput.writeScalingEnabled(False, 18)

    scalingOutput.writeScalingEnabled(False, 18)
    lowLimit = 0x5000
    highLimit = 0xA000
    lowValue = 500
    highValue = 1000
    startValue = 750
    midValue = lowLimit + (highLimit - lowLimit) // 2
   
    scalingInput.writePublicData(midValue)
    scalingOutput.writeScalingEnabled(True, 18)
    scalingOutput.writeHysteresis(lowLimit, lowValue, highLimit, highValue, startValue)

    SW18B_UnitTest_globals.test("SCALE_HYS_01", scalingOutput.readPublicData(), startValue)

    scalingInput.writePublicData(highLimit)
    SW18B_UnitTest_globals.test("SCALE_HYS_02", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(lowLimit)
    SW18B_UnitTest_globals.test("SCALE_HYS_03", scalingOutput.readPublicData(), lowValue)

    scalingInput.writePublicData(65535)
    SW18B_UnitTest_globals.test("SCALE_HYS_04", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(midValue)
    SW18B_UnitTest_globals.test("SCALE_HYS_05", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(0)
    SW18B_UnitTest_globals.test("SCALE_HYS_06", scalingOutput.readPublicData(), lowValue)

    scalingInput.writePublicData(midValue)
    SW18B_UnitTest_globals.test("SCALE_HYS_07", scalingOutput.readPublicData(), lowValue)