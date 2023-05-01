import time
from simongame import SimonGame
from shipgame import ShipGame
from servo import Servo, servo2040
from triviagame import TriviaGame

def main():
    s = Servo(servo2040.SERVO_1)
    # Enable the servo (this puts it at the middle)
    s.enable()
    # Close Box
    s.to_max()
    time.sleep(5)
    
    # Collision Avoidance Game
    shipGame = ShipGame(21, 20, 2, 7)
    print("Start of Collision Avoidance Game")
    shipGame.playGame()
    print("End of the Collision Avoidance Game")
    
    time.sleep(3)
    #Simon Game
    simonGame = SimonGame(12,13,14,15,7,11,9,10,8)
    print("Start of the Simon Game")
    simonGame.playGame()
    print("End of the Simon Game")
    
    time.sleep(3)
    #Trivia Game
    print("Start of Trivia Game")
    triviaGame = TriviaGame(2, 1, 6, 5, 4, 3)
    triviaGame.playGame()
    print("End of the Trivia Game")
    
    # Open Box
    s.to_min()
    time.sleep(5)
    s.to_max()
    # Disable the servo
    s.disable()

main()
