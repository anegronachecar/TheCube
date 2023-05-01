from machine import Pin, PWM
class Buzzer:

    # Each button has its own frequency of sound
    gameSounds = [262, 330, 392, 494, 73] # Last sound for game over

    def __init__(self, buzzPin):
        self.buzzer = PWM(Pin(buzzPin))

    def playTone(self, number):
        # Buzzer tone based on frequency
        self.buzzer.freq(self.gameSounds[number])
        self.buzzer.duty_u16(1000)

    def stopTune(self):
        self.buzzer.duty_u16(0)