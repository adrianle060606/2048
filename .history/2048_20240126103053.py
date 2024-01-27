# Example file showing a circle moving on screen
import pygame
import constants
from enum import Enum
import copy
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

class Direction(Enum):
    STATIC = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    

class Snake:
    def __init__(self, xStart, yStart, length):
        self.player_pos = pygame.Vector2(xStart, yStart)
        self.length = length
        self.tickCount = 0
        self.direction = Direction.EAST
        self.tail = [pygame.Vector2(xStart, yStart)]
        self.waitingOnIncrease = False
        self.score = 0
        self.running = True
    
    def InitiateTail(self):
        for item in range(1,self.length):
            self.tail.append(pygame.Vector2(self.tail[0].x-(item*constants.PIXEL_WIDTH), self.tail[0].y))
        

    def UpdateTail(self):
        if self.waitingOnIncrease:
            tempLastTail = self.tail[len(self.tail)-1]
        
        for item in range(len(self.tail)-1,0,-1):
            self.tail[item] = self.tail[item-1]
        
        self.tail[0] = copy.deepcopy(self.player_pos)
        if self.waitingOnIncrease:
            self.tail.append(copy.deepcopy(tempLastTail))
            self.waitingOnIncrease = False
            

    def CollisionDetection(self):
        #if in same position as apple
        if self.player_pos == apple1.player_pos:
            apple1.newPosition();
            self.waitingOnIncrease = True
            self.score+=1

        #if outside bounds
        if self.player_pos.x<0 or self.player_pos.x>constants.SCREEN_WIDTH or self.player_pos.y<0 or self.player_pos.y>constants.SCREEN_HEIGHT:
            GameOver()


def GameOver():
    #player1.running = False
    player1.direction = Direction.STATIC

class Apple:
    def __init__(self):
        #self.player_pos = pygame.Vector2(xStart, yStart)
        pass
    def newPosition(self):
        self.player_pos = pygame.Vector2(random.randint(0,constants.PIXELS_ACROSS-1)*constants.PIXEL_WIDTH, random.randint(0,constants.PIXELS_DOWN-1)*constants.PIXEL_WIDTH)



player1 = Snake(constants.X_START_CORD * constants.PIXEL_WIDTH, constants.Y_START_CORD * constants.PIXEL_WIDTH, 3)
player1.InitiateTail()
apple1 = Apple()
apple1.newPosition()

font = pygame.font.Font('freesansbold.ttf', 32)

 
# create a text surface object,
# on which text is drawn on it.
text = font.render(f"Score: {player1.score}", True, "green", "blue")
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.
textRect.center = (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/8)

while player1.running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.direction = Direction.NORTH
    elif keys[pygame.K_s]:
        player1.direction = Direction.SOUTH
    elif keys[pygame.K_a]:
        player1.direction = Direction.WEST
    elif keys[pygame.K_d]:
        player1.direction = Direction.EAST

    #move player 
    if player1.direction == Direction.NORTH:
        player1.player_pos.y -= constants.PIXEL_WIDTH
    elif player1.direction == Direction.SOUTH:
        player1.player_pos.y += constants.PIXEL_WIDTH
    elif player1.direction == Direction.WEST:
        player1.player_pos.x -= constants.PIXEL_WIDTH
    elif player1.direction == Direction.EAST:
        player1.player_pos.x += constants.PIXEL_WIDTH
    

    # move tail along
    player1.UpdateTail();

    #collision detection
    player1.CollisionDetection();

    #draw apple
    pygame.draw.rect(screen, constants.APPLE_COLOUR, pygame.Rect(apple1.player_pos.x, apple1.player_pos.y, constants.PIXEL_WIDTH, constants.PIXEL_WIDTH))

    #draw text
    text = font.render(f"Score: {player1.score}", True, "green", "blue")
    screen.blit(text, textRect)
    #draw head
    pygame.draw.rect(screen, "green", pygame.Rect(player1.player_pos.x, player1.player_pos.y, constants.PIXEL_WIDTH-1, constants.PIXEL_WIDTH-1))
    #draw tail
    for tailBlock in range(1,len(player1.tail)):
        pygame.draw.rect(screen, "green", pygame.Rect(player1.tail[tailBlock].x, player1.tail[tailBlock].y, constants.PIXEL_WIDTH-1, constants.PIXEL_WIDTH-1))
        #print(player1.tail[tailBlock],tailBlock)
    
    



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 5
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(8) / 1000

pygame.quit()
