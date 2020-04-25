import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Pixel:
    def __init__(self, screen, x, y, size):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.color = BLACK
        self.rect = pygame.Rect(x*size, y*size, size, size)
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    def live(self):
        nextGen = Pixel(self.screen, self.x, self.y, self.size)
        nextGen.color = WHITE
        return nextGen
    def die(self):
        nextGen = Pixel(self.screen, self.x, self.y, self.size)
        nextGen.color = BLACK
        return nextGen
    def isAlive(self):
        return self.color == WHITE