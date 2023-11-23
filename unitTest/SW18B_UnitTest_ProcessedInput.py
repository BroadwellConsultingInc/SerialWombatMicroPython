import SW18B_UnitTest_globals
import SerialWombatAbstractProcessedInput
import SerialWombatProcessedInputPin
import SerialWombatServo
import SerialWombat
from ArduinoFunctions import delay

IP_IN_PIN  = 18
IP_OUT_PIN  = 19
ipInput = SerialWombatServo.SerialWombatServo_18AB (SW18B_UnitTest_globals.SW6B)
processedInput = SerialWombatProcessedInputPin.SerialWombatProcessedInputPin(SW18B_UnitTest_globals.SW6B)

def inputProcessorTest():

  ipDisabledTest()
  ipExclusionTest()
  ipAverageTest()
  ipMxbTest()

def ipDisabledTest():
    SW18B_UnitTest_globals.resetAll()
    ipInput.attach(IP_IN_PIN)
    processedInput.begin(IP_OUT_PIN,IP_IN_PIN)

    for i in range(0, 65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_DIS_01", result, i)
        delay(0)

    processedInput.writeInverted(True)
    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_DIS_02", result, i)
        delay(0)
    processedInput.writeProcessedInputEnable(True)

    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_INV_01", result, 65535 - i)
        delay(0)

    processedInput.writeInverted(False)
    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_INV_02", result, i)
        delay(0)

def ipExclusionTest():
    SW18B_UnitTest_globals.resetAll()
    ipInput.attach(IP_IN_PIN)
    processedInput.begin(IP_OUT_PIN,IP_IN_PIN)
    processedInput.writeProcessedInputEnable(True)
    ipInput.writePublicData(12500)
    processedInput.writeExcludeBelowAbove(20000,40000)
   
    for i in range (0,19999,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_EX_01", result, 12500)
        delay(0)

    for i in range (20000,40001,13):
        ipInput.writePublicData(i)
        lastVal = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_EX_02", lastVal, i)
        delay(0)

    for i in range (40001,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        SW18B_UnitTest_globals.test("IP_EX_03", result, lastVal)
        delay(0)

def ipAverageTest():

    SW18B_UnitTest_globals.resetAll()

    processedInput.begin(IP_OUT_PIN,78)#SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_LFSR)


    processedInput.writeAveragingNumberOfSamples(4000)

    processedInput.writeProcessedInputEnable(True)

    delay(5000)

    result = processedInput.readAverage()
    SW18B_UnitTest_globals.test("IP_AVG_01", result, 32768, 500);  # Random should average out to 32768, will allow +/- 500

    processedInput.writeExcludeBelowAbove(40000,60000)

    delay(30000)


    result = processedInput.readAverage()
    SW18B_UnitTest_globals.test("IP_AVG_01", result, 50000, 500);  # Random should average out to 50000, will allow +/- 500

def ipMxbTest():
    SW18B_UnitTest_globals.resetAll()
    ipInput.attach(IP_IN_PIN)
    processedInput.begin(IP_OUT_PIN,IP_IN_PIN)
    processedInput.writeProcessedInputEnable(True)

    processedInput.writeTransformLinearMXB(5 * 256,32)
   
    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        expected = i * 5  + 32
        if (expected > 65535):
            expected = 65535
        SW18B_UnitTest_globals.test("IP_MXB_01", result, expected)
        delay(0)
  
    processedInput.writeTransformLinearMXB(5 * 256,-20000)
   
    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        expected = i * 5 - 20000
        if (expected > 65535):
            expected = 65535
        if (expected < 0):
            expected = 0
    
        SW18B_UnitTest_globals.test("IP_MXB_02", result, expected)
        delay(0)

    processedInput.writeTransformLinearMXB(-5 * 256,100000)
   
    for i in range (0,65536,13):
        ipInput.writePublicData(i)
        result = processedInput.readPublicData()
        expected = i * -5  + 100000
        if (expected > 65535):
            expected = 65535
        if (expected < 0):
            expected = 0
    
        SW18B_UnitTest_globals.test("IP_MXB_03", result, expected)
        delay(0)
