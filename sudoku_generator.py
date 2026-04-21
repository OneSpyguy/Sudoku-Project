import math, random, pygame, sys

pygame.init()
screen = pygame.display.set_mode((900, 900))
screen.fill((255, 255, 255))
pygame.display.set_caption("Sudoku")

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketch = 0
        self.interact = False  # for use in board
        self.cell_size = 100

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketch = value

    def draw(self):
        top, left, bottom, right = self.row * self.cell_size, self.col * self.cell_size, self.cell_size, self.cell_size  # All caps are placeholders
        pygame.draw.rect(self.screen, (0, 0, 0), (left, top, right, bottom), 1)

        if self.interact:
            pygame.draw.rect(self.screen, (255, 0, 0), (left, top, right, bottom), 3)
            if self.value != 0:
                num_font = pygame.font.Font(None, 70)
                num_surf = num_font.render(str(self.value), True, (0, 0, 0))
                num_rect = num_surf.get_rect(center = (left + self.cell_size // 2, top + self.cell_size // 2))
                self.screen.blit(num_surf, num_rect)

            if self.sketch != 0:
                num_font = pygame.font.Font(None, 20)
                num_surf = num_font.render(str(self.value), True, (0, 0, 0))
                num_rect = num_surf.get_rect(bottom_left = ((left - 70),(bottom - 70)))
                self.screen.blit(num_surf, num_rect)

class Board:
    def __int__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        self.generator = SudokuGenerator(9, removed)
        self.generator.fill_values()

        self.generator.remove_cells()
        self.initial_board = [row[:] for row in self.generator.get_board()]

        self.cells = [
            [Cell(self.initial_board[i][j], i, j, screen) for j in range(9)]
            for i in range(9)
        ]
        self.selected_cell = None

    def draw(self):
        pass
    def select(self, row, col):
        pass
    def click(self, x, y):
        pass
    def sketch(self, value):
        pass
    def place_number(self, value):
        pass
    def reset_to_original(self):
        pass
    def is_full(self):
        pass
    def update_board(self):
        pass
    def check_board(self):
        pass
######################### SudokuGenerator Class ############################
import math
import random

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = 9
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(self.row_length)] for _ in range(self.row_length)]
        self.box_length = int(math.sqrt(self.row_length))


    def get_board(self):
        return self.board


    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        return True


    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True


    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True


    def is_valid(self, row, col, num):
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_row_start, box_col_start, num))


    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)


    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False



    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)


    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1


######################### generate_sudoku function ############################
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

####################### generating cells #########################

cells = [[Cell(0, j, i, screen).draw() for i in range(9)] for j in range(9)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            row_start = y // 300
            col_start = x // 300
            x, y = event.pos
            row = y // 100
            col = x // 100
            for r in range(9):
                for c in range(9):
                    cells[r][c].interact = False
            cells[row][col].interact = True
        if event.type == pygame.KEYDOWN:
            x, y = pygame.mouse.get_pos()
            z = event.unicode()
            if z.isdigit():
                cells[row][col].value = int(z)

    pygame.display.update()