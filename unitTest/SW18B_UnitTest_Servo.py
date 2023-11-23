import SW18B_UnitTest_globals
import SerialWombatServo
import time

SERVO_DEFAULT_BASE = 544
SERVO_DEFAULT_VARIABLE = 1856
SERVO_TEST_INCREMENTS = 100
def servoTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SWServo0 = SerialWombatServo.SerialWombatServo(SW6B)
    
    SW18B_UnitTest_globals.resetAll()

    for pin in range(SW18B_UnitTest_globals.NUM_TEST_PINS):
        # TODO initialize pulse and check if test pin
        if (SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
            SW18B_UnitTest_globals.initializePulseReaduS(pin)

    for variable in range(800,2100,100):
        print(f"Servo test {variable} of 2100, Pass: {SW18B_UnitTest_globals.passCount}  fail: {SW18B_UnitTest_globals.failCount}")
        for base in range(500,1300,100):
            print(f"    Servo test {base} of 1300, Pass: {SW18B_UnitTest_globals.passCount}  fail: {SW18B_UnitTest_globals.failCount}")
            for reverse in range(2):
                for i in range(SERVO_TEST_INCREMENTS):
                    for pin in range(SW18B_UnitTest_globals.NUM_TEST_PINS):
                        if (SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
                            SWServo0.attach(pin,base,base + variable, reverse)
                            position = (i * 65535) // SERVO_TEST_INCREMENTS + (pin * 65535 // SW18B_UnitTest_globals.NUM_TEST_PINS)
                            position = position & 0xFFFF
                            SWServo0.write16bit(position)
                    time.sleep(0.020)
                    for pin in range(SW18B_UnitTest_globals.NUM_TEST_PINS):
                        if (SW18B_UnitTest_globals.test_pinCanBeOutput(pin)):
                            result = SW18B_UnitTest_globals.pulseRead(pin)
                            setting = (i * 65535) // SERVO_TEST_INCREMENTS + (pin * 65535 // SW18B_UnitTest_globals.NUM_TEST_PINS)
                            setting &= 0xFFFF
                            if (reverse):
                                setting = 65535 - setting
                            expected = variable * setting // 65536 + base
                            SW18B_UnitTest_globals.test(f"Servo pin: {pin} var:{variable} base: {base} reverse:{reverse} i: {i}",result,expected,20,4)
            






        
