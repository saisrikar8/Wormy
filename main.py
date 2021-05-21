# Wormy (a Nibbles clone)

import random, pygame, sys
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Colors  R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (120, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
DARKERGRAY = (2, 2, 2)
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
	pygame.display.set_caption('Wormy')

	while (True):
		showStartScreen()
		runGame()
		showGameOverScreen()


def runGame():
		score = 0
		# Set a random start point.
		startx = random.randint(5, CELLWIDTH - 6)
		starty = random.randint(5, CELLHEIGHT - 6)

		# Direction on start.
		xCoordinate = 0
		yCoordinate = 0
		randomDirection = random.randint(1,4)
		# HINT: CHECK THE DIRECTION BASED ON RANDOM NUMBER
		if (randomDirection == 1):
			randomDirection = UP
			yCoordinate = 1
		elif (randomDirection == 2):
				randomDirection = DOWN
				yCoordinate = -1
		elif (randomDirection == 3):
				randomDirection = RIGHT
				xCoordinate = 1
		elif (randomDirection == 4):
				randomDirection = LEFT
				xCoordinate = -1

		wormCoords = [{'x': startx, 'y': starty},
									{'x': startx - xCoordinate, 'y': starty + yCoordinate},
									{'x': startx - xCoordinate * 2, 'y': starty + yCoordinate * 2}]
		direction = randomDirection

		# Start the apple in a random place.
		apple = getRandomLocation()

		while True:  # main game loop
				for event in pygame.event.get():  # event handling loop
						if event.type == QUIT:
								terminate()
						elif event.type == KEYDOWN:
								# HINT: CHECK IF YOUR KEY IS WORKING, TURN LEFT or RIGHT
								if ((event.key == K_LEFT or event.key == K_a) and direction != RIGHT):
										direction = LEFT
								elif ((event.key == K_RIGHT or event.key == K_d) and direction != LEFT):
										direction = RIGHT
								elif ((event.key == K_UP or event.key == K_w) and direction != DOWN):
										direction = UP
								elif ((event.key == K_DOWN or event.key == K_s) and direction != UP):
										direction = DOWN
								elif (event.key == K_ESCAPE):
										terminate()

				# check if the worm has hit itself or the edge
				if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
						return  # game over
				for wormBody in wormCoords[1:]:
						if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
								return  # game over

				# check if worm has eaten an apply
				if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
					score += 1
					# don't remove worm's tail segment
					apple = getRandomLocation()  # set a new apple somewhere
				else:
						del wormCoords[-1]  # remove worm's tail segment

				# move the worm by adding a segment in the direction it is moving
				if direction == UP:
						newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
				elif direction == DOWN:
						newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
				elif direction == LEFT:
						newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
				elif direction == RIGHT:
						newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
				wormCoords.insert(0, newHead)
				DISPLAYSURF.fill(BGCOLOR)
				drawGrid()
				drawWorm(wormCoords)
				drawApple(apple)
				drawScore(score)
				pygame.display.update()
				FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, BLUE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:  # event is quit
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # event is escape key
                terminate()
            else:
                return event.key  # key found return with it
    # no quit or key events in queue so return None
    return None


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('Wormy', True, CYAN, DARKGRAY)
    titleSurf2 = titleFont.render('Wormy!', True, WHITE)

    degrees1 = 0
    degrees2 = 0

    # KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  # clear out event queue

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()
        # KRT 14/06/2012 rewrite event detection to deal with mouse use
        if checkForKeyPress():
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
		gameRect.midtop = (WINDOWWIDTH / 2, 10)
		overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

		DISPLAYSURF.blit(gameSurf, gameRect)
		DISPLAYSURF.blit(overSurf, overRect)
		drawPressKeyMsg()
		pygame.display.update()
		pygame.time.wait(500)
		# KRT 14/06/2012 rewrite event detection to deal with mouse use
		pygame.event.get()  # clear out event queue
		while True:
			if checkForKeyPress():
				return
			# KRT 12/06/2012 reduce processor loading in gameover screen.
			pygame.time.wait(100)


def drawScore(score):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 120, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
	for coord in wormCoords:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		# HINT: CAN YOU SEE ITS OUTTER BODY?
		pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		# HINT: CAN YOU SEE ITS INNER BODY?
		pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	# HINT: CAN YOU SEE THE APPLE?
	pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
	for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
		# HINT: CHANGE THE X-AXIS GRID LINE COLOR
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
	main()