import time
import random
import math
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from players import Ball, Triangle


class ShipGame:

    balls=[]
    
    def __init__(self, btnAPin, btnBPin, difficulty, shipSpeed):
        self.button_a = Button(btnAPin)
        self.button_b = Button(btnBPin)
        self.difficulty = difficulty
        # Starting the display
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0, pen_type=PEN_P8)
        self.display.set_backlight(1.0)
        self.WIDTH, self.HEIGHT = self.display.get_bounds()
        self.WHITE = self.display.create_pen(255, 255, 255)
        self.BLACK = self.display.create_pen(0, 0, 0)
        # Creating ship
        self.ship = Triangle(20, 82, 20, 58, 36, 70, shipSpeed, 5, self.display.create_pen(255, 0, 0))
        self.createBalls()

    # Function to create the enemies
    def createBalls(self):
        for i in range(0, self.difficulty):
            r = random.randint(0, 10) + 3
            self.balls.append(
                Ball(
                    random.randint(r, r + (self.WIDTH - 2 * r)),
                    random.randint(r, r + (self.HEIGHT - 2 * r)),
                    r,
                    (14 - r) / 2,
                    (14 - r) / 2,
                    self.display.create_pen(0, 0, 255),
                    self.WIDTH,
                    self.HEIGHT
                )
            )
       
    def restartGame(self):
        # Restarting all values for the game
        self.balls=[]
        self.createBalls()
        self.ship.life = 5
        self.ship.score = 0
        
    def displayFinishMessage(self, message):
        # Diplay the final message, wether the user wins or looses
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.display.set_pen(self.WHITE)
        self.display.text(message, 40, 70, 0, 3)
        self.display.update()
        time.sleep(2)
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.display.update()
        
        # Main game function
    def playGame(self):
        # Either we win by a score of 7 or loose all our lives
        while self.ship.life > 0 and self.ship.score < 7:
            self.display.set_pen(self.BLACK)
            self.display.clear()

            # Update Ship Position based on button pressed
            if self.button_a.read():
                self.ship.updatePosition("UP")
            elif self.button_b.read():
                self.ship.updatePosition("DOWN")

            self.display.set_pen(self.ship.pen)
            self.display.triangle(int(self.ship.x1), int(self.ship.y1), int(self.ship.x2), int(self.ship.y2), int(self.ship.x3), int(self.ship.y3))

            # Updating ball position
            for ball in self.balls:
                # Check for collision before changing to a new position
                if self.ship.collision(ball):
                        ball.x = 190
                        ball.y = 70
                ball.updatePosition()
                self.display.set_pen(ball.pen)
                self.display.circle(int(ball.x), int(ball.y), int(ball.r))

            # Check game status, wether we win or loose
            if self.ship.life <= 0:
                self.displayFinishMessage("Game Over")
                self.restartGame()
                continue
            elif self.ship.score >= 7:
                self.displayFinishMessage("You Win!")
                break

            # draws a white background for the text
            self.display.set_pen(self.WHITE)
            self.display.rectangle(140, 1, 100, 25)

            # writes the reading as text in the white rectangle
            self.display.set_pen(self.BLACK)
            self.display.text("Ship:{:}".format(self.ship.life), 143, 3, 0, 3)

            # time to update the display
            self.display.update()

            # waits for 5 seconds
            time.sleep(0)
