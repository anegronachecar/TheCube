from machine import Pin 
import time

class NumberDisplay:
    #Numbers to be displayed on 7 Segment LED 
    #     __a___
    #    |      |
    #   f|      |b
    #    |      |
    #     ---g---
    #    |      |
    #   e|      |c
    #    |______|
    #       d       dp
    # Configuration used for realstate
    # dp  __d___
    #    |      |
    #   c|      |e
    #    |      |
    #     ---g---
    #    |      |
    #   b|      |f
    #    |______|
    #       a       
    #
    # e, b, a, dp, c, d, g, f

    # Data Array containing the numbers. Coment above shows how we are mapping the bits on the array
    dataArray = [0b00010010, 0b01111110,0b00011001,0b01011000,0b01110100,0b11010000,0b10010000,0b01111010,
        0b00010000,0b01010000]

    def __init__(self, dPin, lpin, clkPin, clrPin, **kwargs):
        self.dataPin = Pin(dPin, Pin.OUT)
        self.latchPin = Pin(lpin, Pin.OUT)
        self.clockPin = Pin(clkPin, Pin.OUT)
        self.clearPin = Pin(clrPin, Pin.OUT)
        #Seeting pins default values
        self.dataPin.value(0)
        self.latchPin.value(0)
        self.clockPin.value(0)
        self.clearPin.value(1)

    #Fucntion to clear the display
    def clearDisplay(self):
        self.clearPin.low()
        time.sleep(0.005)
        self.clearPin.high()
    
    #Function that adds the bits to the output of the register
    def addBitData(self):
        self.clockPin.low()
        time.sleep(0.005)
        self.clockPin.high()
        time.sleep(0.005)
        self.clockPin.low()
     
    #Function that sends the bits to the output of the register  
    def sendToDisplay(self):
        self.latchPin.low()
        time.sleep(0.005)
        self.latchPin.high()

    # Main function called by the program to display a number
    def displayNumber(self, number):
        # Numbers are alinged with the array. dataArray[0] shows the value to display 0, etc.
        print(self.dataArray[number])
        #print("Start")
        for i in range(8):
            data = self.dataArray[number] >> i & 1
            #print(data)
            if data == 0:
                self.dataPin.low()
            else:
                self.dataPin.high()
            time.sleep(0.005)
            self.addBitData()
        self.sendToDisplay()
        #print("End")
        time.sleep(0.5)