# Import pygame and sys modules
import pygame
import sys

# Import Board class and start_screen, draw_button, and generate_sudoku functions
from board import Board
from board import start_screen
from sudoku_generator import *

# ── Colour palette
WHITE = (255, 255, 255)
LIGHT_RED = (220,  80,  80)   # main background colour
DARK_RED = (180,  40,  40)   # deeper red for button hover
BTN_COLOR = (255, 255, 255)   # white buttons
BTN_HVR = (220, 220, 220)   # light grey on hover
BTN_TEXT = (0,   0,   0)     # black button text
LINE_COLOR = (180,  60,  60)   # reddish separator line
from board import draw_button
from sudoku_generator import generate_sudoku
 
BOARD_SIZE = 540
SCREEN_HEIGHT = 660   # 540 board + 120 for button bar

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50


def game_over_screen(screen, result):
    import pygame
    pygame.font.init()

    width, height = screen.get_size()

    font_large = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 40)

    if result == "won":
        message = "You Won!"
    else:
        message = "Game Over"

    # Buttons
    restart_rect = pygame.Rect(width//2 - 100, height//2 + 40, 200, 50)
    exit_rect = pygame.Rect(width//2 - 100, height//2 + 110, 200, 50)

    while True:
        screen.fill((220, 80, 80))  # background

        # Draw message
        text = font_large.render(message, True, (255, 255, 255))
        screen.blit(text, (width//2 - text.get_width()//2, height//2 - 100))

        # Draw buttons
        pygame.draw.rect(screen, (255,255,255), restart_rect, border_radius=8)
        pygame.draw.rect(screen, (255,255,255), exit_rect, border_radius=8)

        restart_text = font_small.render("Restart", True, (0,0,0))
        exit_text = font_small.render("Exit", True, (0,0,0))

        screen.blit(restart_text, (restart_rect.x + 50, restart_rect.y + 10))
        screen.blit(exit_text, (exit_rect.x + 70, exit_rect.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                if exit_rect.collidepoint(event.pos):
                    return "exit"

# Main
# if __name__ == "__main__":
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

    # Form screen
    win = pygame.display.set_mode((540, 660))
    pygame.display.set_caption("Sudoku")
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
        removed_cells = 45

    elif difficulty == "hard":
        removed_cells = 55

    # Call Board class from board [dot] py
    board_data = generate_sudoku(9, removed_cells)
    board = Board(540, 540, win, difficulty, board_data)
    board = Board(BOARD_SIZE, BOARD_SIZE, win, difficulty, board_data)

    # Loop through Sudoku game
    while True:

        win.fill((255,255,255))
        board.draw()

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

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos[0], pos[1])

                if clicked:
                    board.select(clicked[0], clicked[1])

            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    board.sketch(num)

                if event.key == pygame.K_BACKSPACE:
                    board.clear()

                if event.key == pygame.K_RETURN:
                    if board.selected == True:
                        row, col = board.selected
                        num = board.cells[row][col].sketched_value
                        if num != 0:
                            board.place_number(num)
            # Click event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Check if clicked reset button
                # event.pos returns x, y
                if reset_rect.collidepoint(event.pos):
                    print("Clicked reset button")
                    # board.draw()
                    # Reset board (generate new numbers across board)
                    board.reset_to_original()

                # Check if clicked restart button
                if restart_rect.collidepoint(event.pos):
                    print("Clicked restart button")
                    # Create new game (new game function)
                    board_data = generate_sudoku(9, removed_cells)
                    board = Board(BOARD_SIZE, BOARD_SIZE, win, difficulty, board_data)

                # Check if clicked exit button
                if exit_rect.collidepoint(event.pos):
                    # Add pygame.quit and sys exit
                    pygame.quit()
                    sys.exit()

                # Check if player selects 1 - Easy
                # if (x == 180) and (y == 250):
                #     print("Generate Sudoku Board")

        pygame.display.update()

        # Win/loss condition

        if board.is_full():
            if board.check_board():
                result = "won"
            else:
                result = "lost"

            action = game_over_screen(win, result)

            if action == "restart":
                difficulty = start_screen(win)

                if difficulty == "easy":
                    removed_cells = 30
                elif difficulty == "medium":
                    removed_cells = 45
                else:
                    removed_cells = 55
                board_data = generate_sudoku(9, removed_cells)
                board = Board(540, 540, win, difficulty, board_data)

            elif action == "exit":
                pygame.quit()



# Main
if __name__ == "__main__":

    main()
