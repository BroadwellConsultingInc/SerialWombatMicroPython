import SW18B_UnitTest_globals

#TODO add random seed
def echoTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    for i in range(5000):
        tx = [ord('!'), 1,2,3,4,5,6,7]
        count,rx = SW6B.sendPacket(tx)
        passed = True
        if (rx[0] != ord('!')):
            passed = False
        for x in range(1,8):
            if (rx[x] != tx[x]):
                passed = False
        if (passed):
            SW18B_UnitTest_globals.testPassed(i)
        else:
            SW18B_UnitTest_globals.testFailed(i)

        
