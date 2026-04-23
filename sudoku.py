import pygame
import sys

from sudoku_generator import Board

pygame.init()

WIDTH = 900
HEIGHT = 1000
BG_COLOR = (250, 249, 246)
LINE_COLOR = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)


TITLE_FONT = pygame.font.Font(None, 80)
SUBTITLE_FONT = pygame.font.Font(None, 60)
BUTTON_FONT = pygame.font.Font(None, 50)


def draw_start_screen(screen):

    screen.fill(BG_COLOR)

    welcome_text = TITLE_FONT.render("Welcome to Sudoku", True, LINE_COLOR)
    pick_text = SUBTITLE_FONT.render("Select Game Mode:", True, LINE_COLOR)

    screen.blit(welcome_text, welcome_text.get_rect(center=(WIDTH // 2, 200)))
    screen.blit(pick_text, pick_text.get_rect(center=(WIDTH // 2, 400)))


    easy_btn = pygame.Rect(100, 500, 200, 80)
    med_btn = pygame.Rect(350, 500, 200, 80)
    hard_btn = pygame.Rect(600, 500, 200, 80)


    pygame.draw.rect(screen, ORANGE, easy_btn)
    pygame.draw.rect(screen, ORANGE, med_btn)
    pygame.draw.rect(screen, ORANGE, hard_btn)


    easy_txt = BUTTON_FONT.render("EASY", True, WHITE)
    med_txt = BUTTON_FONT.render("MEDIUM", True, WHITE)
    hard_txt = BUTTON_FONT.render("HARD", True, WHITE)

    screen.blit(easy_txt, easy_txt.get_rect(center=easy_btn.center))
    screen.blit(med_txt, med_txt.get_rect(center=med_btn.center))
    screen.blit(hard_txt, hard_txt.get_rect(center=hard_btn.center))

    return easy_btn, med_btn, hard_btn


def draw_game_ui(screen):
    pygame.draw.rect(screen, BG_COLOR, (0, 900, WIDTH, 100))

    reset_btn = pygame.Rect(100, 920, 200, 60)
    restart_btn = pygame.Rect(350, 920, 200, 60)
    exit_btn = pygame.Rect(600, 920, 200, 60)

    pygame.draw.rect(screen, ORANGE, reset_btn)
    pygame.draw.rect(screen, ORANGE, restart_btn)
    pygame.draw.rect(screen, ORANGE, exit_btn)

    reset_txt = BUTTON_FONT.render("Reset", True, WHITE)
    restart_txt = BUTTON_FONT.render("Restart", True, WHITE)
    exit_txt = BUTTON_FONT.render("Exit", True, WHITE)

    screen.blit(reset_txt, reset_txt.get_rect(center=reset_btn.center))
    screen.blit(restart_txt, restart_txt.get_rect(center=restart_btn.center))
    screen.blit(exit_txt, exit_txt.get_rect(center=exit_btn.center))

    return reset_btn, restart_btn, exit_btn


def draw_game_over(screen, won):
    screen.fill(BG_COLOR)

    if won == True:
        text = "Game won!"
        btn_text = "Exit"
    else:
        text = "Game over :("
        btn_text = "Restart"

    title_surface = TITLE_FONT.render(text, True, LINE_COLOR)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 200)))

    option_box = pygame.Rect(350, 500, 200, 80)
    pygame.draw.rect(screen, ORANGE, option_box)

    txt_surface = SUBTITLE_FONT.render(btn_text, True, WHITE)
    screen.blit(txt_surface, txt_surface.get_rect(center=option_box.center))

    return option_box


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    current_state = "start"
    board = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_state == "start":
                easy_btn, med_btn, hard_btn = draw_start_screen(screen)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    y = event.pos[1]

                    if easy_btn.collidepoint(x, y):
                        board = Board(WIDTH, 900, screen, "easy")
                        current_state = "playing"
                    elif med_btn.collidepoint(x, y):
                        board = Board(WIDTH, 900, screen, "medium")
                        current_state = "playing"
                    elif hard_btn.collidepoint(x, y):
                        board = Board(WIDTH, 900, screen, "hard")
                        current_state = "playing"

            elif current_state == "playing":
                reset_btn, restart_btn, exit_btn = draw_game_ui(screen)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    y = event.pos[1]

                    if reset_btn.collidepoint(x, y):
                        board.reset_to_original()
                    elif restart_btn.collidepoint(x, y):
                        current_state = "start"
                    elif exit_btn.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                    else:
                        clicked_coords = board.click(x, y)
                        if clicked_coords != None:
                            board.select(clicked_coords[0], clicked_coords[1])


                if event.type == pygame.KEYDOWN:
                    if board.selected_cell != None:

                        if event.key == pygame.K_UP:
                            board.move_selection("up")
                        elif event.key == pygame.K_DOWN:
                            board.move_selection("down")
                        elif event.key == pygame.K_LEFT:
                            board.move_selection("left")
                        elif event.key == pygame.K_RIGHT:
                            board.move_selection("right")

                        elif event.unicode.isdigit() and int(event.unicode) != 0:
                            board.sketch(int(event.unicode))

                        elif event.key == pygame.K_RETURN:
                            if board.selected_cell.sketch != 0:
                                board.place_number(board.selected_cell.sketch)

                                board.selected_cell.set_sketched_value(0)

                                if board.is_full() == True:
                                    if board.check_board() == True:
                                        current_state = "won"
                                    else:
                                        current_state = "lost"

            elif current_state == "won" or current_state == "lost":
                if current_state == "won":
                    option_box = draw_game_over(screen, True)
                else:
                    option_box = draw_game_over(screen, False)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    y = event.pos[1]

                    if option_box.collidepoint(x, y):
                        if current_state == "won":
                            pygame.quit()
                            sys.exit()
                        else:
                            current_state = "start"


        if current_state == "playing":
            screen.fill(BG_COLOR)
            board.draw()
            draw_game_ui(screen)

        pygame.display.update()



if __name__ == "__main__":
    main()