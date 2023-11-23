import SW18B_UnitTest_globals
import SerialWombatQuadEnc
import SerialWombatSimulatedQuadEnc
import time
from SW18B_UnitTest_globals import delay

from SW18B_UnitTest_globals import millis

def QuadEncTest():
    SW6B = SW18B_UnitTest_globals.SW6B
    SW6D = SW18B_UnitTest_globals.SW6D
    SW6E = SW18B_UnitTest_globals.SW6E
    qeSimA = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW6D, SW6D, 1, 2, True, False)
    qeSimB = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW6E, SW6E, 1, 2, True, False)
    qeA = SerialWombatQuadEnc.SerialWombatQuadEnc(SW6B)
    qeB = SerialWombatQuadEnc.SerialWombatQuadEnc(SW6B)
    SW18B_UnitTest_globals.resetAll()
    qeSimA.initialize()
    qeSimB.initialize()
    qeA.begin(5, 6,10,True)
    qeB.begin(18, 19,10,True)
 
    target = 30000

    qeA.write(target)
    qeSimA.targetPosition = qeSimA.currentPosition = target
  
    qeB.write(target)
    qeSimB.targetPosition = qeSimB.currentPosition = target

    for testIteration in range(20):
        qeSimA.targetPosition += testIteration
        qeSimB.targetPosition += testIteration


        while(qeSimB.targetPosition != qeSimB.currentPosition or qeSimA.targetPosition != qeSimA.currentPosition  ):  
            qeSimA.service()                     
            qeSimB.service()
            SW18B_UnitTest_globals.delay(1)

        SW18B_UnitTest_globals.delay(15)

        SW18B_UnitTest_globals.test("QEA_0", qeA.read() , (qeSimA.currentPosition & 0xFFFF),0);  
        """    
        if (qeA.read() == (qeSimA.currentPosition & 0xFFFF)):

            SW18B_UnitTest_globals.testPassed(0)
        else:

            SW18B_UnitTest_globals.testFailed(0)
            print(f"0: {qeA.read()} {qeSimA.currentPosition}")
        
        """        
        qeSimA.targetPosition -= 2*testIteration
        SW18B_UnitTest_globals.test("QEB_0", qeB.read() , (qeSimB.currentPosition & 0xFFFF),0);
        """
        if (qeB.read() == (qeSimB.currentPosition & 0xFFFF)):
        
            SW18B_UnitTest_globals.testPassed(1)
        else:
            SW18B_UnitTest_globals.testFailed(1)
            print(f"1: {qeB.read()} {qeSimB.currentPosition}")
        """
        qeSimB.targetPosition -= 2*testIteration
        
        while(qeSimB.targetPosition != (qeSimB.currentPosition & 0xFFFF) or qeSimA.targetPosition != (qeSimA.currentPosition & 0xFFFF) ):
            
            qeSimA.service()
            qeSimB.service()
            delay(1)
        delay(15)
        SW18B_UnitTest_globals.test("QEA_1", qeA.read() , (qeSimA.currentPosition & 0xFFFF),0);
        SW18B_UnitTest_globals.test("QEB_1", qeB.read() , (qeSimB.currentPosition & 0xFFFF),0);
        """
        if (qeA.read() == (qeSimA.currentPosition & 0xFFFF)):
            SW18B_UnitTest_globals.testPassed(2)
        else:
            SW18B_UnitTest_globals.testFailed(2)
            print(f"2: {qeA.read()} {qeSimA.currentPosition}")
        if (qeB.read() == (qeSimB.currentPosition & 0xFFFF)):
             SW18B_UnitTest_globals.testPassed(3)
        else:
            SW18B_UnitTest_globals.testFailed(3)
            print(f"3: {qeB.read()} {qeSimB.currentPosition}")
        """