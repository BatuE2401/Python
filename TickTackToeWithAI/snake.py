from pygame import *
from pygame.locals import *
import sys
from random import *

BGCOL = (157,188,122)
BLACK = (0,0,0)
RED = (255,0,0)

class Space_Invaders:
    def __init__(self):
        self.screen = display.set_mode((640,480))
        self.screen.fill(BGCOL)

        self.snake_X = self.screen.get_width() / 2
        self.snake_Y = self.screen.get_height() / 2

        self.apple_X = randint(0, self.screen.get_width())
        self.apple_Y = randint(0, self.screen.get_height())

        self.snake = Rect(self.snake_X, self.snake_Y, 8, 8)
        self.apple = Rect(self.apple_X, self.apple_Y, 8, 8)

        draw.rect(self.screen, BLACK, self.snake)
        draw.rect(self.screen, RED, self.apple)

        self.direction = 1

    #def snake_update(self):
    #    self.snake_X += 5

    def apple_update(self):
        draw.rect(self.screen, RED, self.apple)
    def snake_update(self):
        draw.rect(self.screen, BLACK, self.snake)

    def run(self):
        while True:

            t0 = time.get_ticks()

            display.flip()

            self.apple_update()
            self.snake_update()

            for events in event.get():
                if events.type == QUIT: #Exits the game
                    sys.exit()

            #self.screen.blit(self.snake, (self.snake_X, self.snake_Y))

            t1 = time.get_ticks()
            time.wait(40 - (t1 - t0))



if __name__ == "__main__":
    Space_Invaders().run()
