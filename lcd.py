from machine import Pin
import time

class LCD:
    # define the LCD commands
    LCD_CLEAR_DISPLAY = 0x01
    LCD_RETURN_HOME = 0x02
    LCD_ENTRY_MODE_SET = 0x04
    LCD_DISPLAY_CONTROL = 0x08
    LCD_CURSOR_SHIFT = 0x10
    LCD_FUNCTION_SET = 0x20
    LCD_SET_CGRAM_ADDR = 0x40
    LCD_SET_DDRAM_ADDR = 0x80

    def __init__(self, rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin):
        self.rsPin = Pin(rsPin, Pin.OUT)
        self.enPin = Pin(enPin, Pin.OUT)
        self.d4Pin = Pin(d4Pin, Pin.OUT)
        self.d5Pin = Pin(d5Pin, Pin.OUT)
        self.d6Pin = Pin(d6Pin, Pin.OUT)
        self.d7Pin = Pin(d7Pin, Pin.OUT)
        self.rsPin.value(0)
        self.enPin.value(0)
        self.d4Pin.value(0)
        self.d5Pin.value(0)
        self.d6Pin.value(0)
        self.d7Pin.value(0)
        self.num_lines = 2
        self.num_columns = 16
        self.cursor_x = 0
        self.cursor_y = 0
        #Initializing the display
        self.writeCommand(0x33) # Display ON cursor ON
        self.writeCommand(0x32)
        self.writeCommand(self.LCD_FUNCTION_SET | 0x08 | 0x04 | 0x00)
        self.writeCommand(self.LCD_DISPLAY_CONTROL | 0x04 | 0x00)
        self.writeCommand(self.LCD_CLEAR_DISPLAY)
        self.writeCommand(self.LCD_ENTRY_MODE_SET | 0x02)
        self.writeCommand(self.LCD_RETURN_HOME)
        self.writeCommand(self.LCD_DISPLAY_CONTROL | 0x04 | 0x02 | 0x01)


    def sleepLCD(self):
        time.sleep(0.005)

    # Adds the data to the 4 bits used, since we are in 4-bit mode
    def setDataPins(self, value):
        self.d4Pin.value(value & 0x01)
        self.d5Pin.value(value & 0x02)
        self.d6Pin.value(value & 0x04)
        self.d7Pin.value(value & 0x08)

    # Sends commands to the screen
    def writeCommand(self, cmd):
        #Data into pins
        # Shifting bits to send the data
        self.setDataPins(cmd >> 4)
        # RS pin needs to be 0 when sending commands
        self.rsPin.value(0)
        self.enPin.value(1)
        self.sleepLCD()
        self.enPin.value(0)
        self.sleepLCD()

        # Sending without shifting to capture the rest of the command
        self.setDataPins(cmd)
        self.rsPin.value(0)
        self.enPin.value(1)
        self.sleepLCD()
        self.enPin.value(0)
        self.sleepLCD()

    def writeData(self, data):
        #Data into pins
        # Shifting bits to send the data
        self.setDataPins(ord(data) >> 4)
        # RS pin needs to be 1 when sending data
        self.rsPin.value(1)
        self.enPin.value(1)
        self.sleepLCD()
        self.enPin.value(0)
        self.sleepLCD()

        # Sending without shifting to capture the rest of the command
        self.setDataPins(ord(data))
        self.rsPin.value(1)
        self.enPin.value(1)
        self.sleepLCD()
        self.enPin.value(0)
        self.sleepLCD()

    def displayString(self, message):
        # Sending one character at a time
        for char in message:
            self.writeData(char)
            self.writeCommand(0x04)
            print(char)
            # Shifting cursor to write next letter in proper location
            self.cursor_x += 1
            if self.cursor_x >= self.num_columns:
                self.cursor_x = 0
                self.cursor_y += 1
                self.implied_newline = (char != '\n')
            if self.cursor_y >= self.num_lines:
                self.cursor_y = 0
            self.move_to(self.cursor_x, self.cursor_y)

    #Function to clear the screen and start at the begining
    def clear(self):
        self.writeCommand(0x01)
        self.writeCommand(0x02)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        """Moves the cursor position to the indicated position. The cursor
        position is zero based (i.e. cursor_x == 0 indicates first column).
        """
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40    # Lines 1 & 3 add 0x40
        if cursor_y & 2:    # Lines 2 & 3 add number of columns
            addr += self.num_columns
        self.writeCommand(self.LCD_SET_DDRAM_ADDR | addr)


# lcdScreen = LCD(2, 1, 6, 5, 4, 3)
# #time.sleep(5)
# lcdScreen.displayString("Hello World!")
# time.sleep(5)
# lcdScreen.clear()