# Import pygame and sys modules
import pygame
import sys

# Import Board class and start_screen and generate_sudoku functions
from board import Board
from board import start_screen
from sudoku_generator import generate_sudoku

# ── Colour palette
WHITE = (255, 255, 255)
LIGHT_RED = (220,  80,  80)   # main background colour
DARK_RED = (180,  40,  40)   # deeper red for button hover
BTN_COLOR = (255, 255, 255)   # white buttons
BTN_HVR = (220, 220, 220)   # light grey on hover
BTN_TEXT = (0,   0,   0)     # black button text
LINE_COLOR = (180,  60,  60)   # reddish separator line
 
BOARD_SIZE = 540
SCREEN_HEIGHT = 660   # 540 board + 120 for button bar


# Draw button
def draw_button(surface, text, rect, font, color=BTN_COLOR, hover_color=BTN_HVR, text_color=BTN_TEXT):
    mouse = pygame.mouse.get_pos()
    current_color = hover_color if rect.collidepoint(mouse) else color
    pygame.draw.rect(surface, current_color, rect, border_radius=8)
    pygame.draw.rect(surface, DARK_RED, rect, 2, border_radius=8)
    label = font.render(text, True, text_color)
    lx = rect.x + (rect.width - label.get_width()) // 2
    ly = rect.y + (rect.height - label.get_height()) // 2
    surface.blit(label, (lx, ly))
    return rect


# Main
if __name__ == "__main__":

    # Initialize pygame
    pygame.init()

    # Screen display
    screen_display = pygame.display

    # Form screen
    screen = screen_display.set_mode()

    # Get default size
    x, y = screen.get_size()

    # Store screen size
    z = [x, y]

    # Set size of window
    win = screen_display.set_mode(z)

    # Difficulty
    difficulty = start_screen(win)

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
    board = Board(540, 540, win, difficulty, board_data)

    # Loop through Sudoku game
    while True:

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
