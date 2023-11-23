import machine
import SerialWombat_mp_i2c
import SerialWombatPulseTimer
import time

global SW18B_0_MATCH_PIN
SW18B_0_MATCH_PIN = 3

global SW18B_1_MATCH_PIN
SW18B_1_MATCH_PIN = 0# 1

global SW18B_2_MATCH_PIN
SW18B_2_MATCH_PIN = 0#2

global SW18B_3_MATCH_PIN
SW18B_3_MATCH_PIN = 0 #3

global SW18B_4_MATCH_PIN
SW18B_4_MATCH_PIN = 0 #4

global SW18B_5_MATCH_PIN
SW18B_5_MATCH_PIN = 2#5

global SW18B_6_MATCH_PIN
SW18B_6_MATCH_PIN = 1#6

global SW18B_7_MATCH_PIN
SW18B_7_MATCH_PIN = 0#7

global SW18B_8_MATCH_PIN
SW18B_8_MATCH_PIN = 0#8

global SW18B_9_MATCH_PIN
SW18B_9_MATCH_PIN = 1#9

global SW18B_10_MATCH_PIN
SW18B_10_MATCH_PIN = 2#10

global SW18B_11_MATCH_PIN
SW18B_11_MATCH_PIN = 3#11

global SW18B_12_MATCH_PIN
SW18B_12_MATCH_PIN = 0#12

global SW18B_13_MATCH_PIN
SW18B_13_MATCH_PIN = 0#13

global SW18B_14_MATCH_PIN
SW18B_14_MATCH_PIN = 3#14

global SW18B_15_MATCH_PIN
SW18B_15_MATCH_PIN = 2#15

global SW18B_16_MATCH_PIN
SW18B_16_MATCH_PIN = 1#16

global SW18B_17_MATCH_PIN
SW18B_17_MATCH_PIN = 3#17

global SW18B_18_MATCH_PIN
SW18B_18_MATCH_PIN = 2#18

global SW18B_19_MATCH_PIN
SW18B_19_MATCH_PIN = 1#19

global i2c
i2c = None

global SWMatchPin
SWMatchPin = [ SW18B_0_MATCH_PIN ,#0
  SW18B_1_MATCH_PIN ,# 1
  SW18B_2_MATCH_PIN ,#2
  SW18B_3_MATCH_PIN , #3
  SW18B_4_MATCH_PIN , #4
  SW18B_5_MATCH_PIN ,#5
  SW18B_6_MATCH_PIN ,#6
  SW18B_7_MATCH_PIN ,#7
  SW18B_8_MATCH_PIN ,#8
  SW18B_9_MATCH_PIN ,#9
  SW18B_10_MATCH_PIN,#10
  SW18B_11_MATCH_PIN,#11
  SW18B_12_MATCH_PIN,#12
  SW18B_13_MATCH_PIN,#13
  SW18B_14_MATCH_PIN,#14
  SW18B_15_MATCH_PIN,#15
  SW18B_16_MATCH_PIN,#16
  SW18B_17_MATCH_PIN,#17
  SW18B_18_MATCH_PIN,#18
  SW18B_19_MATCH_PIN ]#19

def init():
    global i2c
    i2c = machine.I2C(0,
                  scl=machine.Pin(1),
                  sda=machine.Pin(0),
                  freq=100000,timeout = 50000)

    global NUM_TEST_PINS
    NUM_TEST_PINS = 20

    global SW6B 
    SW6B = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6B)
    SW6B.address = 0x6B

    global SW6C
    SW6C = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6C)
    SW6C.address = 0x6C

    global SW6D
    SW6D = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6D)
    SW6D.address = 0x6D
    
    global SW6E
    SW6E = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6E)
    SW6E.address = 0x6E

    global SW6F
    SW6F = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,0x6F)
    SW6F.address = 0x6F

    global SWMatch
    SWMatch = [ SW6D,#0
        None,# 1
        None,#2
        None, #3
        None, #4
        SW6D,#5
        SW6D,#6
        SW6C,#7
        SW6D,#8
        SW6C,#9
        SW6C,#10
        SW6C,#11
        SW6E,#12
        SW6F,#13
        SW6F,#14
        SW6F,#15
        SW6F,#16
        SW6E,#17
        SW6E,#18
        SW6E ]#19
    global passCount
    passCount = 0

    global failCount
    failCount = 0

    global lastPassedTest
    lastPassedTest = -1


    SWPT00 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6D)
    SWPT05 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6D)
    SWPT06 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6D)
    SWPT07 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6C)
    SWPT08 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6D)
    SWPT09 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6C)
    SWPT10 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6C)
    SWPT11 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6C)
    SWPT12 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6E)
    SWPT13 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6F)
    SWPT14 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6F)
    SWPT15 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6F)
    SWPT16 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6F)
    SWPT17 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6E)
    SWPT18 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6E)
    SWPT19 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW6E)

    global PulseTimerArray
    PulseTimerArray = [SWPT00, None,None,None,None,
                       SWPT05,
                       SWPT06,
                       SWPT07,
                       SWPT08,
                       SWPT09,
                       SWPT10,
                       SWPT11,
                       SWPT12,
                       SWPT13,
                       SWPT14,
                       SWPT15,
                       SWPT16,
                       SWPT17,
                       SWPT18,
                       SWPT19
                       ]

    global initializePulseReaduS
    def initializePulseReaduS(pin):
        if (pin < NUM_TEST_PINS):
            if (PulseTimerArray[pin] != None):
                PulseTimerArray[pin].begin(SWMatchPin[pin])
            else:
                print("TEST ERROR: NULL PIN in initializePulseReaduS")
        else:
            print("TEST ERROR: INVALID PIN in initializePulseReaduS")

    global testPassed
    def testPassed(i):
        global passCount
        passCount += 1
        lastPassedTest = i

    global lastFailedTest
    lastFailedTest = -1

    global testFailed
    def testFailed(i):
        global lastFailedTest
        lastFailedTest = i
        global failCount
        failCount += 1

def resetAll():
    SW6B.begin()
    while (not SW6B.queryVersion):
        pass
    SW6C.begin()
    disablePPS(SW6C)
    while (not SW6C.queryVersion):
        pass
    SW6D.begin()
    disablePPS(SW6C)
    while (not SW6D.queryVersion):
        pass
    SW6E.begin()
    disablePPS(SW6C)
    while (not SW6E.queryVersion):
        pass
    SW6F.begin()
    disablePPS(SW6C)
    while (not SW6F.queryVersion):
        pass


def disablePPS(sw):
    b = [219, 1, 16, 0x55, 0x55, 0x55, 0x55, 0x55]
    sw.sendPacket(b)
    b[1] = 2
    sw.sendPacket(b)
    b[1] = 3
    sw.sendPacket(b)

    sw.pinMode(1, 0) #INPUT
    sw.pinMode(2,  0)
    sw.pinMode(3,  0)

def pulseRead(pin):
    if (pin < NUM_TEST_PINS):
        if (PulseTimerArray[pin] != None):
            return PulseTimerArray[pin].readHighCounts()
        else:
            print("TEST ERROR: NULL PIN in initializePulseReaduS")
            return 0
    else:
        print("TEST ERROR: INVALID PIN in initializePulseReaduS")
        return 0

def pulseCounts(pin):
    if (pin < NUM_TEST_PINS):
        if (PulseTimerArray[pin] != None):
            return PulseTimerArray[pin].readPulses()
        else:
            Serial.println("TEST ERROR:  NULL PIN in pulseCounts");
            return (0);
    else:
        print("TEST ERROR:  INVALID PIN in pulseCounts");
    return 0

def withinRange( value,  expected,  sixtyFourths,  counts):
    x32 = expected
    if ((value > x32 + counts) and (value > (x32 * (64 + sixtyFourths)) // 64)):
        return (False)

    if ((value < x32 - counts) and (value < (x32 * (64 - sixtyFourths)) // 64)):
        return (False)
    return (True)

def test( designator,  value,  expected = 1,  counts = 0,  sixtyFourths = 0):

  if (withinRange(value, expected, sixtyFourths, counts)):
  
    testPassed(1)
    #print(f"{designator} P V:{value} X: {expected}  Passes: {passCount} Fails:{failCount}")
    #SW6B.sendPacket(bytearray([0x40,0,expected & 0xFF, expected //256, value&0xFF,value//256,0x55,0x55]))

  else:
  
    testFailed(1)
    print(f"{designator} F V:{value} X: {expected}  Passes: {passCount} Fails:{failCount}")
    SW6B.sendPacket(bytearray([0x40,0,expected & 0xFF, expected //256, value&0xFF,value//256,0x55,0x55]))

def testGEZ( designator,  value):

  if (value >= 0):
  
    testPassed(1)
    #print(f"{designator} P V:{value} X: {expected}  Passes: {passCount} Fails:{failCount}")
    #SW6B.sendPacket(bytearray([0x40,0,expected & 0xFF, expected //256, value&0xFF,value//256,0x55,0x55]))

  else:
  
    testFailed(1)
    print(f"{designator} F V:{value} X: >0  Passes: {passCount} Fails:{failCount}")
    SW6B.sendPacket(bytearray([0x40,0,0, 0 , value&0xFF,value//256,0x55,0x55]))

def test_pinCanBeOutput(pin):
  if (pin < NUM_TEST_PINS):
    return (SWMatch[pin] != None)
  return (False)

millisStart = time.ticks_ms()
def millis():
    return(int((time.ticks_ms() - millisStart)))

def delay(delayMs):
    startTime = millis()
    while (millis() < startTime + delayMs):
        continue

def wrandom(seed):
  #32,7,5,3,2,1
  MASK =  0x80000057
  output = 0
  for i in range(16):
    if ((seed & 0x00000001) > 0):
      seed = (((seed ^ MASK) >> 1) | 0x80000000);
    else:
      seed >>= 1
    output <<= 1
    output |= seed & 0x01
  
  return ((output,seed))