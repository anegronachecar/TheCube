from machine import Pin, PWM
import time
import random
from buzzer import Buzzer
from numberdisplay import NumberDisplay

class SimonGame:
    sequence = []
    leds = []
    buttons = []

    def __init__(self, pin1, pin2, pin3, pin4, buzzerPin, dPin, lPin, clkPin, clrPin):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.buzzer = Buzzer(buzzerPin)
        self.numberDisplay = NumberDisplay(dPin, lPin, clkPin, clrPin)

    def setLEDs(self):
        #Function to set the PINs as Output from pico to control the LEDs
        self.led1 = Pin(self.pin1, Pin.OUT)
        self.led2 = Pin(self.pin2, Pin.OUT)
        self.led3 = Pin(self.pin3, Pin.OUT)
        self.led4 = Pin(self.pin4, Pin.OUT)
        self.led1.value(0)
        self.led2.value(0)
        self.led4.value(0)
        self.led3.value(0)
        # Array containing values for easy identification during code and less duplicate code
        self.leds = [self.led1, self.led2, self.led3, self.led4]

    def setButtons(self):
        #Function to set the PINs as Inputs for pico to read the button press
        self.button1 = Pin(self.pin1, Pin.IN, Pin.PULL_DOWN)
        self.button2 = Pin(self.pin2, Pin.IN, Pin.PULL_DOWN)
        self.button3 = Pin(self.pin3, Pin.IN, Pin.PULL_DOWN)
        self.button4 = Pin(self.pin4, Pin.IN, Pin.PULL_DOWN)
        # Array containing values for easy identification during code and less duplicate code
        self.buttons = [self.button1, self.button2, self.button3, self.button4]

    def playSequence(self):
        # Play sequence code
        # Adds a random number to the sequence
        self.sequence.append(random.randint(0, 3))
        # Turn LED Pins to Output
        self.setLEDs()
        # Sent the pattern
        for s in self.sequence:
            # Play tone on buzzer
            self.buzzer.playTone(s)
            # Turn on the LED
            self.leds[s].value(1)
            time.sleep(.75)
            # Turn off LED and buzzer
            self.buzzer.stopTune()
            self.leds[s].value(0)
            time.sleep(0.5)

    def readUserInputs(self):
        # Get User's Input
        # Settin pins to read button presses
        self.setButtons()
        for s in self.sequence:
            button_pressed = False
            # Wait for a button to be pressed
            while button_pressed == False:
                button_number = 0
                # Checking each button to be pressed
                for b in self.buttons:
                    if b.value():
                        button_pressed = True
                        self.buzzer.playTone(button_number)
                        time.sleep(.75)
                        self.buzzer.stopTune()
                        break
                    button_number +=1
            # Checking to see if the button pressed is the same for the sequence
            if button_number != s:
                # If not, game over
                print("Game Over")
                self.buzzer.playTone(4)
                self.sequence = []
                time.sleep(.75)
                self.buzzer.stopTune()
                break

    def playGame(self):
        print("Game Started")
        self.numberDisplay.displayNumber(0)
        while len(self.sequence) < 5:
            # Get sequence from pico
            self.playSequence()
            # Read input from user until the right sequence is entered or a mistake was made
            self.readUserInputs()
            # Display number in the 7-segment display
            self.numberDisplay.displayNumber(len(self.sequence))