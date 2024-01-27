
import pygame 
import constants
pygame.init() 
  
# CREATING CANVAS 
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) 
  
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
clock = pygame.time.Clock()
exit = False

class Player(object):
    def __init__(self):
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
        pygame.draw.rect(surface, (0, 0, 128), self.rect)

player = Player()
while not exit:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    
    screen.fill((255, 255, 255))
    player.draw(screen)
    player.handle_keys()
    pygame.display.update()
    clock.tick(40)