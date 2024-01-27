
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

        valid_move = False
        x_range = None
        y_range = None

        #set move direction for x
        if direction[0] == 1:
            x_range = list(range(constants.TILES_ACROSS-1, -1, -1))
        else: 
            x_range = list(range(constants.TILES_ACROSS))
            

        #set move direction for y
        if direction[1] == 1:
            y_range = list(range(constants.TILES_ACROSS-1, -1, -1))
        else: 
            y_range = list(range(constants.TILES_ACROSS))

        self.temp_state = copy.deepcopy(self.state)
        for y in y_range:
            for x in x_range:
                tile_value = copy.deepcopy(self.temp_state[y][x])
                if tile_value != 0:
                    has_moved = False
                    init_pos = (x, y)
                    final_pos = (x, y)
                    init_tile_value = tile_value
                    finished_moving = False
                    y_target = y + direction[1]
                    x_target = x + direction[0]
                    prev_y_target = y
                    prev_x_target = x
                    combined = False
                    while not finished_moving:
                        
                        #collision detection

                        # y collision detection
                        if y_target > constants.TILES_ACROSS - 1 or y_target < 0 :
                            finished_moving = True
                        
                        # x collision detection
                        elif x_target > constants.TILES_ACROSS - 1 or x_target < 0:
                            finished_moving = True

                        # check if the tile doesn't clash with another tile
                        elif self.temp_state[y_target][x_target] != tile_value and self.temp_state[y_target][x_target] != 0:
                            finished_moving = True
                        elif self.temp_state[y_target][x_target] == tile_value and combined:
                            finished_moving = True

                        if not finished_moving:

                            # increase tile number by 1 if the same
                            if self.temp_state[y_target][x_target] == tile_value and not combined:
                                tile_value += 1
                                tile_value = -tile_value # mark an already converted block with a negative sign
                                combined = True

                            # if passes collision detection then move
                            valid_move = True
                            has_moved = True
                            self.temp_state[y_target][x_target] = tile_value
                            self.temp_state[prev_y_target][prev_x_target] = 0
                            prev_y_target = copy.deepcopy(y_target)
                            prev_x_target = copy.deepcopy(x_target)
                            y_target += direction[1]
                            x_target += direction[0]

                        elif has_moved:
                            final_pos = (prev_x_target, prev_y_target)
                            self.animate_tile(init_pos, final_pos, init_tile_value, abs(tile_value))

        #copy the state into the temp state
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                self.state[y][x] = abs(self.temp_state[y][x])
        # finally add a new piece after moving
        if valid_move:
            self.new_piece()

    def animate_tile(self, init_pos, final_pos, init_tile_value, final_tile_value):
        print(init_pos, final_pos, init_tile_value, final_tile_value)

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
            self.move((-1, 0))
        if event.key == pygame.K_RIGHT:
            self.move((1, 0))
        if event.key == pygame.K_DOWN:
            self.move((0, 1))
        if event.key == pygame.K_UP:
            self.move((0, -1))


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