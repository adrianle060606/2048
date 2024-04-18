import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 400, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048 Game - Home Screen")
game_script = '2048.py'

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 128, 255)

# Define fonts
TITLE_FONT = pygame.font.Font(None, 48)
BUTTON_FONT = pygame.font.Font(None, 32)
INSTRUCTION_FONT = pygame.font.Font(None, 24)

# Define button properties
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X, BUTTON_Y = (WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2 + 50

# Define instructions
INSTRUCTIONS = [
    "Use arrow keys to move tiles in any direction.",
    "When two tiles with the same number touch, they merge into one!",
    "Join the numbers and get to the 2048 tile!"
]

# Main loop
def main():
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                    # Start the game (replace with your game's main function)
                    print("Starting the game...")
                    subprocess.run(['python', game_script])

        # Clear the window
        WINDOW.fill(WHITE)

        # Render title
        title_text = TITLE_FONT.render("2048 Game", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        WINDOW.blit(title_text, title_rect)

        # Render start button
        pygame.draw.rect(WINDOW, BLUE, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        start_text = BUTTON_FONT.render("Start Game", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
        WINDOW.blit(start_text, start_rect)

        # Render instructions
        for i, instruction in enumerate(INSTRUCTIONS):
            instruction_text = INSTRUCTION_FONT.render(instruction, True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100 + i * 30))
            WINDOW.blit(instruction_text, instruction_rect)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()