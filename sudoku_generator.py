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
        top, bottom = self.row * self.cell_size, self.row * self.cell_size + self.cell_size  # All caps are placeholders
        num_font = pygame.font.Font(None, 80)
        one_surf = num_font.render('1', 0, (0, 255, 0))
        one_rect = one_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        two_surf = num_font.render('2', 0, (0, 255, 0))
        two_rect = two_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        three_surf = num_font.render('3', 0, (0, 255, 0))
        three_rect = three_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        four_surf = num_font.render('4', 0, (0, 255, 0))
        four_rect = four_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        five_surf = num_font.render('5', 0, (0, 255, 0))
        five_rect = five_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        six_surf = num_font.render('6', 0, (0, 255, 0))
        six_rect = six_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        seven_surf = num_font.render('7', 0, (0, 255, 0))
        seven_rect = seven_surf.get_rect(center=(top + (self.cell_size // 2), bottom - (self.cell_size // 2)))
        eight_surf = num_font.render('8', 0, (0, 255, 0))
        eight_rect = eight_surf.get_rect(center=(top + (self.cell_size // 2), bottom + (self.cell_size // 2)))
        nine_surf = num_font.render('9', 0, (0, 255, 0))
        nine_rect = nine_surf.get_rect(center=(top + (self.cell_size // 2), bottom + (self.cell_size // 2)))

        if self.interact:
            pygame.draw.rect(screen, (255, 0, 0), ((self.row * self.cell_size + self.cell_size), (self.col * self.cell_size + self.cell_size)), 1)
            screen.blit(one_surf, one_rect)

class Board:
    def __int__(self, width, height, screen, difficulty):

    def draw(self):

    def select(self, row, col):

    def click(self, x, y):

    def sketch(self, value):

    def place_number(self, value):

    def reset_to_original(self):

    def is_full(self):

    def update_board(self):

    def check_board(self):

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
            print(" ".join(map(str, row)))

    def valid_in_row(self, row, num):
        return num not in self.board[row]


    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False
        return True


    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + self.box_length):
            for j in range(col_start, col_start + self.box_length):
                if self.board[i][j] == num:
                    return False #Need a way for boxes to not overlap or position base on chosen box alone
        return True


    def is_valid(self, row, col, num):
        box_row_start = (row // self.box_length) * self.box_length
        box_col_start = (col // self.box_length) * self.box_length
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_row_start, box_col_start, num))


    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = nums.pop() #what does this do?


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
            # Ensure we don't remove the same cell twice [cite: 585, 586]
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row, row_start = y // 300
            col, col_start = x // 300
        if event.type == pygame.KEYDOWN:
            z = event.unicode

    pygame.display.update()