
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
    def __init__(self, surface):
        # 0 --> empty, 1 --> 2, 2 --> 4, 3 --> 8 etc.
        self.state = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.new_piece()
        self.new_piece()
        self.surface = surface
        self.draw(surface)

        self.animations = []

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
                            init_pos = (init_pos[0] * constants.TILE_WIDTH, init_pos[1] * constants.TILE_WIDTH)
                            final_pos = (prev_x_target * constants.TILE_WIDTH, prev_y_target * constants.TILE_WIDTH)
                            self.add_animation(init_pos, final_pos, init_tile_value, abs(tile_value), direction)

        #copy the state into the temp state
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                self.state[y][x] = abs(self.temp_state[y][x])
        # finally add a new piece after moving
        if valid_move:
            self.new_piece()

    def add_animation(self, init_pos, final_pos, init_tile_value, final_tile_value, direction):
        # check which direction
        block_movement = 0
        if init_pos[1] == final_pos[1]:
            # if moving x
            block_movement = abs(final_pos[0]/constants.TILE_WIDTH - init_pos[0]/constants.TILE_WIDTH)
        else:
            # if moving y
            block_movement = abs(final_pos[1]/constants.TILE_WIDTH - init_pos[1]/constants.TILE_WIDTH)

        animation_speed = block_movement/4
        self.animations.append({"current_pos": init_pos, "final_pos": final_pos, "init_tile_value": init_tile_value, "final_tile_value": final_tile_value, "direction": direction, "animation_speed": animation_speed})

    def animate_tiles(self):
        
        animation_removal = []

        
        for animation in self.animations:

            animation_speed = constants.ANIMATION_SPEED * animation["animation_speed"]
            if animation["current_pos"][0] == animation["final_pos"][0] and animation["current_pos"][1] == animation["final_pos"][1]:
                animation_removal.append(animation)
            else:
                position_shift = (animation["direction"][0] * animation_speed, animation["direction"][1] * animation_speed)
                animation["current_pos"] = tuple(map(lambda i, j: i + j, animation["current_pos"], position_shift))
                
                # check if tile has reached it's final position

                self.draw_tile(animation["current_pos"][0], animation["current_pos"][1], str(2**animation["init_tile_value"]))

        for animation in animation_removal:
            self.animations.remove(animation)


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
        
        
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if self.state[y][x] != 0:
                    self.draw_tile(constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, str(2 ** self.state[y][x]))
                else:
                    pygame.draw.rect(surface, grey, pygame.Rect((constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))

    def draw_tile(self, x, y, tile_value):
        pygame.draw.rect(self.surface, (0, 0, 128), pygame.Rect((x, y, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))
        font = pygame.font.Font('freesansbold.ttf', constants.TILE_FONT_SIZE)
        text = font.render(tile_value, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (x + constants.TILE_WIDTH // 2, y + constants.TILE_WIDTH // 2)
        screen.blit(text, textRect)
        
screen.fill((255, 255, 255))
board = Board(screen)

while not exit:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
        elif event.type == pygame.KEYDOWN:
            board.handle_keys(event)

    
    screen.fill((255, 255, 255))
    
    board.draw(screen)

    board.animate_tiles()
    

    pygame.display.update()
    clock.tick(40)