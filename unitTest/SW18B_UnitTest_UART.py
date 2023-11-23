import SW18B_UnitTest_globals
import SerialWombatServo
import SerialWombat
import SerialWombatUART
from ArduinoFunctions import delay


def uartHWTest():
    SW18B_UnitTest_globals.resetAll()
    SW6B = SW18B_UnitTest_globals.SW6B
    SW6C = SW18B_UnitTest_globals.SW6C
    SW6E = SW18B_UnitTest_globals.SW6E
    
    sw18UART1 = SerialWombatUART.SerialWombatUART (SW6B)
    sw18UART2 = SerialWombatUART.SerialWombatUART (SW6B)
    UART1Match = SerialWombatUART.SerialWombatUART(SW6C)
    UART2Match = SerialWombatUART.SerialWombatUART(SW6E)
    uartRx = bytearray(200)
    uartTx = bytearray(200)
    txSeed = 1
    countSeed = 1

    baudArray = [ 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]


    SW6C.digitalWrite(1,1)
    SW6C.pinMode(1,1)
    SW6E.digitalWrite(1,1)
    SW6E.pinMode(1,1)




    for  baudIteration in range(9): 
        UART1Match.enable1ByteTransmissions(baudIteration == 8)
        UART2Match.enable1ByteTransmissions(baudIteration == 8)
        delayMs = 1000 * (8+1+1) / baudArray[baudIteration]
        if (baudIteration == 8):
            delayMs *= 4
        
        txcount = 0
        sw18UART1.begin(baudArray[baudIteration], 9, 9, 7)
        UART1Match.begin(baudArray[baudIteration], 0, 0, 1)

        sw18UART2.begin(baudArray[baudIteration], 19, 19, 17, 2)
        UART2Match.begin(baudArray[baudIteration], 3, 3, 1)
        sw18UART1.flush()
        sw18UART2.flush()
        UART1Match.flush()
        UART2Match.flush()
        for iteration in range(500):
            txcount, seed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount = txcount % 32
            for i in range(txcount):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx[i] = rval

           
            sw18UART1.write(uartTx, txcount)
            
            delay(delayMs * txcount)

            uartRx = UART1Match.readBytes( txcount)

            
            for i in range( txcount):
                    if (len(uartRx) < txcount):
                        print(f'F0 short packet: expected {txcount} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                        SW18B_UnitTest_globals.testFailed(1)
                    elif (uartTx[i] == uartRx[i]):
                        SW18B_UnitTest_globals.testPassed(1)
                    else:
                        print(f'F0 mismatch: expected {uartTx[i]} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                        SW18B_UnitTest_globals.test("F0", uartTx[i], uartRx[i],0,0)

            txcount,countSeed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount %= 32

            for i in range(txcount):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx[i] = rval
            UART1Match.write(uartTx, txcount)
            delay(delayMs * txcount)
            uartRx = sw18UART1.readBytes( txcount)
            for i in range(txcount):
                if (len(uartRx) < txcount):
                    print(f'F1 short packet: expected {txcount} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.testFailed(1)
                elif (uartTx[i] == uartRx[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F1 mismatch: expected {uartTx[i]} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F1", uartTx[i], uartRx[i],0,0)


            txcount, countSeed = SW18B_UnitTest_globals.wrandom(countSeed)
            txcount = txcount % 32;

            for i in range(txcount):
                rval,txSeed = SW18B_UnitTest_globals.wrandom(txSeed)
                uartTx[i] = rval
            sw18UART2.write(uartTx, txcount)
            delay(delayMs * txcount)
            uartRx = UART2Match.readBytes( txcount)
            for  i in range(txcount):
                if (len(uartRx) < txcount):
                    print(f'F2 short packet: expected {txcount} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.testFailed(1)
                elif (uartTx[i] == uartRx[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F2 mismatch: expected {uartTx[i]} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F2", uartTx[i], uartRx[i],0,0)

            txcount,countSeed = SW18B_UnitTest_globals.wrandom(countSeed) 
            txcount %= 32

            for  i in range(txcount):
                rval, txSeed = SW18B_UnitTest_globals.wrandom(txSeed) 
                uartTx[i] = rval

            UART2Match.write(uartTx, txcount)
           
            delay(delayMs * txcount)
            uartRx = sw18UART2.readBytes( txcount)
                   
            for i in range(txcount):
                if (len(uartRx) < txcount):
                    print(f'F3 short packet: expected {txcount} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.testFailed(1)
                elif (uartTx[i] == uartRx[i]):
                    SW18B_UnitTest_globals.testPassed(1)
                else:
                    print(f'F3 mismatch: expected {uartTx[i]} got {len(uartRx)} b: {baudIteration} iter: {iteration} i: {i} ')
                    SW18B_UnitTest_globals.test("F3", uartTx[i], uartRx[i],0,0)
                    """
                    print (txcount)
                    print(uartTx)
                    print()
                    print (len(uartRx))
                    print(uartRx)
                    print("------------------------------")
                    """
                   
    return (0)
