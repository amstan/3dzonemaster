#3DZoneMaster Driver
##by amstan

This is an attempt at writing a driver for the Techmedia 3DZoneMaster. Since I didn't have any protocol specs, i had to reverse engineer it.

##Serial Port considerations
Since this device is powered of the serial port, it's very finicky in terms of what it likes. It seems to use either the rts or the dtr line for power, this line should have a positive voltage. I could not get it to work with 
one of my usb->rs232 adaptors.

##Protocol specs
The device always sends packets when the joystick is pointed at it.

The packets are 5 bytes long, always start with a byte that ANDs with 0x80.

###Buttons
Each button has a bit in the message, most of them in the last bit, some of them in the first nibble.

###Positions
Relative positions are sent as fast as the serial port can handle it, while the joystick is in range.
X,Y,Z deltas are byte 1,2,3 respectively. 7 bits each(the 8th bit is reserved for the start of message), sign dependent on direction. Second nibble of the message contains direction for each of the axis. The direction bit+the 7 size bits add up to 8 bit signed(2's complement) value.