# board.py
import pygame

# ---------- START SCREEN ----------

# The start_screen(win) function MUST be called in sudoku [dot] py.
# See the following implementation:

# In sudoku.py ...
# from board import Board
# difficulty = start_screen(win) ####################### Call start_screen(win) function.
# board_data = generate_sudoku(9, removed_cells)
# board = Board(540, 540, win, difficulty, board_data) # Call Board class from board [dot] py
# while True:
#   board.draw()
#   pygame.display.update()

def start_screen(win):
    font=pygame.font.SysFont("comicsans", 50)
    small_font=pygame.font.SysFont("comicsans", 30)

    while True:
        win.fill((255,255,255)) #Background color

        #Difficulty levels
        title=font.render("Sudoku Game", True, (0,0,0))
        easy=small_font.render("1 - Easy", True, (0,0,0))
        medium=small_font.render("2 - Medium", True, (0,0,0))
        hard=small_font.render("3 - Hard", True, (0,0,0))

        win.blit(title, (180,100))
        win.blit(easy, (180, 250))
        win.blit(medium, (180, 300))
        win.blit(hard,(180, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    return "easy"
                elif event.key==pygame.K_2:
                    return "medium"
                elif event.key==pygame.K_3:
                    return "hard"

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
        self.sketched=False

    def set_cell_value(self, value):
        self.value=value

    def set_sketched_value(self, value):
        self.sketched_value=value

    def draw(self):
        gap=540//9
        x=self.col*gap
        y=self.row*gap

        font=pygame.font.SysFont("comicsans", 40)
        small_font=pygame.font.SysFont("comicsans", 20)

        if self.value!=0:
            text=font.render(str(self.value), True, (0,0,0))
            self.screen.blit(text, (x+20, y+15))
        elif self.sketched_value!=0:
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
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
        row, col=self.selected
        self.cells[row][col].set_cell_value(0)
        self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        row, col=self.selected
        self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        row, col=self.selected
        self.cells[row][col].set_cell_value(value)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value==0:
                    return False
        return True
