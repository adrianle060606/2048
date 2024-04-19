
import pygame 
import constants
import random
import copy
import time
import math
import csv

# comment at the start of each method a description
# use name mangling to encapsulate code
# use inheritance
# game manager class

class gameManager():
    def __init__(self):
        pygame.init()
        self.in_menu = True
        self.in_guide = False
        self.exit = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)) 
        self.board = Board(self.screen)
        self.csv_file = "board.csv"

        
        pygame.display.set_caption("2048") 

    def run(self):
        while not self.exit:
            
            
            if self.in_menu:

                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.exit = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_btns(pygame.mouse.get_pos())

                #draw background
                self.screen.fill(constants.BACKGROUND_WHITE)

                #draw heading
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 100)
                text = font.render("2048", True, constants.TEXT_GREY)
                textRect = text.get_rect()
                textRect.center = (350, 120)
                self.screen.blit(text, textRect)

                if not self.in_guide:
                    #draw play button
                    self.draw_button(constants.PLAY_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Play")

                    #draw load button
                    self.draw_button(constants.LOAD_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Load Game")

                    #draw help button
                    self.draw_button(constants.HELP_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Guide")

                else:
                    font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 40)
                    text = font.render("How To Play", True, constants.TEXT_GREY)
                    textRect = text.get_rect()
                    textRect.center = (350, 300)
                    self.screen.blit(text, textRect)

                    font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 20)
                    for i, instruction in enumerate(constants.INSTRUCTIONS):
                        text = font.render(instruction, True, constants.TEXT_GREY)
                        textRect = text.get_rect()
                        textRect.center = (350, 370 + 50*i)
                        self.screen.blit(text, textRect)

                    #back button
                    self.draw_button(constants.BACK_BTN, constants.TILE_COLOURS[11], 30, constants.WHITE, "Back")


            else:
                
                for event in pygame.event.get():
                    #event manager
                    if event.type == pygame.QUIT: 
                        self.exit = True
                    elif event.type == pygame.KEYDOWN and not self.board.in_animation:
                        self.board.handle_keys(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_btns(pygame.mouse.get_pos())
                self.board.in_keydown = False
                
                if self.board.saving:
                    self.board.save(self.csv_file)
                if self.board.save_delay <= 0:
                    self.board.save_colour = constants.WHITE
                    self.board.save_status = "Save"
                else:
                    self.board.save_delay -= 1/constants.CLOCK_SPEED

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
                pygame.draw.rect(self.screen, constants.BACKGROUND_GREY, pygame.Rect((350, 40, 100, 60)))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 20)
                text = font.render("Score:", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (400, 50)
                self.screen.blit(text, textRect)

                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 25)
                text = font.render(f"{self.board.score}", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (400, 75)
                self.screen.blit(text, textRect)

                #highscore menu
                pygame.draw.rect(self.screen, constants.BACKGROUND_GREY, pygame.Rect((480, 40, 100, 60)))
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 18)
                text = font.render("Highscore:", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (530, 50)
                self.screen.blit(text, textRect)

                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 25)
                text = font.render(f"{self.board.highscore}", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (530, 75)
                self.screen.blit(text, textRect)

                #draw restart button
                self.draw_button(constants.RESTART_BTN, constants.BROWN, 20, constants.WHITE, "Restart")

                #draw save button
                self.draw_button(constants.SAVE_BTN, constants.BROWN, 20, self.board.save_colour, self.board.save_status)

                #draw back button
                self.draw_button(constants.HOME_BTN, constants.BROWN, 20, constants.WHITE, "Home")

                #draw board and tiles
                self.board.draw(self.screen)
                self.board.animate_tiles()

                #if gameover render gameover text
                font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', 50)
                text = font.render("Game Over", True, constants.WHITE)
                textRect = text.get_rect()
                textRect.center = (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)
                self.screen.blit(text, textRect)

                
                

            pygame.display.update()
            self.clock.tick(constants.CLOCK_SPEED)

    def handle_btns(self, pos):
        # decides which buttons are pressed based on mouse pos
        
        if self.in_menu: #menu buttons
            btn = constants.PLAY_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.new_game()
            
            btn = constants.LOAD_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.load_game()

            btn = constants.HELP_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.help_menu()

            btn = constants.BACK_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.in_guide = False

        else: #game buttons

            #home button
            btn = constants.HOME_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.in_menu = True

            #save button
            btn = constants.SAVE_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.board.save(self.csv_file)

            #restart button
            btn = constants.RESTART_BTN
            if pos[0] >= btn[0] and pos[0] <= btn[0] + btn[2] and pos[1] >= btn[1] and pos[1] <= btn[1] + btn[3]:
                self.board.restart()



    def new_game(self):
        self.board.restart()
        self.in_menu = False

    def load_game(self):
        self.board.restart()
        self.in_menu = False
        self.board.load_file(self.csv_file)


    def help_menu(self):
        self.in_guide = True

    def draw_button(self, btn_position, btn_colour, font_size, font_colour, text_content):
        pygame.draw.rect(self.screen, btn_colour, pygame.Rect(btn_position), 0, 5)
        font = pygame.font.Font('Assets/Fonts/clear_sans_bold.ttf', font_size)
        text = font.render(text_content, True, font_colour)
        textRect = text.get_rect()
        textRect.center = (0.5*(2*btn_position[0] + btn_position[2]), 0.5*(2*btn_position[1] + btn_position[3]))
        self.screen.blit(text, textRect)

class Board(object):
    def __init__(self, surface):
        # 0 --> empty, 1 --> 2, 2 --> 4, 3 --> 8 etc.
        self.state = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.new_piece()
        self.new_piece()
        self.score = 0
        self.highscore = self.read_highscore()
        self.in_keydown = False
        self.surface = surface
        self.in_animation = False
        self.animations = []
        self.saving = False
        self.save_status = "Save"
        self.save_colour = constants.WHITE
        self.save_delay = 0
        self.game_over = False

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
        self.check_game_over()

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
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.move((-1, 0))
            self.in_keydown = True
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.move((1, 0))
            self.in_keydown = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.move((0, 1))
            self.in_keydown = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.move((0, -1))
            self.in_keydown = True     

    def load_file(self, csv_file):
        # loads saved game board from csv file
        rows = []
        with open(csv_file, 'r') as file:
            csvreader = csv.reader(file)
            self.score = int(next(file))
            for row in csvreader:
                rows.append(list(map(lambda n: int(n), row)))

        self.state = rows

    def save(self, csv_file):
        # writing game_board to csv file 
        if self.in_animation:
            self.saving = True
        else:            
            with open(csv_file, 'w') as csvfile:   
                # creating a csv writer object   
                csvwriter = csv.writer(csvfile)   
                csvwriter.writerow(list([self.score]))
                # writing the data rows   
                csvwriter.writerows(self.state) 
            self.saving = False
            self.save_status = "Saved!"
            self.save_colour = constants.GREEN
            self.save_delay = constants.SAVE_ANIMATION_DELAY

    def restart(self):
        self.__init__(self.surface)

    def check_game_over(self):
        #checks if user can't move anymore

        #first check if there is any spare tile space
        y = 0
        vacant_tile_exists = False
        while y < len(self.state) and not vacant_tile_exists:
            x = 0
            while x < len(self.state[y]) and not vacant_tile_exists:
                if self.state[y][x] == 0:
                    vacant_tile_exists = True
                x += 1
            y += 1

        if vacant_tile_exists == False:
            # secondly check if there are no two matching adjacent tiles
            # to do this we first check horizontally then vertically
            game_over = True

            y = 0
            while y < len(self.state) and game_over:
                prev_tile = self.state[y][0]
                x = 1
                while x < len(self.state[y]) and game_over:
                    if self.state[y][x] == prev_tile:
                        game_over = False
                    prev_tile = self.state[y][x]
                    x += 1
                y += 1
                
            x = 0
            while x < len(self.state[0]) and game_over:
                prev_tile = self.state[0][x]
                y = 1
                while y < len(self.state) and game_over:
                    if self.state[y][x] == prev_tile:
                        game_over = False
                    prev_tile = self.state[y][x]
                    y += 1
                x += 1
        
            if game_over:
                print("game_over")
                self.game_over = True

    def read_highscore(self):
        with open(constants.HIGHSCORE_FILE, "r") as file:
            return int(file.read())
    
    def update_highscore(self):
        # checks if new highscore and writes it to file
        if self.score > self.highscore:
            self.highscore = self.score
            with open(constants.HIGHSCORE_FILE, "w") as file:
                file.write(f"{self.highscore}")

game = gameManager()
game.run()

            
        
        