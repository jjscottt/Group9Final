import pygame

# Copied draw_button, color palette, and button settings from sudoku

# ── Color palette
WHITE = (255, 255, 255)
LIGHT_RED = (220,  80,  80)   # main background color
new_border = (0,0,0)   # C - changed dark_red to black
BTN_COLOR = (255, 255, 255)   # white buttons
BTN_HVR = (220, 220, 220)   # light gray on hover
BTN_TEXT = (0,   0,   0)     # black button text
LINE_COLOR = (180,  60,  60)   # reddish separator line

# Button settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

def draw_button(surface, text, rect, font, color=BTN_COLOR, hover_color=BTN_HVR, text_color=BTN_TEXT):
    mouse = pygame.mouse.get_pos()
    current_color = hover_color if rect.collidepoint(mouse) else color
    pygame.draw.rect(surface, current_color, rect, border_radius=8)
    pygame.draw.rect(surface, new_border, rect, 2, border_radius=8)
    label = font.render(text, True, text_color)
    lx = rect.x + (rect.width - label.get_width()) // 2
    ly = rect.y + (rect.height - label.get_height()) // 2
    surface.blit(label, (lx, ly))
    return rect


# ---------- START SCREEN ----------

def start_screen(win):
    import sys
    pygame.font.init()

    # Set background image

    bg_img = pygame.image.load('bg_img.jpg').convert()
    bg_img = pygame.transform.scale(bg_img, (1000, 700))

    # Set fonts

    font=pygame.font.SysFont("Arial", 50)
    sub_font = pygame.font.SysFont("Arial", 40)
    button_font=pygame.font.SysFont("Arial", 20)

    # Set difficulty-level buttons

    easy_rect=pygame.Rect(100,380,BUTTON_WIDTH,BUTTON_HEIGHT)
    medium_rect=pygame.Rect(210,380,BUTTON_WIDTH,BUTTON_HEIGHT)
    hard_rect=pygame.Rect(320,380,BUTTON_WIDTH,BUTTON_HEIGHT)

    while True:

        # The title and "Select Game Mode" prompt

        title=font.render("Welcome to Sudoku", True, (0,0,0))
        win.blit(title, (40, 100))

        sub_title = sub_font.render("Select Game Mode:", True, (0,0,0))
        win.blit(sub_title, (85, 285))

        # Button design

        draw_button(win, "Easy", easy_rect, button_font)
        draw_button(win, "Medium", medium_rect, button_font)
        draw_button(win, "Hard", hard_rect, button_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=event.pos
                if easy_rect.collidepoint(mouse_pos):
                    return "easy"
                elif medium_rect.collidepoint(mouse_pos):
                    return "medium"
                elif hard_rect.collidepoint(mouse_pos):
                    return "hard"

        # Set start screen background image
        win.blit(bg_img, (0, 0))

        # pygame.display.update()

# ---------- THE BOARD ----------

# The Cell class helps with interaction:
# value storage and placement, sketch, and position.

class Cell:
    def __init__(self, value, row, col, screen):
        self.value=value
        self.row=row
        self.col=col
        self.screen=screen
        self.sketched_value=0
        self.selected=False

    def set_cell_value(self, value):
        self.value=value

    def set_sketched_value(self, value):
        self.sketched_value=value

    def draw(self):
        gap=540//9
        x=self.col*gap
        y=self.row*gap

        font=pygame.font.SysFont("Arial", 30)
        small_font=pygame.font.SysFont("Arial", 20)

        if self.value!=0:
            text=font.render(str(self.value), True, (0,0,0))
            self.screen.blit(text, (x+20, y+15))
        elif self.sketched_value!=0:
            text = small_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

        if self.selected:
            pygame.draw.rect(self.screen, (255,0,0), (x, y, gap, gap), 3)

# The Board class:
# Contains 81 cell objects and handles user interaction.

class Board:
    def __init__(self, width, height, screen, difficulty, board):
        self.width=width
        self.height=height
        self.screen=screen
        self.difficulty=difficulty
        self.cells=[[Cell(board[i][j],i,j,screen) for j in range(9)] for i in range(9)]
        self.selected=None
        self.original=[[board[i][j] for j in range(9)] for i in range(9)]

    # Added function reset_to_original for sudoku[dot]py button 'Reset.'

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].value=self.original[i][j]
                self.cells[i][j].sketched_value=0

    def draw(self):
        gap=self.width//9

        for i in range(10):
            thickness=4 if i%3==0 else 1
            pygame.draw.line(self.screen, (0,0,0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(self.screen, (0,0,0), (i*gap, 0), (i*gap, self.height), thickness)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            self.cells[self.selected[0]][self.selected[1]].selected=False
        self.selected=(row,col)
        self.cells[row][col].selected=True

    def click(self, x, y):
        gap=self.width//9
        if x<self.width and y<self.height:
            return (y//gap, x//gap)
        return None

    def clear(self):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_cell_value(0)
        self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected is None:
            return
        row, col=self.selected
        self.cells[row][col].set_cell_value(value)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value==0:
                    return False
        return True
