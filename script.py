"""
#
# GameOfLife: A tribute to John Conway
#
"""
import sys, pygame
import Pixel
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
PIXEL_SIZE = 7
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

GLIDER_GUN = [(1, 25),
              (2, 23), (2, 25),
              (3, 13), (3, 14), (3, 21), (3, 22), (3, 35), (3, 36),
              (4, 12), (4, 16), (4, 21), (4, 22), (4, 35), (4, 36),
              (5, 1),  (5, 2),  (5, 11), (5, 17), (5, 21), (5, 22),
              (6, 1),  (6, 2),  (6, 11), (6, 15), (6, 17), (6, 18), (6, 23), (6, 25),
              (7, 11), (7, 17), (7, 25),
              (8, 12), (8, 16),
              (9, 13), (9, 14)]

def user_pick(world):
    # mouse event tracker to color every pixel pressed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: running = False
            elif pygame.mouse.get_pressed()[0] == 1:
                x, y = ((int(pygame.mouse.get_pos()[0] / PIXEL_SIZE), int(pygame.mouse.get_pos()[1] / PIXEL_SIZE)))
                world[y][x].color = WHITE
                world[y][x].draw()
                pygame.display.update()
                
# Create pixel world
def init():
    SCREEN.fill(BLACK)
    pygame.display.update()
    world = []
    for y in range(int(SCREEN_HEIGHT / PIXEL_SIZE)):
        row = []
        for x in range(int(SCREEN_WIDTH / PIXEL_SIZE)):
            pixel = Pixel.Pixel(SCREEN, x, y, PIXEL_SIZE)
            pixel.draw()
            row.append(pixel)
        world.append(row)

    user_pick(world) # let user pick starting state

    # Draw a glider gun
    # for (y, x) in GLIDER_GUN: world[y][x].color = WHITE

    return world

def countAliveNeighbours(world, x, y):
    try:
        neighbours = [world[y-1][x-1].isAlive(), world[y-1][x].isAlive(), world[y-1][x+1].isAlive(), world[y][x+1].isAlive(), world[y+1][x+1].isAlive(), world[y+1][x].isAlive(), world[y+1][x-1].isAlive(), world[y][x-1].isAlive()]
        return len([True for cond in neighbours if cond])
    except Exception:
        pass

# Prepare the next generation according to game rules
def play(world):
    nextGenPixels = []
    for row in world:
        next_gen_row = []
        for pixel in row:
            # assign each pixel's state by it's neighbours
            aliveNeighbours = countAliveNeighbours(world, pixel.x, pixel.y)
            if (not pixel.isAlive()) and aliveNeighbours == 3:
                next_gen_row.append(pixel.live())
            elif pixel.isAlive() and (aliveNeighbours > 3 or aliveNeighbours < 2):
                next_gen_row.append(pixel.die())
            else:
                next_gen_row.append(pixel)
        nextGenPixels.append(next_gen_row)
    return nextGenPixels

world = init()  # before running - create pixel world

while True:
    # handle exit states / restart
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == 'q'): sys.exit()
        elif event.type == pygame.KEYDOWN and event.unicode == 'r': world = init()

    nextG = play(world) # begin next generation
    
    # draw next generation
    for row in nextG:
        for pixel in row: pixel.draw()

    pygame.display.update() # display next generation
    world = nextG           # assign world to next generation
    CLOCK.tick(15)