# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import math
import pygame
import random
import sys

from pygame.locals import *

FPS = 4
WINDOWWIDTH = 1400
WINDOWHEIGHT = 720
CELLSIZE = 20
RADIUS = math.floor(CELLSIZE / 2.5)
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
BGCOLOR = BLACK



UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy Is a Good Game!')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

#created a class called worm for two player mode
class worm:
    # Set a random start point
    def __init__(self):
        self.startx = random.randint(5, CELLWIDTH - 6)
        self.starty = random.randint(5, CELLHEIGHT - 6)
        self.wormCoords = [{'x': self.startx, 'y': self.starty},
                           {'x': self.startx - 1, 'y': self.starty},
                           {'x': self.startx - 2, 'y': self.starty},
                           {'x': self.startx - 3, 'y': self.starty},
                           {'x': self.startx - 4, 'y': self.starty},
                           {'x': self.startx - 5, 'y': self.starty},
                           {'x': self.startx - 6, 'y': self.starty}]
        self.direction = RIGHT

    def update(self):
        # move the worm by adding a segment in the direction it is moving
        if self.direction == UP:
            newHead = {'x': self.wormCoords[HEAD]['x'], 'y': self.wormCoords[HEAD]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.wormCoords[HEAD]['x'], 'y': self.wormCoords[HEAD]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.wormCoords[HEAD]['x'] - 1, 'y': self.wormCoords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.wormCoords[HEAD]['x'] + 1, 'y': self.wormCoords[HEAD]['y']}
        self.wormCoords.insert(0, newHead)  # have already removed the last segment

    def fire(self):
            return True


class shot:
    def __init__(self, direction, coord):
        self.direction = direction
        self.coords = [coord]
        if self.direction == UP:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.coords[HEAD]['x'] - 1, 'y': self.coords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coords[HEAD]['x'] + 1, 'y': self.coords[HEAD]['y']}
        self.coords.insert(0, newHead)  # have already removed the last segment


    def update(self):
        if self.direction == UP:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] - 2}
        elif self.direction == DOWN:
            newHead = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] + 2}
        elif self.direction == LEFT:
            newHead = {'x': self.coords[HEAD]['x'] - 2, 'y': self.coords[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coords[HEAD]['x'] + 2, 'y': self.coords[HEAD]['y']}
        self.coords.insert(0, newHead)  # have already removed the last segment
        del self.coords[-1]  # remove projectile's tail segment


def runGame():
    # Set a random start point.
    Worm1 = worm()
    Worm2 = worm()
    shots = []
    stones = []


    # Start the apples in a random place.
    apple1 = getRandomLocation()
    apple2 = getRandomLocation()
    apple3 = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key in [K_KP2, K_KP4, K_KP6, K_KP8]:
                    if (event.key == K_KP4) and Worm1.direction != RIGHT:
                        Worm1.direction = LEFT
                    elif (event.key == K_KP6) and Worm1.direction != LEFT:
                        Worm1.direction = RIGHT
                    elif (event.key == K_KP8) and Worm1.direction != DOWN:
                        Worm1.direction = UP
                    elif (event.key == K_KP2) and Worm1.direction != UP:
                        Worm1.direction = DOWN

                    if (event.key == K_KP4) and Worm2.direction != RIGHT:
                        Worm2.direction = LEFT
                    elif (event.key == K_KP6) and Worm2.direction != LEFT:
                        Worm2.direction = RIGHT
                    elif (event.key == K_KP8) and Worm2.direction != DOWN:
                        Worm2.direction = UP
                    elif (event.key == K_KP2) and Worm2.direction != UP:
                        Worm2.direction = DOWN
                else:
                    if (event.key == K_LEFT) and Worm1.direction != RIGHT:
                        Worm1.direction = LEFT
                    elif (event.key == K_RIGHT) and Worm1.direction != LEFT:
                        Worm1.direction = RIGHT
                    elif (event.key == K_UP) and Worm1.direction != DOWN:
                        Worm1.direction = UP
                    elif (event.key == K_DOWN) and Worm1.direction != UP:
                        Worm1.direction = DOWN
                    elif event.key == K_a and Worm2.direction != RIGHT:
                        Worm2.direction = LEFT
                    elif event.key == K_d and Worm2.direction != LEFT:
                        Worm2.direction = RIGHT
                    elif event.key == K_w and Worm2.direction != DOWN:
                        Worm2.direction = UP
                    elif event.key == K_s and Worm2.direction != UP:
                        Worm2.direction = DOWN
                    elif event.key == K_RALT:
                        Stone = shot(Worm1.direction, Worm1.wormCoords[HEAD])
                        shots.append(Stone)
                    elif event.key == K_LALT:
                        Stone = shot(Worm2.direction, Worm2.wormCoords[HEAD])
                        shots.append(Stone)
                    elif event.key == K_ESCAPE:
                        terminate()

        for projectile in shots:
            if projectile.coords[HEAD]['x'] == -1 or projectile.coords[HEAD]['x'] == CELLWIDTH or projectile.coords[HEAD]['y'] == -1 or projectile.coords[HEAD]['y'] == CELLHEIGHT:
                shots.remove(projectile)
            for w in [Worm1, Worm2]:
                for wormCoordinate in w.wormCoords:
                    if projectile.coords[HEAD]['x'] == wormCoordinate['x'] and projectile.coords[HEAD]['y'] == wormCoordinate['y']:
                        shots.remove(projectile)
                        stones.extend(w.wormCoords[w.wormCoords.index(wormCoordinate):])
                        del w.wormCoords[w.wormCoords.index(wormCoordinate):]
            projectile.update()

        for w in [Worm1, Worm2]:
            # check if the worm has hit itself or the edge
            if w.wormCoords[HEAD]['x'] == -1 or w.wormCoords[HEAD]['x'] == CELLWIDTH or w.wormCoords[HEAD]['y'] == -1 or w.wormCoords[HEAD]['y'] == CELLHEIGHT:
                return  # game over
            for projectile in stones:
                if projectile['x'] == w.wormCoords[HEAD]['x'] and projectile['y'] == w.wormCoords[HEAD]['y']:
                    return  # game over
            for wormBody in Worm2.wormCoords[1:]:
                if wormBody['x'] == w.wormCoords[HEAD]['x'] and wormBody['y'] == w.wormCoords[HEAD]['y']:
                    return  # game over
            for wormBody in Worm1.wormCoords[1:]:
                if wormBody['x'] == w.wormCoords[HEAD]['x'] and wormBody['y'] == w.wormCoords[HEAD]['y']:
                    return  # game over
            if w.wormCoords[HEAD]['x'] == apple1['x'] and w.wormCoords[HEAD]['y'] == apple1['y']:
                apple1 = getRandomLocation()  # set a new apple1 somewhere
            elif w.wormCoords[HEAD]['x'] == apple2['x'] and w.wormCoords[HEAD]['y'] == apple2['y']:
                apple2 = getRandomLocation()  # set a new apple2 somewhere
            elif w.wormCoords[HEAD]['x'] == apple3['x'] and w.wormCoords[HEAD]['y'] == apple3['y']:
                apple3 = getRandomLocation()  # set a new apple3 somewhere
            else:
                del w.wormCoords[-1]  # remove wrm.s tail segment
            w.update()

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

        drawWorm(Worm1.wormCoords, DARKGREEN, BLUE)
        drawWorm(Worm2.wormCoords, GREEN, YELLOW)
        drawWorm(stones, DARKGRAY, WHITE)
        drawApple(apple1)
        drawApple(apple2)
        drawApple(apple3)

        for projectile in shots:
            drawShot(projectile.coords[HEAD])

        drawScore(len(Worm1.wormCoords) - 7, WINDOWWIDTH - 5)
        drawScore(len(Worm2.wormCoords) - 7, 85)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy', True, RED, BLACK)
    titleSurf2 = titleFont.render('The Game!', True, DARKGRAY)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (math.floor(WINDOWWIDTH / 2), math.floor(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (math.floor(WINDOWWIDTH / 2), 10)
    overRect.midtop = (math.floor(WINDOWWIDTH / 2), gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score, offset):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - offset, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, innerColor, outerColor):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, outerColor, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, innerColor, wormInnerSegmentRect)

def drawShot(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    shotRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, WHITE, shotRect)

def drawApple(coord):
    xcenter = coord['x'] * CELLSIZE + math.floor(CELLSIZE / 2)
    ycenter = coord['y'] * CELLSIZE + math.floor(CELLSIZE / 2)
    pygame.draw.circle(DISPLAYSURF, RED, (xcenter, ycenter), RADIUS)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
