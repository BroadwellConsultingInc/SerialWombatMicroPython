import SW18B_UnitTest_globals


def CommunicationErrorTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    priorErrorCount = SW6B.errorCount
    tx = [200, 63, 1, 0x55, 0x55, 0x55, 0x55, 0x55]
    SW6B.sendPacket(tx)
    if (SW6B.errorCount != priorErrorCount + 1):
        SW18B_UnitTest_globals.testFailed(1)
        print ("CommunicationErrorTest failed.")
    else:
        SW18B_UnitTest_globals.testPassed(1)
