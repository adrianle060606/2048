
import pygame 
import constants
import random
import copy
import time
import math

# comment at the start of each method a description
# use name mangling to encapsulate code
# use inheritance
# game manager class

class gameManager():
    def __init__(self):
        pygame.init()
        self.in_menu = True
        self.exit = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) 
        self.board = Board(self.screen)
        
        pygame.display.set_caption("My Board") 

    def run(self):
        while not self.exit:
            
            
            if self.in_menu:

                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.exit = True

                #draw background
                self.screen.fill(constants.BACKGROUND_WHITE)

                #draw heading
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 100)
                text = font.render("2048", True, constants.TEXT_GREY)
                textRect = text.get_rect()
                textRect.center = (350, 100)
                self.screen.blit(text, textRect)

                #draw play button
                pygame.draw.rect(self.screen, constants.TILE_COLOURS[11], pygame.Rect(constants.PLAY_BTN), 0, 5)
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 30)
                text = font.render("Play", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (0.5*(2*constants.PLAY_BTN[0] + constants.PLAY_BTN[2]), 0.5*(2*constants.PLAY_BTN[1] + constants.PLAY_BTN[3]))
                self.screen.blit(text, textRect)

                #draw help button
                pygame.draw.rect(self.screen, constants.TILE_COLOURS[11], pygame.Rect((365, 400, 65, 65)), 0, 5)
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 30)
                text = font.render("Play", True, constants.WHITE)
                textRect = text.get_rect()
                #textRect.center = (0.5*(2*constants.PLAY_BTN[0] + constants.PLAY_BTN[2]), 0.5*(2*constants.PLAY_BTN[1] + constants.PLAY_BTN[3]))
                self.screen.blit(text, textRect)

            else:
                
                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.exit = True
                    elif event.type == pygame.KEYDOWN and not self.board.in_animation:
                        self.board.handle_keys(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.board.handle_click(pygame.mouse.get_pos())
                self.board.in_keydown = False
                
                #draw background
                self.screen.fill(constants.BACKGROUND_WHITE)
                pygame.draw.rect(self.screen, constants.BACKGROUND_GREY, pygame.Rect((constants.X_OFFSET - constants.GRID_MARGIN, constants.Y_OFFSET - constants.GRID_MARGIN, constants.TILES_ACROSS*constants.TILE_WIDTH + constants.GRID_MARGIN * 2, constants.TILES_ACROSS*constants.TILE_WIDTH  + constants.GRID_MARGIN * 2)))

                #draw heading
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', constants.HEADING_SIZE)
                text = font.render("2048", True, constants.TEXT_GREY)
                textRect = text.get_rect()
                textRect.center = constants.HEADING_POS
                self.screen.blit(text, textRect)

                #draw score menu
                pygame.draw.rect(self.screen, constants.BACKGROUND_GREY, pygame.Rect((400, 50, 100, 50)))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 20)
                text = font.render("Score:", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (450, 60)
                self.screen.blit(text, textRect)

                text = font.render(str(self.board.score), True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (450, 80)
                self.screen.blit(text, textRect)
                
                #draw restart button
                pygame.draw.rect(self.screen, constants.BROWN, pygame.Rect(constants.RESTART_BUTTON_POSITION))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 20)
                text = font.render("Restart", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (460, 155)
                self.screen.blit(text, textRect)



                #draw board and tiles
                self.board.draw(self.screen)
                self.board.animate_tiles()
                

            pygame.display.update()
            self.clock.tick(40)

class Board(object):
    def __init__(self, surface):
        # 0 --> empty, 1 --> 2, 2 --> 4, 3 --> 8 etc.
        self.state = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.new_piece()
        self.new_piece()
        self.score = 0
        self.in_keydown = False
        self.surface = surface
        self.in_animation = False
        self.animations = []

    def move(self, direction):

        valid_move = False
        x_range = None
        y_range = None

        animations = []
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
                                self.score += 2**abs(tile_value)

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
                            
                            animations.append((prev_x_target, prev_y_target))
                            
                            init_pos = (init_pos[0] * constants.TILE_WIDTH, init_pos[1] * constants.TILE_WIDTH)
                            final_pos = (abs(prev_x_target) * constants.TILE_WIDTH, abs(prev_y_target) * constants.TILE_WIDTH)

                            # check if target block is stationary
                            target_animated = False
                            if init_tile_value == abs(tile_value):
                                target_animated = True
                            else:
                                for animation in self.animations:
                                    if animation["final_pos"] == final_pos:
                                        target_animated = True
                            
                            if not target_animated:
                                self.add_animation(final_pos, final_pos, init_tile_value, init_tile_value, (0,0))

                            self.add_animation(init_pos, final_pos, init_tile_value, abs(tile_value), direction)

        # add 100 to the animations so that they aren't rendered normally
        for animation in animations:
            self.temp_state[animation[1]][animation[0]] += 100

        #copy the state into the temp state
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                self.state[y][x] = abs(self.temp_state[y][x])
        
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
            self.in_animation = True
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
            self.draw_tile(animation["current_pos"][0], animation["current_pos"][1], str(2**animation["init_tile_value"]))
            self.state[animation["final_pos"][1] // constants.TILE_WIDTH][animation["final_pos"][0] // constants.TILE_WIDTH] = animation["final_tile_value"]



        if len(self.animations) == 0:
            if self.in_animation:
                self.in_animation = False
                self.new_piece()

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

    def draw(self, surface):
        
        
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if self.state[y][x] != 0 and self.state[y][x] <= 50:
                    self.draw_tile(constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, str(2 ** self.state[y][x]))
                else:
                    pygame.draw.rect(surface, constants.TILE_COLOURS[0], pygame.Rect((constants.TILE_WIDTH * x + constants.X_OFFSET, constants.TILE_WIDTH * y + constants.Y_OFFSET, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))

    def draw_tile(self, x, y, tile_value):
        
        tile_num = math.log2(int(tile_value))
        font_colour = None
        if tile_num <= 2:
            font_colour = constants.TEXT_GREY
        else:
            font_colour = constants.WHITE

        pygame.draw.rect(self.surface, constants.TILE_COLOURS[tile_num], pygame.Rect((x + constants.X_OFFSET, y + constants.Y_OFFSET, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))
        font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', constants.TILE_FONT_SIZE)
        text = font.render(tile_value, True, font_colour)
        textRect = text.get_rect()
        textRect.center = (x + constants.TILE_WIDTH // 2 + constants.X_OFFSET, y + constants.TILE_WIDTH // 2 + constants.Y_OFFSET)
        self.surface.blit(text, textRect)
    
    def handle_keys(self, event):
        if event.key == pygame.K_LEFT:
            self.move((-1, 0))
            self.in_keydown = True
        elif event.key == pygame.K_RIGHT:
            self.move((1, 0))
            self.in_keydown = True
        elif event.key == pygame.K_DOWN:
            self.move((0, 1))
            self.in_keydown = True
        elif event.key == pygame.K_UP:
            self.move((0, -1))
            self.in_keydown = True
    
    def handle_click(self, pos):
        #restart button
        rbtn = constants.RESTART_BUTTON_POSITION
        if pos[0] >= rbtn[0] and pos[0] <= rbtn[0] + rbtn[2] and pos[1] >= rbtn[1] and pos[1] <= rbtn[1] + rbtn[3]:
            self.restart()

    def restart(self):
        self.__init__(self.surface)

game = gameManager()
game.run()

            
        
        