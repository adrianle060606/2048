
import pygame 
import constants
import random
import copy
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
        self.state = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.new_piece()
        self.new_piece()

    def move(self, direction):

        x_range = None
        y_range = None

        #set move direction for x
        if direction[0] == -1:
            x_range = range(constants.TILES_ACROSS)
        else: 
            x_range = range(0, constants.TILES_ACROSS, -1)

        #set move direction for y
        if direction[1] == -1:
            y_range = range(constants.TILES_ACROSS)
        else: 
            y_range = range(0, constants.TILES_ACROSS, -1)

        for y in y_range:
            for x in x_range:
                tile_value = copy.deepcopy(self.state[y][x])
                if tile_value != 0:
                    finished_moving = False
                    y_target = y + direction[1]
                    x_target = x + direction[0]
                    prev_y_target = y
                    prev_x_target = x
                    while not finished_moving:
                        
                        #collision detection

                        # y collision detection
                        if y_target > constants.TILES_ACROSS - 1 or y_target < 0:
                            finished_moving = True
                        
                        # x collision detection
                        if x_target > constants.TILES_ACROSS - 1 or x_target < 0:
                            finished_moving = True

                        if not finished_moving:
                            # if passes collision detection then move

                            self.state[y_target][x_target] = tile_value
                            self.state[prev_y_target][prev_x_target] = 0
                            prev_y_target = copy.deepcopy(y_target)
                            prev_x_target = copy.deepcopy(x_target)
                            y_target += direction[1]
                            x_target += direction[0]

    def new_piece(self):
        empty_indexes = []
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if self.state[y][x] == 0:
                    empty_indexes.append((x, y))

        if len(empty_indexes) > 0:
            selected_index = random.randint(0, len(empty_indexes)-1)

            # get random chance: 90% of a 2, 10% of a 4
            self.state[empty_indexes[selected_index][1]][empty_indexes[selected_index][0]] = self.tile_value() 

    def tile_value(self):
        roll = random.randint(0,10)
        if roll != 1:
            return 1
        else:
            return 2

    def handle_keys(self, event):
        if event.key == pygame.K_LEFT:
            location -= 1
        if event.key == pygame.K_RIGHT:
            location += 1
        if event.key == pygame.K_DOWN:
            location += 1
        if event.key == pygame.K_UP:
            self.move((0, -1))
            #self.new_piece()

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
        elif event.type == pygame.KEYDOWN:
            board.handle_keys(event)

    
    screen.fill((255, 255, 255))
    board.draw(screen)

    pygame.display.update()
    clock.tick(40)