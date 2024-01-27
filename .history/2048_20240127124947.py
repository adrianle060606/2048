
import pygame 
import constants
pygame.init() 
  
# CREATING CANVAS 
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) 
  
#colours

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
grey = (63, 63, 74)

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
clock = pygame.time.Clock()
exit = False

class Board(object):
    def __init__(self):
        # 0 --> empty, 1 --> 2, 2 --> 4, 3 --> 8 etc.
        self.state = [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]]
        self.rect = pygame.rect.Rect((64, 54, 16, 16))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT]:
           self.rect.move_ip(-1, 0)
        if key[pygame.K_RIGHT]:
           self.rect.move_ip(1, 0)
        if key[pygame.K_UP]:
           self.rect.move_ip(0, -1)
        if key[pygame.K_DOWN]:
           self.rect.move_ip(0, 1)

    def draw(self, surface):
        font = pygame.font.Font('freesansbold.ttf', constants.TILE_FONT_SIZE)

        
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if self.state[y][x] != 0:
                    pygame.draw.rect(surface, (0, 0, 128), pygame.Rect((constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))
                    text = font.render(str(2 ** self.state[y][x]), True, green, blue)
                    textRect = text.get_rect()
                    textRect.center = (x * constants.TILE_WIDTH + constants.TILE_WIDTH // 2, y * constants.TILE_WIDTH + constants.TILE_WIDTH // 2)
                    screen.blit(text, textRect)
                else:
                    pygame.draw.rect(surface, grey, pygame.Rect((constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))


board = Board()

while not exit:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    
    screen.fill((255, 255, 255))
    board.draw(screen)
    board.handle_keys()
    pygame.display.update()
    clock.tick(40)