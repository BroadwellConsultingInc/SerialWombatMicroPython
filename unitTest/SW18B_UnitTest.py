import time
#import datetime
import sys

#sys.path.append(r'..')
import SW18B_UnitTest_globals
from ArduinoFunctions import delay
from ArduinoFunctions import millis

SW18B_UnitTest_globals.init()

SW6B = SW18B_UnitTest_globals.SW6B
SW6C = SW18B_UnitTest_globals.SW6C
SW6D = SW18B_UnitTest_globals.SW6D
SW6E = SW18B_UnitTest_globals.SW6E
SW6F = SW18B_UnitTest_globals.SW6F

print()
print("#############################################################")
print()
print("Serial Wombat 18B Unit Test")
print()
print("#############################################################")
print()

lastPassedTest = -1
SW18B_UnitTest_globals.resetAll()
SW6B.readVersion()
print(f"SW18AB Version: {SW6B.fwVersion}")


def testPassed(i):
    passCount += 1
    lastPassedTest = i

lastFailedTest = -1

def testFailed(i):
    lastFailedTest = i
    failCount += 1

import SW18B_UnitTest_Analog
import SW18B_UnitTest_Servo
import SW18B_UnitTest_Scaling
import SW18B_UnitTest_Debounce
import SW18B_UnitTest_HSClock
import SW18B_UnitTest_HSCounter
import SW18B_UnitTest_EchoTest
import SW18B_UnitTest_PWM
import SW18B_UnitTest_ProcessedInput
import SW18B_UnitTest_PulseOnChange
import SW18B_UnitTest_PulseTimer
import SW18B_UnitTest_UART
import SW18B_UnitTest_UART_SW
"""
import SW18B_UnitTest_CommunicationError





"""
import SW18B_UnitTest_FrameTimer
import SW18B_UnitTest_QuadEnc

def currentTimeString():
    return  f" timestamp {millis()//1000} "
def loop():
     
    print(f"Starting Analog Input Test at {currentTimeString()}")
    SW18B_UnitTest_Analog.analogInputTest()
    print(f"Analog Input Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting Resistance Input Test at {currentTimeString()}")
    SW18B_UnitTest_Analog.resistanceInputTest()
    print(f"Resistance Input Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
 
    print(f"Starting Pulse Timer Test at {currentTimeString()}")
    SW18B_UnitTest_PulseTimer.pulseTimerTest()
    print(f"PulseTimer Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    

    print(f"Starting SW UART Test at {currentTimeString()}")
    SW18B_UnitTest_UART_SW.uartSWTest()
    print(f"SW UART Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
   
    print(f"Starting HW UART Test at {currentTimeString()}")
    SW18B_UnitTest_UART.uartHWTest()
    print(f"HW UART Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    print(f"Starting PulseOnChange Test at {currentTimeString()}")
    SW18B_UnitTest_PulseOnChange.pulseOnChangeTest18AB()
    print(f"PulseOnChange Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    delay(20000)
    
    print(f"Starting ProcessedInput Test at {currentTimeString()}")
    SW18B_UnitTest_ProcessedInput.inputProcessorTest()
    print(f"ProcessedInput Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting PWM Test at {currentTimeString()}")
    SW18B_UnitTest_globals.resetAll()
    SW18B_UnitTest_PWM.pwmTest()
    print(f"PWM Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print("Starting ECHO Test.  This test takes about 2 minutes")
    SW18B_UnitTest_EchoTest.echoTest()
    print(f"Echo test complete.  Pass: {SW18B_UnitTest_globals.passCount}  Fail {SW18B_UnitTest_globals.failCount}")
 
    print(f"Starting HSClock Test at {currentTimeString()}")
    SW18B_UnitTest_HSClock.hsClockTest()
    print(f"HSClock Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting HSCounter Test at {currentTimeString()}")
    SW18B_UnitTest_HSCounter.hsCounterTest()
    print(f"HSCounter Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting Debounce Test at {currentTimeString()}")
    SW18B_UnitTest_Debounce.debounceTest()
    print(f"Debounce Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")


    print(f"Starting OutputScaling Test at {currentTimeString()}")
    SW18B_UnitTest_Scaling.scalingTest()
    print(f"OutputScaling Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting Servo Test at {currentTimeString()}")
    SW18B_UnitTest_globals.resetAll()
    SW18B_UnitTest_Servo.servoTest()
    print(f"Servo Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")


    print(f"Starting Frametimer Test at {currentTimeString()}")
    SW18B_UnitTest_FrameTimer.frameTimerTest()
    print(f"Frametimer Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

   
    print(f"Starting QuadEnc Test at {currentTimeString()}")
    SW18B_UnitTest_QuadEnc.QuadEncTest()
    print(f"QuadEnc Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    """

    SW18B_UnitTest_globals.resetAll()
    print("Starting communication error test.  This test takes less than a minute")
    SW18B_UnitTest_CommunicationError.CommunicationErrorTest()
    """

while (True):
    loop()
