import time
from machine import ADC, Pin
from lcd import LCD

class TriviaGame:
    # Hardcoded questions and answers for the game
    questions = ["Iron Man is a genius billionaire", "Thanos snapped  twice in Endgame", "Spider Man is   from Queens NY", "Thor is the God of Thunder"]
    answers = [True, False, True, True]
    def __init__(self, rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin):
        # Create the LCD object
        self.lcd = LCD(rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin)
        # ADC for A0 button
        self.buttonADC = ADC(Pin(26))
        self.score = 0

    def sendMessage(self, message):
        # Sending a message to the LCD
        self.lcd.clear()
        self.lcd.displayString(message)

    def clearScreen(self):
        self.lcd.clear()
        
    def checkGameResult(self):
        # Final check to see wether the user win or loose.
        if self.score >= 3:
            message = "Winner! Claim   your Price"
        else:
            message = "You Loose"
        self.sendMessage(message)
        time.sleep(5)
        self.clearScreen()
        
    def playGame(self):
        result = False
        
        while result != True:
            # Looping throug the questions
            for index, question in enumerate(self.questions):
                self.sendMessage(question)
                time.sleep(1)
                buttonPressed = False
                selection = False
                # Loop that waits until one fo the two buttons is pressed
                while buttonPressed != True:
                    # ADC value is stored and compared to see which button was pressed
                    # If its within the range, it registerd the answer accordingly
                    buttonMeasurement = self.buttonADC.read_u16()
                    print(buttonMeasurement)
                    if  buttonMeasurement < 65000 and buttonMeasurement > 35000:
                        selection = True
                        buttonPressed = True
                    elif buttonMeasurement < 15500 and buttonMeasurement > 200:
                        selection = False
                        buttonPressed = True
                    time.sleep(0.5)
                #After button press is identified, check if it matches the answer
                if selection == self.answers[index]:
                    self.sendMessage("Correct Answer!")
                    self.score += 1
                    time.sleep(2)
                else:
                    self.sendMessage("Worng Answer!")
                    time.sleep(2)
                # If 3 correct answer, exit game
                if self.score >= 3:
                    result = True
                    break
            # Check if the user won or loss
            self.checkGameResult()