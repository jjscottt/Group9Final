# Import pygame and sys modules
import pygame
import sys

# Import Board class and start_screen and generate_sudoku functions
from board import Board
from board import start_screen
from sudoku_generator import generate_sudoku
 
BOARD_SIZE = 540
SCREEN_HEIGHT = 660   # 540 board + 120 for button bar

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100


def main():

    # Initialize pygame
    pygame.init()

    # Create font settings for button
    button_font = pygame.font.Font(None, 30)

    # Create rectangle for reset, restart, and exit buttons
    # Format: pygame.Rect(x (left), y (top), width, height)
    reset_rect = pygame.Rect(60, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_rect = pygame.Rect(60, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_rect = pygame.Rect(60, 600, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Screen display
    screen_display = pygame.display

    # Set screen size
    x, y = BOARD_SIZE, SCREEN_HEIGHT

    # Store screen size
    z = [x, y]

    # Set size of window
    win = screen_display.set_mode(z)

    # Difficulty
    difficulty = start_screen(win)

    # 1. Remove start screen after difficulty screen
    # 2. Fill screen with white
    win.fill((255, 255, 255))

    # Update screen
    pygame.display.update()

    # Determine number of removed cells
    if difficulty == "easy":
        removed_cells = 30

    elif difficulty == "medium":
        removed_cells = 40

    elif difficulty == "hard":
        removed_cells = 50

    # Board data
    board_data = generate_sudoku(9, removed_cells)

    # Call Board class from board [dot] py
    board = Board(BOARD_SIZE, BOARD_SIZE, win, difficulty, board_data)
    # board = Board(x, y, win, difficulty, board_data)

    # Create reset, restart, and exit buttons
    draw_button(win, "RESET", reset_rect, button_font)
    draw_button(win, "RESTART", restart_rect, button_font)
    draw_button(win, "EXIT", exit_rect, button_font)

    # Loop through Sudoku game
    while True:

        # Clear screen to begin game session
        win.fill((255, 255, 255))

        # Draw board
        board.draw()

        # Event loop
        for event in pygame.event.get():

            # Manage player exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Click event
            # if event.type == pygame.MOUSEBUTTONDOWN:
            # Get position
            # x, y = event.pos
            #
            # # Check if player selects 1 - Easy
            # if (x == 180) and (y == 250):
            #     print("Generate Sudoku Board")

            # Key input event
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_1:
            #         # 1
            #     elif event.key == pygame.K_2:
            #         # 2
            #     elif event.key == pygame.K_3:
            #         # 3
            #     elif event.key == pygame.K_4:
            #         # 4
            #     elif event.key == pygame.K_5:
            #         # 5
            #     elif event.key == pygame.K_6:
            #         # 6
            #     elif event.key == pygame.K_7:
            #         # 7
            #     elif event.key == pygame.K_8:
            #         # 8
            #     elif event.key == pygame.K_9:
            #         # 9
            #     # Return/enter key
            #     elif event.key == pygame.K_RETURN:
            #         # Return

        pygame.display.update()

        # Win/loss condition

        # End game screen
        # if game_result in ("won", "lost"):
        #     end = game_over_screen(win, game_result)
        #
        #     if end == "restart":
        #         # Back to start screen
        #         continue


# Main
if __name__ == "__main__":

    main()
