import time

# Enemies displayed as balls
class Ball:
    def __init__(self, x, y, r, dx, dy, pen, displayWidth, displayHeight):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen
        self.displayWidth = displayWidth
        self.displayHeight= displayHeight
        
    def updatePosition(self):
        self.y += self.dy
        self.x += self.dx
        
        xmax = self.displayWidth - self.r
        xmin = self.r
        ymax = self.displayHeight - self.r
        ymin = self.r

        # Bounce effect once they reach the walls.
        if self.x < xmin or self.x > xmax:
            self.dx *= -1

        if self.y < ymin or self.y > ymax:
            self.dy *= -1
    
# Ship displayed as a triangle
class Triangle:
    def __init__(self, x1, y1, x2, y2, x3, y3, dy, life, pen):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.dy = dy
        self.life = life
        self.pen = pen
        self.score = 0
        
    def updatePosition(self, direction):
#         print("x = {} and y = {}".format(self.x1, self.y1))
#         print("Updating Position") 
        # Updating position based on the button that was pressed.
        if direction == "UP":
            self.y1 -= self.dy
            self.y2 -= self.dy
            self.y3 -= self.dy
        elif direction == "DOWN":
            self.y1 += self.dy
            self.y2 += self.dy
            self.y3 += self.dy
            
    def collision(self, ball):
        #print("x = {}, y = {}, r = {}".format(int(ball.x), int(ball.y), int(ball.r)))
        #print(self.y2)
        # Collision detection conditions.
        if (self.x1 < (ball.x - ball.r) and (self.x1 + 8) > (ball.x - ball.r)) and (self.y1 > (ball.y + ball.r) and self.y2 < (ball.y + ball.r)):
            self.life -= 1
            print("Collision happened Bottom Left")
            # waits for 5 seconds
            time.sleep(2)
            return True
            
        elif (self.x2 < (ball.x + ball.r) and (self.x2 + 8) > (ball.x + ball.r)) and (self.y1 > (ball.y + ball.r) and self.y2 < (ball.y + ball.r)):
            self.life -= 1
            print("Collision happened Bottom Right")
            time.sleep(2)
            return True
            
        elif (self.x2 < (ball.x - ball.r) and (self.x2 + 8) > (ball.x - ball.r)) and (self.y1 > (ball.y - ball.r) and self.y2 < (ball.y - ball.r)):
            self.life -= 1
            print("Collision happened Top Left")
            time.sleep(2)
            return True
            
        elif (self.x2 < (ball.x + ball.r) and (self.x2 + 8) > (ball.x + ball.r)) and (self.y1 > (ball.y - ball.r) and self.y2 < (ball.y - ball.r)):
            self.life -= 1
            print("Collision happened Top Right")
            time.sleep(2)
            return True

        # Resetting ball to the begining if we were able to avoid it
        elif self.x1 > (ball.x - ball.r):
            self.score += 1
            ball.x = 220
        return False
