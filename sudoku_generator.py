import math, random, pygame, sys

pygame.init()
screen = pygame.display.set_mode((900, 1000))
screen.fill((250, 249, 246))
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
        # top, left, bottom, right = self.row * self.cell_size, self.col * self.cell_size, self.cell_size, self.cell_size  # All caps are placeholders
        # pygame.draw.rect(self.screen, (0, 0, 0), (left, top, right, bottom), 1)
        top = self.row * self.cell_size
        left = self.col * self.cell_size

        pygame.draw.rect(self.screen, (0, 0, 0), (left, top, self.cell_size, self.cell_size), 1)

        if self.value != 0:
            num_font = pygame.font.Font(None, 70)
            num_surf = num_font.render(str(self.value), True, (0, 0, 0))
            num_rect = num_surf.get_rect(center = (left + self.cell_size // 2, top + self.cell_size // 2))
            self.screen.blit(num_surf, num_rect)

        if self.sketch != 0:
            num_font = pygame.font.Font(None, 50)
            num_surf = num_font.render(str(self.sketch), True, (230, 230, 230))
            num_rect = num_surf.get_rect(bottomright = ((left + self.cell_size - 5), ((top + self.cell_size) - 5)))
            self.screen.blit(num_surf, num_rect)

        if self.interact:
            pygame.draw.rect(self.screen, (255, 0, 0), (left, top, self.cell_size, self.cell_size), 3)

class Board:
    def __init__(self, width, height, screen, difficulty):
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
        # CHANGES
        full_board = self.generator.get_board()
        self.solution = [row[:] for row in full_board]

        self.generator.remove_cells()
        self.initial_board = [row[:] for row in self.generator.get_board()]

        self.cells = [
            [Cell(self.initial_board[i][j], i, j, screen) for j in range(9)]
            for i in range(9)
        ]
        self.selected_cell = None

    def draw(self):
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * 100, 0), (i * 100, 900), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 100), (900, i * 100), thickness)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.interact = False

        self.selected_cell = self.cells[row][col]
        self.selected_cell.interact = True

    def click(self, x, y):
        if 0 <= x < 900 and 0 <= y < 900:
            return (y // 100, x // 100)
        return None

    def clear(self):
        if self.selected_cell:
            if self.initial_board[self.selected_cell.row][self.selected_cell.col] == 0:
                self.selected_cell.set_cell_value(0)
                self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            if self.initial_board[self.selected_cell.row][self.selected_cell.col] == 0:
                self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            if self.initial_board[self.selected_cell.row][self.selected_cell.col] == 0:
                self.selected_cell.set_cell_value(value)

    def move_selection(self, direction):
        if self.selected_cell:
            row, col = self.selected_cell.row, self.selected_cell.col
            if direction == "up" and row > 0:
                self.select(row - 1, col)
            elif direction == "down" and row < 8:
                self.select(row + 1, col)
            elif direction == "left" and col > 0:
                self.select(row, col - 1)
            elif direction == "right" and col < 8:
                self.select(row, col + 1)

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_cell_value(self.initial_board[i][j])
                self.cells[i][j].set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.generator.board[i][j] = self.cells[i][j].value

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != self.solution[i][j]:
                    return False
        return True


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

####################### game menu #########################
def draw_game_start(screen):
    font = pygame.font.Font(None, 80)
    font2 = pygame.font.Font(None, 60)
    screen.fill((250, 249, 246))
    welcome = font.render("Welcome to Sudoku", True, (0,0,0))
    pick = font2.render("Select Game Mode:", True, (0, 0, 0))
    screen.blit(welcome, welcome.get_rect(center = (450, 200)))
    screen.blit(pick, pick.get_rect(center = (450, 400)))

    easy = pygame.Rect(100, 500, 200, 80)
    medium = pygame.Rect(350, 500, 200, 80)
    hard = pygame.Rect(600, 500, 200, 80)
    pygame.draw.rect(screen, (255, 165, 0), easy)
    pygame.draw.rect(screen, (255, 165, 0), medium)
    pygame.draw.rect(screen, (255, 165, 0), hard)

    button_for_level = pygame.font.Font(None, 50)
    screen.blit(button_for_level.render("EASY", True, (255, 255, 255)), (150, 525))
    screen.blit(button_for_level.render("MEDIUM", True, (255, 255, 255)), (380, 525))
    screen.blit(button_for_level.render("HARD", True, (255, 255, 255)), (650, 525))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.collidepoint(event.pos):
                    return "easy"
                if medium.collidepoint(event.pos):
                    return "medium"
                if hard.collidepoint(event.pos):
                    return "hard"


def draw_end_screen(screen, outcome):
    font = pygame.font.Font(None, 80)
    font2 = pygame.font.Font(None, 60)
    screen.fill((250, 249, 246))
    if outcome:
        result = font.render("Game won!", True, (0, 0, 0))
        option = "Exit"

    else:
        result = font.render("Game over :(", True, (0, 0, 0))
        option = "Restart"

    screen.blit(result, result.get_rect(center=(400, 400)))

    text = font2.render(option, True, (0, 0, 0))

    option_box = pygame.Rect(350, 500, 200, 80)
    pygame.draw.rect(screen, (255, 165, 0), option_box)
    screen.blit(text, text.get_rect(center = option_box.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if option_box.collidepoint(event.pos):
                    if outcome:
                        pygame.quit()
                        sys.exit()
                    else:
                        return




level = draw_game_start(screen)
current_board = Board(900, 900, screen, level)
while True:
    screen.fill((255, 255, 255))
    current_board.draw()
    button_for_options = pygame.font.Font(None, 50)
    reset_text = button_for_options.render("Reset", True, (255, 255, 255))
    restart_text = button_for_options.render("Restart", True, (255, 255, 255))
    exit_text = button_for_options.render("Exit", True, (255, 255, 255))
    reset_box = pygame.Rect(100, 920, 200, 60)
    restart_box = pygame.Rect(350, 920, 200, 60)
    exit_box = pygame.Rect(600, 920, 200, 60)
    pygame.draw.rect(screen, (255, 165, 0), reset_box)
    pygame.draw.rect(screen, (255, 165, 0), restart_box)
    pygame.draw.rect(screen, (255, 165, 0), exit_box)
    screen.blit(reset_text, reset_text.get_rect(center = reset_box.center))
    screen.blit(restart_text, restart_text.get_rect(center = restart_box.center))
    screen.blit(exit_text, exit_text.get_rect(center = exit_box.center))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_box.collidepoint(event.pos):
                current_board.reset_to_original()
            elif restart_box.collidepoint(event.pos):
                level = draw_game_start(screen)
                current_board = Board(900, 900, screen, level)
            elif exit_box.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

            x, y = event.pos
            coords = current_board.click(x, y)
            if coords:
                current_board.select(coords[0], coords[1])
        if event.type == pygame.KEYDOWN and current_board.selected_cell:
            if event.key == pygame.K_RETURN:
                if current_board.selected_cell.sketch != 0:
                    current_board.selected_cell.set_cell_value(current_board.selected_cell.sketch)
                    current_board.selected_cell.set_sketched_value(0)
                    if current_board.is_full():
                        outcome = current_board.check_board()
                        draw_end_screen(screen, outcome)
                        level = draw_game_start(screen)
                        current_board = Board(900, 900, screen, level)


            elif event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                current_board.sketch(int(event.unicode))
            elif event.key == pygame.K_UP:
                current_board.move_selection("up")
            elif event.key == pygame.K_DOWN:
                current_board.move_selection("down")
            elif event.key == pygame.K_LEFT:
                current_board.move_selection("left")
            elif event.key == pygame.K_RIGHT:
                current_board.move_selection("right")


    pygame.display.update()