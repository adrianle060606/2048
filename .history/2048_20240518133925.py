
import pygame 
import constants
import random
import copy
import time
import math
import csv

# make interactive tutorial
# disable saving game when game over
# add to death message to press restart to start new game
# add message that game will not automatically be saved by going home
# add warning that saving a game will override an old game
# add to the guide, make it interactable and include UI techniques such as searchable help

# documentation format:
# 1. author name
# 2. date
# 3. purpose of module
# 4. special notes
# 5. version history


class gameManager():
    def __init__(self):
        #Initialize the game manager.
        pygame.init()
        self.__in_menu = True
        self.__in_guide = False
        self.__exit = False
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) 
        self.__board = Board(self.__screen)
        self.__csv_file = "board.csv"
        self.__demo_file = "demo_board.csv"
        self.__instruction_num = 0
        #myimage = pygame.image.load("Assets/Images/arrow-forward.jpeg")
        #self.__imagerect = myimage.get_rect()
        #self.__new_img = pygame.transform.scale_by(myimage, (0.1, 0.1))
        
        pygame.display.set_caption("2048") 

    def run(self):
        #Main game loop which handles different states - main menu, guide, or main game
        while not self.__exit:
            
            
            if self.__in_menu:

                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.__exit = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_btns(pygame.mouse.get_pos())

                #draw background
                self.__screen.fill(constants.BACKGROUND_WHITE)

                #draw heading
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 100)
                text = font.render("2048", True, constants.TEXT_GREY)
                textRect = text.get_rect()
                textRect.center = (350, 120)
                self.__screen.blit(text, textRect)

                if not self.__in_guide:
                    #draw play button
                    self.draw_button(constants.PLAY_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Play")

                    #draw load button
                    self.draw_button(constants.LOAD_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Load Game")

                    #draw help button
                    self.draw_button(constants.HELP_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Guide")

                else:
                    font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 40)
                    self.__board.set_in_keydown(False)
                
                    if self.__board.get_saving():
                        self.__board.save(self.__csv_file)
                    if self.__board.get_save_delay() <= 0:
                        self.__board.set_save_colour(constants.WHITE)
                        self.__board.set_save_status("Save")
                    else:
                        self.__board.set_save_delay(self.__board.get_save_delay() - 1/constants.CLOCK_SPEED)

                    #draw background
                    self.__screen.fill(constants.BACKGROUND_WHITE)

                    font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 30)
                    text = font.render(f"{self.__board.get_score()}", True, constants.WHITE)

                    


                    
                    

                    if self.__instruction_num == 4:
                        #draw save button
                        self.draw_button((290, 325, 120, 40), constants.BROWN, 20, self.__board.get_save_colour(), self.__board.get_save_status())
                    elif self.__instruction_num == 5:
                        #draw load button
                        self.draw_button((260, 320, 180, 65), constants.TILE_COLOURS[11], 30, constants.WHITE, "Load Game")
                    else:
                        pass
                        #draw board and tiles
                        pygame.draw.rect(self.__screen, constants.BACKGROUND_GREY, pygame.Rect((self.__board.get_x_offset() - constants.GRID_MARGIN, self.__board.get_y_offset() - constants.GRID_MARGIN, constants.TILES_ACROSS*constants.TILE_WIDTH + constants.GRID_MARGIN * 2, constants.TILES_ACROSS*constants.TILE_WIDTH  + constants.GRID_MARGIN * 2)))
                        self.__board.draw(self.__screen)
                        self.__board.animate_tiles()
                        

                    #if gameover render gameover text
                    if self.__board.get_game_over():
                        font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 75)
                        text = font.render("Game Over", True, constants.TEXT_GREY)
                        textRect = text.get_rect()
                        textRect.center = (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 50)
                        self.__screen.blit(text, textRect)

                    #tutorial text
                    current_instructions = []
                    if "\n" in constants.INSTRUCTIONS[self.__instruction_num]:
                        current_instructions = constants.INSTRUCTIONS[self.__instruction_num].split("\n")
                    else:
                        current_instructions = [constants.INSTRUCTIONS[self.__instruction_num]]

                    for i, instruction in enumerate(current_instructions):
                        text = font.render(instruction, True, constants.TEXT_GREY)
                        textRect = text.get_rect()
                        textRect.center = (350, 590 + 50*i)
                        self.__screen.blit(text, textRect)

                    #next button
                    self.draw_button(constants.NEXT_BTN, constants.TILE_COLOURS[11], 20, constants.WHITE, "Next")
                    self.draw_button(constants.BACK_BTN, constants.TILE_COLOURS[11], 20, constants.WHITE, "Back")
                    #self.__screen.blit(self.__new_img, pygame.Rect(constants.NEXT_BTN[0] - 10, constants.NEXT_BTN[1] - 10,100,100))


            else:
                
                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.__exit = True
                    elif event.type == pygame.KEYDOWN and not self.__board.get_in_animation():
                        self.__board.handle_keys(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_btns(pygame.mouse.get_pos())
                self.__board.set_in_keydown(False)
                
                if self.__board.get_saving():
                    self.__board.save(self.__csv_file)
                if self.__board.get_save_delay() <= 0:
                    self.__board.set_save_colour(constants.WHITE)
                    self.__board.set_save_status("Save")
                else:
                    self.__board.set_save_delay(self.__board.get_save_delay() - 1/constants.CLOCK_SPEED)

                #draw background
                self.__screen.fill(constants.BACKGROUND_WHITE)
                pygame.draw.rect(self.__screen, constants.BACKGROUND_GREY, pygame.Rect((self.__board.get_x_offset() - constants.GRID_MARGIN, self.__board.get_y_offset() - constants.GRID_MARGIN, constants.TILES_ACROSS*constants.TILE_WIDTH + constants.GRID_MARGIN * 2, constants.TILES_ACROSS*constants.TILE_WIDTH  + constants.GRID_MARGIN * 2)))

                #draw heading
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', constants.HEADING_SIZE)
                text = font.render("2048", True, constants.TEXT_GREY)
                textRect = text.get_rect()
                textRect.center = constants.HEADING_POS
                self.__screen.blit(text, textRect)

                #draw score menu
                pygame.draw.rect(self.__screen, constants.BACKGROUND_GREY, pygame.Rect((350, 40, 100, 60)))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 20)
                text = font.render("Score:", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (400, 50)
                self.__screen.blit(text, textRect)

                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 25)
                text = font.render(f"{self.__board.get_score()}", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (400, 75)
                self.__screen.blit(text, textRect)

                #highscore menu
                pygame.draw.rect(self.__screen, constants.BACKGROUND_GREY, pygame.Rect((480, 40, 100, 60)))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 18)
                text = font.render("Highscore:", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (530, 50)
                self.__screen.blit(text, textRect)

                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 25)
                text = font.render(f"{self.__board.get_highscore()}", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (530, 75)
                self.__screen.blit(text, textRect)

                #draw restart button
                self.draw_button(constants.RESTART_BTN, constants.BROWN, 20, constants.WHITE, "Restart")

                #draw save button
                self.draw_button(constants.SAVE_BTN, constants.BROWN, 20, self.__board.get_save_colour(), self.__board.get_save_status())

                #draw home button
                self.draw_button(constants.HOME_BTN, constants.BROWN, 20, constants.WHITE, "Home")

                #draw board and tiles
                self.__board.draw(self.__screen)
                self.__board.animate_tiles()

                #if gameover render gameover text
                if self.__board.get_game_over():
                    font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 75)
                    text = font.render("Game Over", True, constants.TEXT_GREY)
                    textRect = text.get_rect()
                    textRect.center = (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 50)
                    self.__screen.blit(text, textRect)

                
                

            pygame.display.update()
            self.__clock.tick(constants.CLOCK_SPEED)

    def handle_btns(self, pos):
        # decides which buttons are pressed based on mouse pos
        
        if self.__in_menu: #menu buttons

            if self.__in_guide:
                btn = constants.NEXT_BTN
                if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                    self.next_btn()

                btn = constants.BACK_BTN
                if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                    self.back_btn()
            else:

                btn = constants.PLAY_BTN
                if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                    self.new_game()
                
                btn = constants.LOAD_BTN
                if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                    self.load_game()

                btn = constants.HELP_BTN
                if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                    self.help_menu()
                

            



        else: #game buttons

            #home button
            btn = constants.HOME_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.__in_menu = True

            #save button
            btn = constants.SAVE_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.__board.save(self.__csv_file)

            #restart button
            btn = constants.RESTART_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.__board.restart()



    def new_game(self):
        # starts new game
        self.__board.restart()
        self.__in_menu = False

    def load_game(self):
        # loads saved game
        self.__board.restart()
        self.__in_menu = False
        self.__board.load_file(self.__csv_file)


    def help_menu(self):
        #Opens the guide
        self.__in_guide = True
        self.__instruction_num = 0
        self.__board.restart()
        self.__board.set_y_offset(50)
        self.__board.load_file(self.__demo_file)

    def next_btn(self):
        if self.__instruction_num == 1:
            self.__board.move((0, -1))
        elif self.__instruction_num == 2:
            self.__board.move((-1, 0))
        elif self.__instruction_num == 5:
            self.__board.set_state([[7,6,4,2], [3,8,1,6], [4,1,2,4], [5,2,9,3]])
        elif self.__instruction_num == 6:
            self.__board.set_state([[10,0,0,10], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
        elif self.__instruction_num == 7:
            self.__board.move((-1,0))
        elif self.__instruction_num == 9:
            self.__in_guide = False
        self.__instruction_num += 1

    def back_btn(self):
        if self.__instruction_num == 0:
            self.__in_guide = False
        elif self.__instruction_num == 1:
            self.__board.move((0, -1))
        elif self.__instruction_num == 2:
            self.__board.move((-1, 0))
        elif self.__instruction_num == 5:
            self.__board.set_state([[7,6,4,2], [3,8,1,6], [4,1,2,4], [5,2,9,3]])
        elif self.__instruction_num == 6:
            self.__board.set_state([[10,0,0,10], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
        elif self.__instruction_num == 7:
            self.__board.move((-1,0))
        elif self.__instruction_num == 8:
            self.__in_guide = False
        self.__instruction_num += 1


    def draw_button(self, btn_position, btn_colour, font_size, font_colour, text_content):
        # generic subroutine for drawing a button
        pygame.draw.rect(self.__screen, btn_colour, pygame.Rect(btn_position), 0, 5)
        font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', font_size)
        text = font.render(text_content, True, font_colour)
        textRect = text.get_rect()
        textRect.center = (0.5*(2*btn_position[0] + btn_position[2]), 0.5*(2*btn_position[1] + btn_position[3]))
        self.__screen.blit(text, textRect)

class Board(object):
    def __init__(self, surface):
        # Initialize the game board.
        #for the game board state: 0 = empty, 1 = 2 tile, 2 = 4 tile, 3 = 8 tile etc.
        self.__state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.__x_offset = 105
        self.__y_offset = 220
        self.__in_keydown = False
        self.__surface = surface
        self.__in_animation = False
        self.__animations = []
        self.__saving = False
        self.__save_status = "Save"
        self.__save_delay = 0
        self.__game_over = False
        self.__score = 0
        self.__save_colour = constants.WHITE
        self.__highscore = self.read_highscore()
        self.new_piece()
        self.new_piece()

    # Getters and setters for each attribute
    def get_state(self):
        # Get the current state of the game board.
        return self.__state

    def set_state(self, state):
        # Set the state of the game board.
        self.__state = state

    def get_in_keydown(self):
        # Get the state of keydown.
        return self.__in_keydown

    def set_in_keydown(self, in_keydown):
        # Set the state of keydown.
        self.__in_keydown = in_keydown

    def get_surface(self):
        # Get the surface object.
        return self.__surface

    def set_surface(self, surface):
        # Set the surface object.
        self.__surface = surface

    def get_in_animation(self):
        # Get the animation state.
        return self.__in_animation

    def set_in_animation(self, in_animation):
        # Set the animation state.
        self.__in_animation = in_animation

    def get_animations(self):
        # Get the list of animations.
        return self.__animations

    def set_animations(self, animations):
        # Set the list of animations.
        self.__animations = animations

    def get_saving(self):
        # Get the saving state.
        return self.__saving

    def set_saving(self, saving):
        # Set the saving state.
        self.__saving = saving

    def get_save_status(self):
        # Get the save status.
        return self.__save_status

    def set_save_status(self, save_status):
        # Set the save status.
        self.__save_status = save_status

    def get_save_delay(self):
        # Get the save delay.
        return self.__save_delay

    def set_save_delay(self, save_delay):
        # Set the save delay.
        self.__save_delay = save_delay

    def get_game_over(self):
        # Get the game over state.
        return self.__game_over

    def set_game_over(self, game_over):
        # Set the game over state.
        self.__game_over = game_over

    def get_score(self):
        # Get the current score.
        return self.__score

    def set_score(self, score):
        # Set the current score.
        self.__score = score

    def get_save_colour(self):
        # Get the save colour.
        return self.__save_colour

    def set_save_colour(self, save_colour):
        # Set the save colour.
        self.__save_colour = save_colour

    def get_x_offset(self):
        # Get the x offset.
        return self.__x_offset

    def set_x_offset(self, x_offset):
        # Set the x offset.
        self.__x_offset = x_offset

    def get_y_offset(self):
        # Get the y offset.
        return self.__y_offset

    def set_y_offset(self, y_offset):
        # Set the y offset.
        self.__y_offset = y_offset

    def get_highscore(self):
        # Get the highscore.
        return self.__highscore

    def set_highscore(self, highscore):
        # Set the highscore.
        self.__highscore = highscore

    def move(self, direction):
        # moves tiles in specified direction while checking for collsion
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

        self.temp_state = copy.deepcopy(self.__state)
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
                                self.__score += 2**abs(tile_value)
                                self.update_highscore()

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
                            self.__in_animation = True

                            
                            init_pos = (init_pos[0] * constants.TILE_WIDTH, init_pos[1] * constants.TILE_WIDTH)
                            final_pos = (abs(prev_x_target) * constants.TILE_WIDTH, abs(prev_y_target) * constants.TILE_WIDTH)

                            # check if target block is stationary
                            target_animated = False
                            if init_tile_value == abs(tile_value):
                                target_animated = True
                            else:
                                for animation in self.__animations:
                                    if animation["final_pos"] == final_pos:
                                        target_animated = True
                            
                            if not target_animated:
                                self.add_animation(final_pos, final_pos, init_tile_value, init_tile_value, (0,0))

                            self.add_animation(init_pos, final_pos, init_tile_value, abs(tile_value), direction)

        # add 100 to the animations so that they aren't rendered normally
        for animation in animations:
            self.temp_state[animation[1]][animation[0]] += 100

        #copy the state into the temp state
        for y in range(len(self.__state)):
            for x in range(len(self.__state[y])):
                self.__state[y][x] = abs(self.temp_state[y][x])
        
    def add_animation(self, init_pos, final_pos, init_tile_value, final_tile_value, direction):
        #adds tile to queue of animations with a specific start and end position and tile value
        
        # check which direction
        block_movement = 0
        if init_pos[1] == final_pos[1]:
            # if moving x
            block_movement = abs(final_pos[0]/constants.TILE_WIDTH - init_pos[0]/constants.TILE_WIDTH)
        else:
            # if moving y
            block_movement = abs(final_pos[1]/constants.TILE_WIDTH - init_pos[1]/constants.TILE_WIDTH)

        animation_speed = block_movement/4
        self.__animations.append({"current_pos": init_pos, "final_pos": final_pos, "init_tile_value": init_tile_value, "final_tile_value": final_tile_value, "direction": direction, "animation_speed": animation_speed})

    def animate_tiles(self):
        # animates moving tiles
        
        animation_removal = []

        
        for animation in self.__animations:
            self.__in_animation = True
            animation_speed = constants.ANIMATION_SPEED * animation["animation_speed"]
            if animation["current_pos"][0] == animation["final_pos"][0] and animation["current_pos"][1] == animation["final_pos"][1]:
                animation_removal.append(animation)
            else:
                position_shift = (animation["direction"][0] * animation_speed, animation["direction"][1] * animation_speed)
                animation["current_pos"] = tuple(map(lambda i, j: i + j, animation["current_pos"], position_shift))
                
                # check if tile has reached it's final position

                self.draw_tile(animation["current_pos"][0], animation["current_pos"][1], str(2**animation["init_tile_value"]))

        for animation in animation_removal:
            self.__animations.remove(animation)
            self.draw_tile(animation["current_pos"][0], animation["current_pos"][1], str(2**animation["init_tile_value"]))
            self.__state[animation["final_pos"][1] // constants.TILE_WIDTH][animation["final_pos"][0] // constants.TILE_WIDTH] = animation["final_tile_value"]

        if len(self.__animations) == 0:
            if self.__in_animation:
                self.__in_animation = False
                self.new_piece()

    def new_piece(self):
        # generates a new random piece in random position
        empty_indexes = []
        for y in range(len(self.__state)):
            for x in range(len(self.__state[y])):
                if self.__state[y][x] == 0:
                    empty_indexes.append((x, y))

        if len(empty_indexes) > 0:
            selected_index = random.randint(0, len(empty_indexes)-1)

            # get random chance: 90% of a 2, 10% of a 4
            self.__state[empty_indexes[selected_index][1]][empty_indexes[selected_index][0]] = self.tile_value() 
        self.check_game_over()

    def tile_value(self):
        # gets random tile value
        roll = random.randint(0,10)
        if roll != 1:
            return 1
        else:
            return 2

    def draw(self, surface):
        #draws the game board
        for y in range(len(self.__state)):
            for x in range(len(self.__state[y])):
                if self.__state[y][x] != 0 and self.__state[y][x] <= 50:
                    self.draw_tile(constants.TILE_WIDTH * x, constants.TILE_WIDTH * y, str(2 ** self.__state[y][x]))
                else:
                    pygame.draw.rect(surface, constants.TILE_COLOURS[0], pygame.Rect((constants.TILE_WIDTH * x + self.__x_offset, constants.TILE_WIDTH * y + self.__y_offset, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))

    def draw_tile(self, x, y, tile_value):
        # draws a tile
        tile_num = math.log2(int(tile_value))
        font_colour = None
        if tile_num <= 2:
            font_colour = constants.TEXT_GREY
        else:
            font_colour = constants.WHITE

        pygame.draw.rect(self.__surface, constants.TILE_COLOURS[tile_num], pygame.Rect((x + self.__x_offset, y + self.__y_offset, constants.TILE_WIDTH - constants.TILE_BORDER, constants.TILE_WIDTH-constants.TILE_BORDER)))
        font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', constants.TILE_FONT_SIZE)
        text = font.render(tile_value, True, font_colour)
        textRect = text.get_rect()
        textRect.center = (x + constants.TILE_WIDTH // 2 + self.__x_offset, y + constants.TILE_WIDTH // 2 + self.__y_offset)
        self.__surface.blit(text, textRect)
    
    def handle_keys(self, event):
        # move tiles in direction of the key pressed
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not self.__in_animation:
            self.move((-1, 0))
            self.__in_keydown = True
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not self.__in_animation:
            self.move((1, 0))
            self.__in_keydown = True
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not self.__in_animation:
            self.move((0, 1))
            self.__in_keydown = True
        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not self.__in_animation:
            self.move((0, -1))
            self.__in_keydown = True     

    def load_file(self, csv_file):
        # loads saved game board from csv file
        rows = []
        with open(csv_file, 'r') as file:
            csvreader = csv.reader(file)
            self.__score = int(next(file))
            for row in csvreader:
                rows.append(list(map(lambda n: int(n), row)))

        self.__state = rows

    def save(self, csv_file):
        # writing game_board to csv file 
        if self.__in_animation:
            self.__saving = True
        else:            
            with open(csv_file, 'w') as csvfile:   
                # creating a csv writer object   
                csvwriter = csv.writer(csvfile)   
                csvwriter.writerow(list([self.__score]))
                # writing the data rows   
                csvwriter.writerows(self.__state) 
            self.__saving = False
            self.__save_status = "Saved!"
            self.__save_colour = constants.GREEN
            self.__save_delay = constants.SAVE_ANIMATION_DELAY

    def restart(self):
        # restarts game
        self.__init__(self.__surface)

    def check_game_over(self):
        #checks if user can't move anymore and game is over

        #first check if there is any spare tile space
        y = 0
        vacant_tile_exists = False
        while y < len(self.__state) and not vacant_tile_exists:
            x = 0
            while x < len(self.__state[y]) and not vacant_tile_exists:
                if self.__state[y][x] == 0:
                    vacant_tile_exists = True
                x += 1
            y += 1

        if vacant_tile_exists == False:
            # secondly check if there are no two matching adjacent tiles
            # to do this we first check horizontally then vertically
            game_over = True

            y = 0
            while y < len(self.__state) and game_over:
                prev_tile = self.__state[y][0]
                x = 1
                while x < len(self.__state[y]) and game_over:
                    if self.__state[y][x] == prev_tile:
                        game_over = False
                    prev_tile = self.__state[y][x]
                    x += 1
                y += 1
                
            x = 0
            while x < len(self.__state[0]) and game_over:
                prev_tile = self.__state[0][x]
                y = 1
                while y < len(self.__state) and game_over:
                    if self.__state[y][x] == prev_tile:
                        game_over = False
                    prev_tile = self.__state[y][x]
                    y += 1
                x += 1
        
            if game_over:
                print("game_over")
                self.__game_over = True

    def read_highscore(self):
        # reads data from highscore file
        with open(constants.HIGHSCORE_FILE, "r") as file:
            return int(file.read())
    
    def update_highscore(self):
        # checks if new highscore and writes it to file
        if self.__score > self.__highscore:
            self.__highscore = self.__score
            with open(constants.HIGHSCORE_FILE, "w") as file:
                file.write(f"{self.__highscore}")

game = gameManager()
game.run()

            
        
        