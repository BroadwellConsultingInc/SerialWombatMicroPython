#pragma once
#include "Stream.h"
#include "SerialWombat.h"


"""! \file SerialWombatUART.h
"""

"""
Copyright 2020-2021 Broadwell Consulting Inc.

"Serial Wombat" is a registered trademark of Broadwell Consulting Inc. in
the United States.  See SerialWombat.com for usage guidance.

Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
"""

import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE16
from ArduinoFunctions import millis
import SerialWombatQueue

"""! @brief A class for the Serial Wombat 4B or SW18AB chips which creates an I2C to UART Bridge

This class allows use of the Serial Wombat 4B chips's internal UART hardware to send
and receive data at standard baud rates in 8-N-1 format.

A Tutorial video is avaialble:

@htmlonly
<iframe width="560" height="315" src="https://www.youtube.com/embed/C1FjcaiBYZs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
@endhtmlonly

https://youtu.be/C1FjcaiBYZs


The class inherits from the Arduino Sream class, so functions such as println()
can be used once the UART is initialized.

The Serial Wombat 4B chip has a 64 byte transmit buffer and 128 byte receive buffer.
Therefore, up to 64 bytes can be sent to the SerialWombatUART at a time.
Attempts to send more than that will result in the write, print, etc command
blocking until space is available on the SerialWombatUART to buffer the data.

Received data is buffered on the Serial Wombat chip until it is retreived from the
host.  

\warning Due to the overhead of querying and retreiving data from the SerialWombatUART,
data loss is likely when receiving streams of data greater than the buffer size at higher
baud rates.

To minimize this possiblity, read data frequently from the Serial Wombat chip, and set I2C frequency
to 400kHz to maximize throughput (SW4B only) .

This class can Send, Receive, or both.  A single instance of this class is allowed per Serial Wombat 4B chip
due to the fact that it relies on the PIC16F15214's UART module, of which there is only one on the micro.

Two instances of this class can be used on the Serial Wombat 18AB chip by using the begin() call
which takes a hardware indicator of 0 or 1.

A full Serial Wombat packet send / receive sequence (8 bytes in each direction) over I2C is necessary to
query the status of the queues or to read or receive a byte of data.  

The protocol becomes more efficient if multiple bytes are read or written using the readBytes or 
write(const * buffer, size_t size) interfaces rather than read() or write( data).

The class must be assigned to a pin.  This may be either the receive or transmit pin.

Pin 0 on the Serial Wombat 4B is suggested as a receive pin as it has only input capability.

Serial Wombat 18AB pins must be enhanced digital performance pins.

Available baud rates are:
 - 300  
 - 1200 
 - 2400  
 - 4800  
 - 9600  
 - 19200 
 - 38400  
 - 57600  
 - 115200
"""

class SerialWombatUART (SerialWombatPin):
        """!
        @brief Constructor for the SerialWombatUART class.  Only one instance is allowed per SerialWombatChip 4B.
        @param serialWombat The Serial Wombat chip on which the SerialWombatUART instance will run.
        """
        def  __init__(self,serial_wombat):
                self._sw = serial_wombat
                self._rxPin  = 255
                self._txPin = 255
                self._baudMarker = 0
                self.timeout = 5000
                self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_UART_RX_TX
                self._tx7Command = SerialWombat.SerialWombatCommands.COMMAND_UART0_TX_7BYTES
                self._rx7Command = SerialWombat.SerialWombatCommands.COMMAND_UART0_RX_7BYTES
                self._1ByteTransmissions = False

        """!
        @brief Initalize the SerialWombatUART.  
        @param baudRate  300, 1200, 2400, 4800, 9600,  19200,  38400,  57600,  115200
        @param pin  The pin that will host the state machine.  This can be either the rxPin or txPin
        @param rxPin The pin that will receive.  All 4 pins on the SW4B may be used.  255 if no receive function is needed
        @param txPin The pin that will transmit.  Valid values for the SW4B are 1-3.  255 if no transmit function is needed
        @param HWinterface  1 or 2 for HW UART 1 or 2
        """
        def begin(self, baudRate,  pin,  rxPin,  txPin, HWinterface = 1 ):
                self._rxPin = rxPin
                self._txPin = txPin
                self._pin = pin
                if (HWinterface == 2):
                    self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_UART1_RX_TX
                    self._tx7Command =SerialWombat.SerialWombatCommands.COMMAND_UART1_TX_7BYTES
                    self._rx7Command = SerialWombat.SerialWombatCommands.COMMAND_UART1_RX_7BYTES

                elif (HWinterface == 1):
                    self._pinMode = 17 # PIN_MODE_UART_RX_TX
                    self._tx7Command = SerialWombat.SerialWombatCommands.COMMAND_UART0_TX_7BYTES
                    self._rx7Command = SerialWombat.SerialWombatCommands.COMMAND_UART0_RX_7BYTES
                else:
                    return (-1)
             
                if (baudRate == 300):
                     self._baudMarker = 0
                elif (baudRate == 1200):
                     self._baudMarker = 1
                elif (baudRate == 2400):
                     self._baudMarker = 2
                elif (baudRate == 4800):
                     self._baudMarker = 3
                elif (baudRate == 9600):
                     self._baudMarker = 4
                elif (baudRate == 19200):
                     self._baudMarker = 5
                elif (baudRate == 38400):
                     self._baudMarker = 6
                elif (baudRate == 57600):
                     self._baudMarker = 7
                else:
                     self._baudMarker = 8
                tx = [ 200, self._pin,self._pinMode, self._baudMarker,self._rxPin,self._txPin,0x55, 0x55 ]
                result,rx = self._sw.sendPacket(tx);
                return result

        """!
        @brief Queries the SerialWombatUART for number bytes available to read
        @return Number of bytes available to read.
        """
        def available(self):
                tx = [ 201, self._pin,self._pinMode, 0,0x55,0x55,0x55,0x55 ]
                result,rx = self._sw.sendPacket(tx)
                return (rx[4])
        """!
        @brief Reads a byte from the SerialWombatUART
        @return A byte from 0-255, or -1 if no bytes were avaialble
        """
        def read(self):
                tx = [ 202, self._pin,self._pinMode, 1,0x55,0x55,0x55,0x55 ]
                result,rx = self._sw.sendPacket(tx)
                if (result < 0):
                        return -1
                if (rx[3] != 0):
                       return (rx[4])
                else:
                        return (-1)

        """!
        @brief  Discard all received bytes
        """
        def flush(self):
                tx = [ 200, self._pin,self._pinMode, self._baudMarker,self._rxPin,self._txPin,0x55, 0x55 ]
                self._sw.sendPacket(tx)
        """!
        @brief Query the SerialWombatUART for the next avaialble byte, but don't remove it from the queue
        @return A byte from 0-255, or -1 if no bytes were avaialble
        """
        def peek(self):
                tx = [ 203, self._pin,self._pinMode,0x55,0x55,0x55,0x55,0x55 ]
                result, rx = self._sw.sendPacket(tx)
                if (result < 0):
                       return (-1)
                if (rx[4] > 0):
                       return (rx[5])
                else:
                      return (-1)
        """!
        @brief Write a byte to the SerialWombatUART for Transmit
        @param data  Byte to write
        @return Number of bytes written

        This does not check to see if space is avaialble in order to improve perfomance
        .  This isn't an issue at high baud rates, as
        overhead to transmit one byte at a time allows sufficent time for queuing data to be sent
        by the UART.  This could
        be a problem at very low baud rates and high I2C bus speeds.
        """
        def writebyte(self, data):
                tx = [ 201, self._pin,self._pinMode,1,data,0x55,0x55,0x55 ]
                self._sw.sendPacket(tx)
                return (1)

        """!
        @brief Write bytes to the SerialWombatUART for Transmit
        @param buf  An array of  bytes to send
        @param size the number of bytes to send
        @return the number of bytes sent

        This function queries the SerialWombatUART for avaialble TX
        buffer space, and sends bytes as buffer space is avaialble.
        If avaialable buffer space is not sufficient to send the entire
        array then the function will block and continue trying until the
        entire message has been sent to the SerialWombatUART transmit queue.
        """
        def write(self, buf,  size):
                bytesAvailable = 0
                bytesSent = 0
                timeoutMillis = millis() + self.timeout
                while( bytesSent  < size ):
                    while (bytesAvailable < 4):
                        peektx = [ 203, self._pin,self._pinMode,0x55,0x55,0x55,0x55,0x55 ]
                        result, peekrx = self._sw.sendPacket(peektx)
                        bytesAvailable = peekrx[3]
                        if (timeoutMillis < millis()):
                                return (bytesSent)
                        timeoutMillis = millis() + self.timeout
                    while (bytesSent < size and bytesAvailable > 0 ):
                            if ((size - bytesSent) < 7 or bytesAvailable < 7 or self._1ByteTransmissions):
                                    tx = [ 201, self._pin,self._pinMode,0,0x55,0x55,0x55,0x55 ]
                                    txLen = 0
                                    tx[3] = 0
                                    while( txLen < 4 and txLen < bytesAvailable and bytesSent < size):
                                            tx[4 + txLen] = buf[bytesSent]
                                            bytesSent += 1
                                            tx[3] += 1
                                            txLen += 1
                                            if (self._1ByteTransmissions):
                                                break
                                    result,rx = self._sw.sendPacket(tx)
                                    bytesAvailable = rx[3]
                            else:
                                    tx = [ self._tx7Command, 0x55,0x55,0x55,0x55,0x55,0x55,0x55 ]
                    
                                    for txLen in range(7):
                                           tx[1 + txLen] = buf[bytesSent]
                                           bytesSent += 1
                                           bytesAvailable -= 1
                                    self._sw.sendPacket(tx)
                return (bytesSent)

        """!
        @brief Queries the SerialWombatUART for the amount of free TX queue space
        @return A value between 0 and 64 for the SW4B
        """
        def availableForWrite(self):
                peektx = [ 203, self._pin,self._pinMode,0x55,0x55,0x55,0x55,0x55 ]
                result,peekrx = self._sw.sendPacket(peektx)
                return peekrx[3]

        """!
        @brief Reads a specified number of bytes from the SerialWombatUART RX queue
        @param buffer  An array into which to put received bytes
        @param length  The maximum number of bytes to be received
        @return the number of bytes written to buffer

        This function will read bytes from the SerialWombatUART RX queue into buffer.
        If 'length' characters are not available to read then the value returned
        will be less than length.
        """
        def readBytes(self, length):
                bytesAvailable = 0
                buf = bytearray()
                timeoutMillis = millis() + self.timeout
                while (length > 0 and timeoutMillis > millis()):
                        bytecount = 4
                        if (length < 4):
                                bytecount = length
                                
                        tx = [ 202, self._pin,self._pinMode,  bytecount,0x55,0x55,0x55,0x55 ]
                        result,rx = self._sw.sendPacket(tx)
                        bytesAvailable = rx[3]
                        
                        if (bytesAvailable == 0) :
                            continue
                        else:
                            timeoutMillis = millis() + self.timeout
                        bytesReturned = bytecount
                        if (rx[3] < bytecount):
                                bytesReturned = rx[3]
                        for i in range(bytesReturned):
                                buf.append( rx[i + 4])
                                bytesAvailable -= 1
                                length -= 1

                        while (bytesAvailable >= 7 and length >= 7):
                                tx = [ self._rx7Command, 0x55,0x55,0x55,0x55,0x55,0x55,0x55 ]
                                result,rx= self._sw.sendPacket(tx)
                                for i in range(7):
                                        buf.append( rx[i + 1])
                                        bytesAvailable -= 1
                                        length -= 1



                return (buf)


        def setTimeout(self, timeout_mS):
                if (timeout_mS == 0):
                        self.timeout = 0x80000000
                else:
                        self.timeout = timeout_mS

        def enable1ByteTransmissions(self,enabled = True):
            self._1ByteTransmissions = enabled;


"""! @brief A class for the Serial Wombat 4B or SW18AB chips which creates a software based UART on the SW18AB

A Tutorial video is avaialble:

@htmlonly
<iframe width="560" height="315" src="https://www.youtube.com/embed/C1FjcaiBYZs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
@endhtmlonly

https://youtu.be/C1FjcaiBYZs


The class inherits from the Arduino Sream class, so functions such as println()
can be used once the Software UART is initialized.


@warning Due to the overhead of querying and retreiving data from the SerialWombatUART,
data loss is likely when receiving streams of data greater than the buffer size at higher
baud rates.

Multiple instances of this class can be created on the Serial Wombat 18AB chip.  This pin mode requires 
more CPU time than most, particularly for higher baud rate ports.  Serial Wombat chip CPU usage should
be checked if multiple software uarts are used.  Exceeding the available SW18AB CPU resources will cause
bit errors in the UART.

A queue in the User Buffer area is allocated for RX and one for TX prior to as part of begin for this mode.
Size of these queues should be determined based on system needs.  The User needs to ensure that the created queues do
not overlap with other structures created in the User Buffer

A full Serial Wombat packet send / receive sequence (8 bytes in each direction) over I2C or the main UART is necessary to
query the status of the queues or to read or receive a byte of data.  

The protocol becomes more efficient if multiple bytes are read or written using the readBytes or 
write(const * buffer, size_t size) interfaces rather than read() or write( data).

The class must be assigned to a pin.  This may be either the receive or transmit pin.

Available baud rates are:
 - 300  
 - 1200 
 - 2400  
 - 4800  
 - 9600  
 - 19200 
 - 28800   (Transmit only, receive may be unreliable )
 - 57600  (Transmit only, receive may be unreliable )
"""
class SerialWombatSWUART ( SerialWombatUART):
  

    """!
    @param baudRate  300, 1200, 2400, 4800, 9600,  19200,  38400,  57600,  115200
    @param pin  The pin that will host the state machine.  This can be either the rxPin or txPin
    @param rxPin The pin that will receive.  All 4 pins on the SW4B may be used.  255 if no receive function is needed
    @param txPin The pin that will transmit.  Valid values for the SW4B are 1-3.  255 if no transmit function is needed
    @param userMemoryoffset The offset into User Memory where the software storage queues begin
    @param rxLength The length in bytes of the on-chip rx queue (can be 0 if rxPin == 255).  
    @param txLength The length in bytes of the on-chip tx queue (can be 0 if txPin == 255).  
    """
    def begin(self,  baudRate,  pin,  rxPin,  txPin,  userMemoryOffset,  rxLength,  txLength):
        self._rxPin = rxPin
        self._txPin = txPin
        self._pin = pin

        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_SW_UART


        if (baudRate == 300):
                self._baudMarker = 0
        elif (baudRate == 1200):
                self._baudMarker = 1
        elif (baudRate == 2400):
                self._baudMarker = 2
        elif (baudRate == 4800):
                self._baudMarker = 3
        elif (baudRate == 9600):
                self._baudMarker = 4
        elif (baudRate == 19200):
                self._baudMarker = 5
        elif (baudRate == 38400):
                self._baudMarker = 6
        elif (baudRate == 57600):
                self._baudMarker = 7
	
	#elif (baud == 115200):
        #default:
        else:
                self._baudMarker = 7;  # Limit to 57600
        tx = [ 200, self._pin,self._pinMode, self._baudMarker,self._rxPin,self._txPin,0x55, 0x55 ]

        result,rx = self._sw.sendPacket(tx)
        if (result < 0):
                return (result)
        rxoffset = 0
	#if (self._rxPin != 255)
	#{
        if (rxLength == 0):
                rxLength = 2
        self.rxQueue = SerialWombatQueue.SerialWombatQueue(self._sw)
        self.txQueue = SerialWombatQueue.SerialWombatQueue(self._sw)
        rxoffset = self.rxQueue.begin(userMemoryOffset, rxLength)
        if (rxoffset >= 0):
                userMemoryOffset += rxoffset
        else:
                return (0);  # No memory should have been allocated.
	#}

        txoffset = 0
	#if (self._txPin != 255)
	#{
        if (txLength == 0):
                txLength = 2
        txoffset = self.txQueue.begin(userMemoryOffset, txLength)
        if (txoffset >= 0):
                userMemoryOffset += txoffset
        else:
                return rxoffset
	#}

        tx5 = bytearray([ 205,self._pin,self._pinMode]) + SW_LE16(self.txQueue.startIndex) + bytearray([0x55,0x55,0x55])
        result,rx = self._sw.sendPacket(tx5)
        if (result < 0):
            return (result)


        tx6 = bytearray([ 206,self._pin,self._pinMode]) + SW_LE16(self.rxQueue.startIndex) + bytearray([0x55,0x55,0x55])
        result,rx = self._sw.sendPacket(tx6)
        if (result < 0):
            return (result)

        return (txoffset + rxoffset)

    """
    #This method can't be called for Software UART because it doens't initialize queues in User Data Area
    """
    #int16_t begin( baudRate,  pin,  rxPin,  txPin,  HWinterface) = delete

    """!
    @brief Write bytes to the SerialWombatUART for Transmit
    @param buffer  An array of  bytes to send
    @param size the number of bytes to send
    @return the number of bytes sent
    
    This function queries the SerialWombatSWUART for avaialble TX
    buffer space, and sends bytes as buffer space is avaialble.
    If avaialable buffer space is not sufficient to send the entire
    array then the function will block and continue trying until the
    entire message has been sent to the SerialWombatUART transmit queue.
    """
    def write(self, buffer,  size):
        return (self.txQueue.writeBuffer(buffer, size))
    
    """!
    @brief  Discard all received bytes
    """
    def flush(self):
        self.rxQueue.flush()
    

