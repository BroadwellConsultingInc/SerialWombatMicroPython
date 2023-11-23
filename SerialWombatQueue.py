#pragma once
"""
Copyright 2020-2023 Broadwell Consulting Inc.

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

#include <stdint.h>
#include "SerialWombat.h"

import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE16
from ArduinoFunctions import millis
from ArduinoFunctions import delay

"""
class SerialWombatQueueType(IntEnum):
    QUEUE_TYPE_RAM_BYTE = 0,  #!< A queue that queues byte-sized data in a queue in the User RAM area
    QUEUE_TYPE_RAM_BYTE_SHIFT = 1,  #!< A queue that queues byte-sized data in a queue in the User RAM area
"""

"""!
 @brief A Class representing a Queue in the User Ram area on the Serial Wombat Chip
"""


class SerialWombatQueue:
    """!
    @brief Constructor for SerialWombatWS2812 class
    @param serialWombat SerialWombat chip on which the driver will run
    """
    def __init__(self,serial_wombat):
        self._sw = serial_wombat
        self._timeout = 500
        self.startIndex = 0xFFFF
        self.length = 0

    """!
    @brief Initialize a Serial Wombat Queue (RAM Bytes) in User Memory Area on Serial Wombat Chip
    ///
    @param index  An index in bytes for the beginning of the Queue location in Serial Wombat User Memory Area
    @param length The length in bytes of avaialble queue space
    @return A positive number indicating the number of bytes used in User Memory Area (Will be more than
    length due to queue management variables) or a negative number indicating an error code.
    """
    def begin(self, index,  length, qtype = 0 ): 
        self.startIndex = index
        self.length = length
        tx = bytearray([0x90]) + SW_LE16(index) + SW_LE16(length)+ bytearray([qtype, 0x55,0x55] )
        result,rx =  self._sw.sendPacket(tx)
        if (result < 0):
            return result
        else:
            return (rx[3] + 256 * rx[4])

    """!
    @brief Queries the Serial Wombat for number bytes available to read
    @return Number of bytes available to read.
        """
    def available(self):
        tx = bytearray([0x94])+ SW_LE16(self.startIndex) + bytearray([0x55,0x55,0x55,0x55,0x55])
        sendResult,rx =  self._sw.sendPacket(tx)
        if (sendResult >= 0):
            return (rx[4] + 256 * rx[5])
        return (0)
    """!
    @brief Reads a byte from the Serial Wombat
    @return A byte from 0-255, or -1 if no bytes were avaialble
    """
    def read(self):
        tx = bytearray([0x93]) +  SW_LE16(self.startIndex) + bytearray([1,0x55,0x55,0x55,0x55]) 
        sendResult,rx = self._sw.sendPacket(tx)
        if (sendResult >= 0):
            if (rx[1] == 1):
                return (rx[2])
        return (-1)
    """!
    @brief  Discard all received bytes
    """
    def flush(self):
        self.begin(self.startIndex, self.length)
    """!
    @brief Query the Serial Wombat for the next avaialble byte, but don't remove it from the queue
    @return A byte from 0-255, or -1 if no bytes were avaialble
    """
    def peek(self):
        tx = bytearray([ 0x94 ])+SW_LE16(self.startIndex) + bytearray([0x55,0x55,0x55,0x55,0x55 ])
        sendResult,rx = self._sw.sendPacket(tx)
        if (sendResult >= 0):
            if ((rx[4] + 256 * rx[5]) > 0):
                return(rx[3])
        return (-1)

    """!
    @brief Write a byte to the Serial Wombat Queue
    @param data  Byte to write
    @return Number of bytes written
    """
   
    def write(self, data):
        tx = bytearray( [0x91] ) + SW_LE16(self.startIndex) + bytearray([1,data,0x55,0x55,0x55 ])
        sendResult,rx = self._sw.sendPacket(tx)
        if (sendResult >= 0):
                return(rx[3])
        return (0)

    """!
    @brief Write bytes to the Serial Wombat Queue
    @param buffer  An array of  bytes to send
    @param size the number of bytes to send
    @return the number of bytes sent
    
    This function queries the Serial Wombat Queue
    buffer space, and sends bytes as buffer space is avaialble.
    If avaialable buffer space is not sufficient to send the entire
    array then the function will block and continue trying until the
    entire message has been sent to the Serial Wombat  queue.
    """
    def writeBuffer(self, buffer, size):
        bytesWritten = 0
        startTime = millis()

        #Write up to the first 4 bytes
        if (size >= 4):
            nextWriteSize = 4
        else:
            nextWriteSize = size
        tx = bytearray([ 0x91])+ SW_LE16(self.startIndex) + bytearray([0,0x55,0x55,0x55,0x55 ])
        for i in range(nextWriteSize):
                tx[4 + i] = buffer[i]
        tx[3] = nextWriteSize
        sendResult,rx  = self._sw.sendPacket(tx)
        if (sendResult < 0):
                return(bytesWritten)
        bytesWritten += rx[3]

        while ((size - bytesWritten) >= 7):
            tx = [0x92 ,
                buffer[bytesWritten],
                buffer[bytesWritten + 1],
                buffer[bytesWritten + 2],
                buffer[bytesWritten + 3],
                buffer[bytesWritten + 4],
                buffer[bytesWritten + 5],
                buffer[bytesWritten + 6]]

            sendResult,rx = self._sw.sendPacket(tx)
            if (sendResult < 0):
                return(bytesWritten)
            bytesWritten += rx[3]
            delay(0)
            if (millis() > startTime + self._timeout):
                return(bytesWritten)

        while (size - bytesWritten > 0):
            if (size - bytesWritten >= 4):
                    nextWriteSize = 4
            else:
                    nextWriteSize = (size - bytesWritten)
            tx = bytearray([0x91]) + SW_LE16(self.startIndex) + bytearray([0,0x55,0x55,0x55,0x55 ])
            for i in range( nextWriteSize):
                    tx[4 + i] = buffer[i + bytesWritten]
            tx[3] = nextWriteSize
            sendResult,rx = self._sw.sendPacket(tx)
            if (sendResult < 0):
                    return(bytesWritten)
            bytesWritten += rx[3]
            if (millis() > startTime + self._timeout):
                    return(bytesWritten)
        return (bytesWritten)

    """!
    @brief Queries the Serial Wombat for the amount of free queue space
    @return Number of bytes avaialable
    """
    def availableForWrite(self,):
        tx = bytearray([0x94]) +  SW_LE16(self.startIndex) + bytearray([0x55,0x55,0x55,0x55,0x55 ])
        sendResult,rx = self._sw.sendPacket(tx)
        if (sendResult >= 0):
            return (rx[6] + 256 * rx[7])
        return (0)

    """!
    @brief Reads a specified number of bytes from the Serial Wombat Queue
    @param buffer  An array into which to put received bytes
    @param length  The maximum number of bytes to be received
    @return the number of bytes written to buffer
    
    This function will read bytes from the Serial Wombat Queue into buffer.
    If 'length' characters are not available to read then the value returned
    will be less than length.
    """
    def readBytes(self, length):
        bytesAvailable = 0
        startTime = millis()
        buffer = bytearray()
        tx = bytearray( [0x94])+ SW_LE16(self.startIndex)+ bytearray([0x55,0x55,0x55,0x55,0x55])
        sendResult,rx = self._sw.sendPacket(rx)
        if (sendResult >= 0):
                bytesAvailable = (rx[4] + 256 * rx[5])

        if (bytesAvailable < length):
                length = bytesAvailable
        bytesRead = 0
        while (bytesRead < length):
            bytesToRead = length - bytesRead
            if (bytesToRead > 6):
                bytesToRead = 6
            tx = bytearray([ 0x93]+SW_LE16(self.startIndex)+ bytearray[bytesToRead,0x55,0x55,0x55,0x55 ])
            sendResult,rx = self._sw.sendPacket(tx)
            if (sendResult >= 0):
                    for i  in range( rx[1]):
                        if (bytesRead < length):
                                buffer+= bytearray( rx[2 + i])
                                bytesRead +=1
                        else:
                            return (bytesRead)  
            if (millis() > startTime + self._timeout):
                return(bytesRead)
        return bytesRead



    def setTimeout(self,  timeout_mS):
        self._timeout = timeout_mS

    #TODO add copy interface

	
