"""
Copyright 2021-2023 Broadwell Consulting Inc.

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

"""! @file SerialWombatMatrixKeypad.h
"""

import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombat import SW_LE32
from SerialWombat import SW_LE16
from ArduinoFunctions import millis

"""! @brief A class for the Serial Wombat SW18AB chips which scans matrix keypads up to 4x4



A Tutorial video is avaialble:

https://youtu.be/hxLda6lBWNg
@htmlonly
<iframe width="560" height="315" src="https://www.youtube.com/embed/hxLda6lBWNg" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
@endhtmlonly



The class inherits from the Arduino Stream class, so queued kepad presses can be read like a
Serial port.

This class allows the user to declare up to 4 row and 4 column pins which are strobed continuously
to read up to 16 buttons.  The Serial Wombat chip's internal pull-up resistors are used so no additional
hardware is necesary.  Standard matrix keypads can be attached directly to the Serial Wombat chip pins.
All Serial Wombat 18AB chip pins can be used in any combination or order.

Results can be returned to the host as a binary 16 bit number indicating the state of 16 buttons, 
as an index indicating which button is currently pressed (0 for Col 0 Row 0,  3 for Col 3 Row 3 and
12 for Col 0 Row 3, or as ASCII values which assume a standard keypad layout.

Index mode:

    |0  1  2  3 |
    |4  5  6  7 |
    |8  9  10 11|
    |12 13 14 15|
    With 16 being used for no current press, depending on mode setting

Ascii Mode:

    |1 2 3 A|
    |4 5 6 B|
    |7 8 9 C|
    |* 0 # D|

Note that the key indexes remain the same regardless of how many rows and columns are enabled.

The Serial Wombat 18AB firmware also keeps track of button transition counts and time since last
transition for all 16 buttons.  In this way each key of the keypad can be treated equivalently to
a SerialWombatDebouncedInput class when encapsulated in a SerialWombatMatrixInput class.  See the
documentation on this class and Arduino examples for details.

The 16 Bit public data presented internally to other Serial Wombat pins and through the SerialWombatChip.readPublicData
method can be configured to present the binary state of 16 buttons, the last button index pressed, 
the last button index pressed or 16 if no button is pressed, or ASCII of last button pressed.

"""

class SerialWombatMatrixKeypad (SerialWombatPin):
    def __init__(self,serial_wombat):
        self._sw = serial_wombat
    """
    @brief Initalize the SerialWombatMatrixKeypad.  
    @param controlPin Keypad scanning transitions will occur while this pin is being serviced by the Serial Wombat executive.  Typically this will be the same as the row0 pin
   @param row0pin pin attached to the topmost keypad row.  On many marked keypads this row has 1,2,3 and A in it.  Enter 255 if this column is unused
    @param row1pin pin attached to the topcenter keypad row.  On many marked keypads this row has 4,5,6 and B in it.  Enter 255 if this row is unused
    @param row2pin pin attached to the topmost keypad row.  On many marked keypads this row has 7,8,9 and C in it.  Enter 255 if this row is unused
    @param row3pin pin attached to the topmost keypad row.  On many marked keypads this row has *,0,# and D in it.  Enter 255 if this row is unused
    @param column0pin pin attached to the leftmost keypad column.  On many marked keypads this column has 1,4,7 and * in it.  Enter 255 if this column is unused
    @param column1pin pin attached to the leftcenter keypad column.  On many marked keypads this column has 1,5,8 and 0 in it. Enter 255 if this column is unused
    @param column2pin pin attached to the rightcenter keypad column.  On many marked keypads this column has 3,5,9 and # in it. Enter 255 if this column is unused
    @param column3pin pin attached to the rightmost keypad column.  On many marked keypads this column has A,B,C and D in it. Enter 255 if this column is unused
     @param bufferMode 0: Public data is Binary of 16 keys (Default)  1:  Public data is last key index pressed  2:  Public data is last key pressed or 16 for no key index  3: Public data is Ascii of last key pressed 
    @param queueMode 0: Button presses are queued as indexes 1: Button Presses are queued as ASCII
    """
    def begin(self, controlPin, row0pin, row1pin, row2pin, row3pin, column0pin, column1pin, column2pin, column3pin, bufferMode = 0, queueMode = 1):
        self._pin = controlPin

        tx = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
							self._pin,
							SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD ,
							row0pin,
							row1pin,
							row2pin,
							row3pin,
							column0pin ]
        result,rx = self._sw.sendPacket(tx)
        if (result < 0):
            return result

        tx5 = [ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE5,
							self._pin,
							SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD ,
							column1pin,
							column2pin,
							column3pin,
							bufferMode,
							queueMode ]
        result,rx = self._sw.sendPacket(tx5)
        return result
    

    """!
    @brief Set a binary mask for which keys are added to Queue
    
    This commands allows exclusion of keys from being queued.  This
    can be useful if, for instance, only the numeric keys of a keypad
    are to be added to the queue (excluding #,*, ABCD, etc) 
    
    @param mask  A 16 bit bitmap where a 1 allows queuing of that key index 
    and a 0 does not.  Index 0 is LSB.  For instance, for a typical Phone/ABCD
    keypad, a mask of 0x2777 would allow the numeric keys to be added to the 
    queue but would exclude ABCD#* .
    @return Returns 0 or higher if successfully set or a negative error code otherwise.
    """
    def writeQueueMask(self,mask):

        tx = bytearray([ SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE7,
			self._pin, SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD]) + SW_LE16(mask) + bytearray([0x55,0x55,0x55 ])
        result ,_rx =  self._sw.sendPacket(tx);
        return result

    """!
    @brief Queries the SerialWombatMatrixKeypad for number bytes available to read
    @return Number of bytes available to read.
    """
    def available(self):
        tx = [ 201, self._pin, SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD, 0,0x55,0x55,0x55,0x55 ]
        _result, rx = self._sw.sendPacket(tx, rx)
        return (rx[4])


    """!
    @brief Reads a byte from the SerialWombatMatrixKeypad queue
    @return A byte from 0-255, or -1 if no bytes were avaialble
    """
    def read(self):
        tx = [ 202, self._pin,SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD, 1,0x55,0x55,0x55,0x55 ]
        result, rx = self._sw.sendPacket(tx)
        if ( result < 0):
            return -1

        if (rx[3] != 0):
            return (rx[4]);
        else:
            return (-1);

    # @brief  Discard all bytes from the SerialWombatMatrixKeypad queue
    def flush():
        pass
    """!
    @brief Query the SerialWombatMatrixKeypad queue for the next avaialble byte, but don't remove it from the queue
    @return A byte from 0-255, or -1 if no bytes were avaialble
    """
    def peek(self):
        tx = [ 203, self._pin,SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,0x55,0x55,0x55,0x55,0x55 ]
        _result, rx = self._sw.sendPacket(tx)
        if (rx[4] > 0):
            return (rx[5])
        else:
            return (-1)

    """!
    @brief Write a byte to the SerialWombatMatrixKeypad queue  (Does Nothing)
    @param data  Byte to write
    @return Number of bytes written
    
    This function exists to fully implement the Stream class.  It throws away the byte.
    """
    def write(data):
        return (1)

    """!
    @brief Write bytes to the SerialWombatMatrixKeypad queue (Does nothing)
    @param buffer  An array of bytes to send
    @param size the number of bytes to send
    @return the number of bytes sent

    This function exists to fully implement the Stream class.  It throws away the bytes.
    """
    def write(self,buffer,  size):
        return(size)

    """!
    @brief Number of bytes avaialble to write to SerialWombatMatrixKeypad queue.  Returns 0
    @return Zero.  Writes are not suppored.
    """
    def availableForWrite(self):
        return(0)

    """!
    @brief Reads a specified number of bytes from the SerialWombatMatrixKeypad queue queue

    @param length  The maximum number of bytes to be received
    @return a bytearray of bytes
    
    This function will read bytes from the SerialWombatMatrixKeypad queue into buffer.
    If 'length' characters are not available to read then the value returned
    will be less than length.
    """
    def readBytes(self, length):
        buffer = bytearray()
        timeoutMillis = millis() + self.timeout
        while (length > 0 and timeoutMillis > millis()):
            bytecount = 4
            if (length < 4):
                bytecount = length
            tx = [ 202, self._pin,SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD, bytecount,0x55,0x55,0x55,0x55]
            result,rx = self._sw.sendPacket(tx)
            bytesAvailable = rx[3]

            if (bytesAvailable == 0):
                continue
            else:
                timeoutMillis = millis() + self.timeout
            bytesReturned = bytecount
            if (rx[3] < bytecount):
                bytesReturned = rx[3]
            for i in range(bytesReturned):
                buffer += bytearray(rx[i + 4])
                index += 1
                bytesAvailable -= 1
                length -= 1
        return (bytearray)


    """!
    @brief implemented to fulfill Stream requirement.
    """
    def setTimeout(self,timeout_mS):
        if (timeout_mS == 0):
            self.timeout = 0x80000000;
        else:
            self.timeout = timeout_mS;



"""!
@brief Class that runs on top of SerialWombatMatrixKeypad to treat a key as an individual button

This class allows a single key from a SerialWombatMatrixKeypad to be treated as an individual SerialWombatAbstractButton
that can be read as such or passed to SerialWombatButtonCounter .  
"""
class SerialWombatMatrixButton :

    """!
    @brief Initialize a SerialWombatMatrixButton

    @param kp An initialized SerialWombatMatrixKeypad
    @param keyIndex a number 0-15 indicating which key (index, not ascii value) is treated as a button
    """
    def __init__(self,kp, keyIndex):

        self._keypad = kp
        self._keyIndex = keyIndex
        self.transitions = 0


    """!
    @brief Returns the  state of the input
    
    This function reads from the public data of the pin which 
    indicates the state of the
    input
    @return TRUE for pressed or FALSE.  
    """
    def digitalRead(self):

        tx = [SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
					self._keypad._pin,
					SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
					0,
					self._keyIndex,0x55,0x55,0x55 ]

        result,rx = self._keypad._sw.sendPacket(tx)
        if (result >= 0):

            transitions = rx[4] + 256 * rx[5]

            return (rx[3] > 0)

        return(0)

    """!
    @brief return the number of mS that the button has been in false state
 
 
 @return returns a value in mS which saturates at 65535.  Returns 0 if currently true.
 	"""
    def readDurationInFalseState_mS(self):
        tx = [SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
					self._keypad._pin,
					SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
					0,
					self._keyIndex,0x55,0x55,0x55 ]
        result,rx = self._keypad._sw.sendPacket(tx)
        if (result >= 0):
        
            transitions = rx[4] + 256 * rx[5]
            time = rx[6] + 256 * rx[7]
            if (rx[3] == 0):
                return(time)

        
        return(0)

    """!
    @brief return the number of mS that the button has been in true state
    
    @return returns a value in mS which saturates at 65535.  Returns 0 if currently false.
    """
    def readDurationInTrueState_mS(self):
        tx = [SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
                        self._keypad._pin,
                        SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
                        0,
                        self._keyIndex,0x55,0x55,0x55]
        result, rx = self._keypad._sw.sendPacket(tx);
        if (result >= 0):

            transitions = rx[4] + 256 * rx[5]
            time = rx[6] + 256 * rx[7]
            if (rx[3] == 1):
            
                return(time);
            
        return(0)


    """!
    @brief Queries the number of transistions that have occured on the button
    
    This function queries the button for current state and transitions since last call.
    transition count is put in the global member transitions.  The keypad driver in the Serial
    Wombat chip resets its count to zero after this call.
    
    @return TRUE or FALSE, current status of debounced input
    """
    def readTransitionsState(self):
	    return self.digitalRead();


