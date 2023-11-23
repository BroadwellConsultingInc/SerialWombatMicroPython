import SW18B_UnitTest_globals
import SerialWombatServo
import SerialWombat
import SerialWombatUART
from ArduinoFunctions import delay


def uartSWTest():
    SW18B_UnitTest_globals.resetAll()
    SW6B = SW18B_UnitTest_globals.SW6B
    SW6D = SW18B_UnitTest_globals.SW6D
    SW6E = SW18B_UnitTest_globals.SW6E
 
 
    SW6D.digitalWrite(2,1)
    SW6D.pinMode(2,1)
    SW6E.digitalWrite(3,1)
    SW6E.pinMode(3,1)

    sw18UART1 = SerialWombatUART.SerialWombatSWUART (SW6B)
    sw18UART2 = SerialWombatUART.SerialWombatSWUART (SW6B)
    UART1Match = SerialWombatUART.SerialWombatUART(SW6D)
    UART2Match = SerialWombatUART.SerialWombatUART(SW6E)
    uartTx = bytearray(200) #TODO remove
    txSeed = 1
    countSeed = 1

    baudArray = [ 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]






    for  baudIteration in range(6): 
        delayMs = 1000 * (8+1+1) / baudArray[baudIteration]
        if (baudIteration == 8):
            delayMs *= 4
        
        result = sw18UART1.begin(baudArray[baudIteration], 5, 5, 6, 0 , 32, 32)
        SW18B_UnitTest_globals.testGEZ("B0",result)
        
        result = UART1Match.begin(baudArray[baudIteration], 1, 1, 2)
        SW18B_UnitTest_globals.testGEZ("B1",result)

        result = UART2Match.begin(baudArray[baudIteration], 3, 3, 1)
        SW18B_UnitTest_globals.testGEZ("B3",result)        

        result = sw18UART2.begin(baudArray[baudIteration], 19, 19, 17, 0x100,32,32)
        SW18B_UnitTest_globals.testGEZ("B2",result)

        sw18UART1.flush()
        sw18UART2.flush()
        UART1Match.flush()
        UART2Match.flush()
        
        uartRxb = sw18UART2.readBytes( 1)
        SW18B_UnitTest_globals.test("F3 PreCheck Len", len(uartRxb),0,0,0)

        for iteration in range(500):
            uartTx0 = bytearray()
            uartTx1 = bytearray()
            uartTx2 = bytearray()
            uartTx3 = bytearray()
            

            txcount0, seed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount0 = txcount0 % 32
            for i in range(txcount0):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx0.append(rval)

           
            sw18UART1.write(uartTx0, txcount0)
            
           

            txcount1,countSeed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount1 %= 32

            for i in range(txcount1):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx1.append(rval)
            UART1Match.write(uartTx1, txcount1)
            
            txcount2, countSeed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount2 = txcount2 % 32;
            for i in range(txcount2):
                rval,txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx2.append(rval)
            sw18UART2.write(uartTx2, txcount2)

            txcount3,countSeed = SW18B_UnitTest_globals.wrandom(countSeed) 
            txcount3 %= 32

            for  i in range(txcount3):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed) 
                uartTx3.append(rval)

            UART2Match.write(uartTx3, txcount3)

            
            delaymax = txcount0
            if (txcount1 > delaymax):
                delaymax = txcount1
            if (txcount2 > delaymax):
                delaymax = txcount2
            if (txcount3 > delaymax):
                delaymax = txcount3                
            delay(delayMs * delaymax)

            uartRx0 = UART1Match.readBytes( txcount0)

            
            for i in range( txcount0):
                    if (len(uartRx0) < txcount0):
                        print(f'F0 short packet: expected {txcount0} got {len(uartRx0)} b: {baudIteration} iter: {iteration} i: {i} ')
                        SW18B_UnitTest_globals.testFailed(1)
                    elif (uartTx0[i] == uartRx0[i]):
                        SW18B_UnitTest_globals.testPassed(1)
                    else:
                        print(f'F0 mismatch: expected {uartTx0[i]} got {len(uartRx0)} b: {baudIteration} iter: {iteration} i: {i} ')
                        SW18B_UnitTest_globals.test("F0", uartTx0[i], uartRx0[i],0,0)
           
            uartRx1 = sw18UART1.readBytes( txcount1)
            for i in range(txcount1):
                if (len(uartRx1) < txcount1):
                    print(f'F1 short packet: expected {txcount1} got {len(uartRx1)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.testFailed(1)
                elif (uartTx1[i] == uartRx1[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F1 mismatch: expected {uartTx1[i]} got {uartRx1[i]} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F1", uartTx1[i], uartRx1[i],0,0)
            
            uartRx2 = UART2Match.readBytes( txcount2)
            for  i in range(txcount2):
                if (len(uartRx2) < txcount2):
                    print(f'F2 short packet: expected {txcount2} got {len(uartRx2)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.testFailed(1)
                elif (uartTx2[i] == uartRx2[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F2 mismatch: expected {uartTx2[i]} got {uartRx2[i]} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F2", uartTx[i], uartRx2[i],0,0)

           
            uartRx3 = sw18UART2.readBytes( txcount3)
                   
            for i in range(txcount3):
                if (len(uartRx3) < txcount3):
                    print(f'F3 Short: expected {txcount3} got {len(uartRx3)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F3 Short", txcount3,len(uartRx3),0,0)
                elif (uartTx3[i] == uartRx3[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F3 mismatch: expected {uartTx3[i]} got {uartRx3[i]} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F3",  uartRx3[i],uartTx3[i], 0,0)
                    """
                    print (txcount)
                    print(uartTx)
                    print()
                    print (len(uartRx))
                    print(uartRx)
                    print("------------------------------")
                    """
                   
    return (0)
