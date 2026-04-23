# Import pygame and sys modules
import pygame
import sys

# Import Board class and start_screen, draw_button, and generate_sudoku functions
from board import Board
from board import start_screen
from board import draw_button
from sudoku_generator import generate_sudoku
 
BOARD_SIZE = 540
SCREEN_HEIGHT = 660   # 540 board + 120 for button bar

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50


def main():

    # Initialize pygame
    pygame.init()

    # Create font settings for button
    button_font=pygame.font.SysFont("Arial", 20)

    # Create rectangle for reset, restart, and exit buttons
    # Format: pygame.Rect(x (left), y (top), width, height)
    reset_rect = pygame.Rect(120, 570, BUTTON_WIDTH, BUTTON_HEIGHT)
    restart_rect = pygame.Rect(230, 570, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_rect = pygame.Rect(340, 570, BUTTON_WIDTH, BUTTON_HEIGHT)

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

    # Loop through Sudoku game
    while True:

        # Clear screen to begin game session
        # C - Instead of white, the board's background
        #color is light blue.
        win.fill((237, 247, 255))

        # Draw board
        board.draw()

        # Create reset, restart, and exit buttons
        draw_button(win, "Reset", reset_rect, button_font)
        draw_button(win, "Restart", restart_rect, button_font)
        draw_button(win, "Exit", exit_rect, button_font)

        # Event loop
        for event in pygame.event.get():

            # Manage player exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Click event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Check if clicked reset button
                # event.pos returns x, y
                if reset_rect.collidepoint(event.pos):
                    print("Clicked reset button")
                    # board.draw()
                    # Reset board (generate new numbers across board)

                # Check if clicked restart button
                if restart_rect.collidepoint(event.pos):
                    print("Clicked restart button")
                    # Create new game (new game function)

                # Check if clicked exit button
                if exit_rect.collidepoint(event.pos):
                    # Add pygame.quit and sys exit
                    pygame.quit()
                    sys.exit()

                # Check if player selects 1 - Easy
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

        # Restart function
        # Clear board

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
