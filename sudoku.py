# Import pygame and sys modules
import pygame
import sys

# Import Board class and start_screen and generate_sudoku functions
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
if __name__ == "__main__":

    # Initialize pygame
    pygame.init()

    # Screen display
    screen_display = pygame.display

    # Form screen
    win = pygame.display.set_mode((540, 660))
    pygame.display.set_caption("Sudoku")

    # Difficulty
    difficulty = start_screen(win)

    # Determine number of removed cells
    if difficulty == "easy":
        removed_cells = 30

    elif difficulty == "medium":
        removed_cells = 40

    elif difficulty == "hard":
        removed_cells = 50

    # Call Board class from board [dot] py
    board_data = generate_sudoku(9, removed_cells)
    board = Board(540, 540, win, difficulty, board_data)

    # Loop through Sudoku game
    while True:

        win.fill((255,255,255))
        board.draw()

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
                    removed_cells = 40
                else:
                    removed_cells = 50
                board_data = generate_sudoku(9, removed_cells)
                board = Board(540, 540, win, difficulty, board_data)

            elif action == "exit":
                pygame.quit()
                sys.exit()
