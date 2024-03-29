import numpy as np
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

#colors
BLUE  = (0, 0, 125)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0,0,0,0)

#Constant
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
PLAN_BOMBS = 0
PLAN_IMG = 1
global FLAG_PLAYING
FLAG_PLAYING = 1

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Minesweeper")
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
gameovertxt = font.render('GAME OVER', True, RED)

image0 = pygame.image.load("0.png")
image1 = pygame.image.load("1.png")
image2 = pygame.image.load("2.png")
image3 = pygame.image.load("3.png")
image4 = pygame.image.load("4.png")
image5 = pygame.image.load("5.png")
image6 = pygame.image.load("6.png")
image7 = pygame.image.load("7.png")
image8 = pygame.image.load("8.png")
imageBomb = pygame.image.load("-1.png")
flagimg = pygame.image.load("flag.png")
noneimg = pygame.image.load("none.png")

#gameplaysettings
GRID_SIZE = 20
NUMBER_BOMBS = 50
SIZE_BOX = 30 # DO NOT CHANGE (or change png too)
board = np.zeros((2,GRID_SIZE, GRID_SIZE))


def main():
    initGame()
    
    while True:
        pygame.display.update()
        drawingGrid(GRID_SIZE,50,50)
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN and FLAG_PLAYING:
                if event.button == 1:
                    # LEFT
                    leftClicked(matchingCoord(pygame.mouse.get_pos(),50,50))
                elif event.button == 3:
                    # RIGHT 
                    rightClicked(matchingCoord(pygame.mouse.get_pos(),50,50))
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def initGame():
    for i in range(NUMBER_BOMBS):
        randindex = np.random.randint(0,board.size/2)
        board[PLAN_BOMBS,randindex//GRID_SIZE,randindex%GRID_SIZE] = -1

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            updateAround(x,y)
            

def updateAround(x, y):
    bombsHere = 0
    if (board[PLAN_BOMBS,x,y] == -1):
        return
    else:
        if x < GRID_SIZE-1 and board[PLAN_BOMBS,x+1,y] == -1:
            bombsHere += 1
        if x < GRID_SIZE-1 and y < GRID_SIZE-1 and board[PLAN_BOMBS,x+1,y+1] == -1:
            bombsHere += 1
        if y < GRID_SIZE-1 and board[PLAN_BOMBS,x,y+1] == -1:
            bombsHere += 1
        if x > 0 and y < GRID_SIZE-1 and board[PLAN_BOMBS,x-1,y+1] == -1:
            bombsHere += 1
        if x > 0 and board[PLAN_BOMBS,x-1,y] == -1:
            bombsHere += 1
        if x > 0 and y > 0 and board[PLAN_BOMBS,x-1,y-1] == -1:
            bombsHere += 1
        if y > 0 and board[PLAN_BOMBS,x,y-1] == -1:
            bombsHere += 1
        if y > 0 and x < GRID_SIZE-1 and board[PLAN_BOMBS,x+1,y-1] == -1:
            bombsHere += 1
        board[PLAN_BOMBS,x,y] = bombsHere
        
def drawingGrid(gridSize=20, offsetX = 0, offsetY = 0):
    #verical lines
    drawingBoard(offsetX, offsetY)
    for y in range(gridSize+1):
        pygame.draw.line(DISPLAYSURF, BLUE, (offsetX,offsetY+y*SIZE_BOX), (offsetX+SIZE_BOX*(gridSize),offsetY+y*SIZE_BOX))
    #horizontal lines
    for x in range(gridSize+1):
        pygame.draw.line(DISPLAYSURF, BLUE, (offsetX+x*SIZE_BOX,offsetY), (offsetX+x*SIZE_BOX,offsetY+SIZE_BOX*(gridSize)))

def drawingBoard(offsetX = 0, offsetY = 0):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):            
            match board[PLAN_BOMBS,x,y]:
                case 0:
                    imageToPrint = image0
                case 1:
                    imageToPrint = image1
                case 2:
                    imageToPrint = image2
                case 3:
                    imageToPrint = image3
                case 4:
                    imageToPrint = image4
                case 5:
                    imageToPrint = image5
                case 6:
                    imageToPrint = image6
                case 7:
                    imageToPrint = image7
                case 8:
                    imageToPrint = image8
                case -1:
                    imageToPrint = imageBomb
                case _:        
                    print("No matching to img")
            if board[PLAN_IMG,x,y] == 0:
                DISPLAYSURF.blit(noneimg, (offsetX+x*SIZE_BOX,offsetY+SIZE_BOX*y))
            elif board[PLAN_IMG,x,y] == 1:
                DISPLAYSURF.blit(imageToPrint, (offsetX+x*SIZE_BOX,offsetY+SIZE_BOX*y))
            elif board[PLAN_IMG,x,y] == 2:
                DISPLAYSURF.blit(flagimg, (offsetX+x*SIZE_BOX,offsetY+SIZE_BOX*y))


def matchingCoord(pos, offsetX, offsetY):
    x = (pos[0]-offsetX)//(SIZE_BOX)
    y = (pos[1]-offsetY)//(SIZE_BOX)
    return (x,y)

def leftClicked(coord):
    board[PLAN_IMG,coord[0],coord[1]] = 1
    if board[PLAN_BOMBS,coord[0],coord[1]] == -1:
        gameOver()
    else:
        # theres no bomb arround
        revealAround(coord)
 
def rightClicked(coord):
    if board[PLAN_IMG,coord[0],coord[1]] == 2:
        board[PLAN_IMG,coord[0],coord[1]] = 0
    elif board[PLAN_IMG,coord[0],coord[1]] == 0:
        board[PLAN_IMG,coord[0],coord[1]] = 2

def revealAround(coord):
    if (board[PLAN_BOMBS,coord[0],coord[1]] == 0):
        x = coord[0]
        y = coord[1]

        if x < GRID_SIZE-1 and board[PLAN_IMG,x+1,y] != 1:
            board[PLAN_IMG,x+1,y] = 1
            if board[PLAN_BOMBS,x+1,y] == 0:
                revealAround((x+1,y))
            
        if x < GRID_SIZE-1 and y < GRID_SIZE-1 and board[PLAN_IMG,x+1,y+1] != 1:
            board[PLAN_IMG,x+1,y+1] = 1
            if board[PLAN_BOMBS,x+1,y+1] == 0:
                revealAround((x+1,y+1))

        if y < GRID_SIZE-1 and board[PLAN_IMG,x,y+1] != 1:
            board[PLAN_IMG,x,y+1] = 1
            if board[PLAN_BOMBS,x,y+1] == 0:
                revealAround((x,y+1))

        if x > 0 and y < GRID_SIZE-1 and board[PLAN_IMG,x-1,y+1] != 1:
            board[PLAN_IMG,x-1,y+1] = 1
            if board[PLAN_BOMBS,x-1,y+1] == 0:
                revealAround((x-1,y+1))

        if x > 0 and board[PLAN_IMG,x-1,y] != 1:
            board[PLAN_IMG,x-1,y] = 1
            if board[PLAN_BOMBS,x-1,y] == 0:
                revealAround((x-1,y))

        if x > 0 and y > 0 and board[PLAN_IMG,x-1,y-1] != 1:
            board[PLAN_IMG,x-1,y-1] = 1
            if board[PLAN_BOMBS,x-1,y-1] == 0:
                revealAround((x-1,y-1))
            
        if y > 0  and board[PLAN_IMG,x,y-1] != 1:
            board[PLAN_IMG,x,y-1] = 1
            if board[PLAN_BOMBS,x,y-1] == 0:
                revealAround((x,y-1))

        if y > 0 and x < GRID_SIZE-1 and board[PLAN_IMG,x+1,y-1] != 1:
            board[PLAN_IMG,x+1,y-1] = 1
            if board[PLAN_BOMBS,x+1,y-1] == 0:
                revealAround((x+1,y-1))
    return 

def gameOver():
    global FLAG_PLAYING
    FLAG_PLAYING = 0
    # display every bombs
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[PLAN_BOMBS,x,y] == -1:
                board[PLAN_IMG,x,y] = 1


main()