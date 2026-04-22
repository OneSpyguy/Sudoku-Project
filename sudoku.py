import pygame
import sys

pygame.init()

WIDTH = 900
HEIGHT = 1000
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
ORANGE = (220, 100, 50)
WHITE = (255, 255, 255)

TITLE_FONT = pygame.font.Font(None,100)
BUTTON_FONT = pygame.font.Font(None,50)
GAME_OVER_FONT = pygame.font.Font(None, 120)

def draw_start_screen(screen):

    screen.fill(BG_COLOR)

    title_surface = TITLE_FONT.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rect = title_surface.get.rect(center=(WIDTH // 2, HEIGHT // 2-50))
    screen.blit(sub_surface, sub_rect)

    easy_btn = pygame.Rect(150, 500, 150, 70)
    med_btn = pygame.Rect(350, 500, 200, 70)
    hard_btn = pygame.Rect(600, 500, 150, 70)

    pygame.draw.rect(screen, ORANGE, easy_btn)
    pygame.draw.rect(screen, ORANGE, med_btn)
    pygame.draw.rect(screen, ORANGE, hard_btn)

    easy_text = BUTTON_FONT.render("EASY", True, WHITE)
    med_text = BUTTON_FONT.render("MEDIUM", True, WHITE)
    hard_text = BUTTON_FONT.render("HARD", True, WHITE)

    screen.blit(easy_text, easy_text.get_rect(center=easy_btn.center))
    screen.blit(med_text, med_text.get_rect(center=med_btn.center))
    screen.blit(hard_text, hard_text.get_rect(center=hard_btn.center))

    return easy_btn, med_btn, hard_btn

def draw_game_ui(screen):

    pygame.draw.rect(screen, BG_COLOR, (0, 900, WIDTH, 100))

    reset_btn = pygame.Rect(200, 915, 150, 60)
    restart_btn = pygame.Rect(400, 915, 150, 60)
    exit_btn = pygame.Rect(600, 915, 150, 60)

    pygame.draw.rect(screen, ORANGE, reset_btn)
    pygame.draw.rect(screen, ORANGE, restart_btn)
    pygame.draw.rect(screen, ORANGE, exit_btn)


    reset_txt = BUTTON_FONT.render("RESET", True, WHITE)
    restart_txt = BUTTON_FONT.render("RESTART", True, WHITE)
    exit_txt = BUTTON_FONT.render("EXIT", True, WHITE)

    screen.blit(reset_txt, reset_txt.get_rect(center=reset_btn.center))
    screen.blit(restart_txt, restart_txt.get_rect(center=restart_btn.center))
    screen.blit(exit_txt, exit_txt.get_rect(center=exit_btn.center))

    return reset_btn, restart_btn, exit_btn


def draw_game_over(screen, won):

    screen.fill(BG_COLOR)


    if won == True:
        text = "Game Won!"
        btn_text = "EXIT"
    else:
        text = "Game Over :("
        btn_text = "RESTART"

    title_surface = GAME_OVER_FONT.render(text, True, LINE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_surface, title_rect)

    btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 70)
    pygame.draw.rect(screen, ORANGE, btn)

    txt_surface = BUTTON_FONT.render(btn_text, True, WHITE)
    screen.blit(txt_surface, txt_surface.get_rect(center=btn.center))

    return btn

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    current_state ="start"
    board = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



            if current_state == "start":
                easy_btn, med_btn, hard_btn = draw_start_screen(screen)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if easy_btn.collidepoint(event.pos):
                        board = Board(WIDTH, 900, screen, "easy")
                        current_state = 'playing'
                    elif med_btn.collidepoint(event.pos):
                        board = Board(WIDTH, 900, screen, "medium")
                        current_state = 'playing'
                    elif hard_btn.collidepoint(event.pos):
                        board = Board(WIDTH, 900, screen, "hard")
                        current_state = 'playing'

                elif current_state == 'playing':
                    reset_btn, restart_btn, exit_btn = draw_game_ui(screen)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x = event.pos[0]
                        y = event.pos[1]


                        if reset_btn.collidepoint(event.pos):
                            board.reset_to_original()
                        elif restart_btn.collidepoint(event.pos):
                            current_state = 'start'
                        elif exit_btn.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        else:

                            clicked = board.click(x, y)
                            if clicked != None:
                                board.select(clicked[0], clicked[1])

                    if event.type == pygame.KEYDOWN:

                        if board.selected_cell != None:

                            if event.unicode.isdigit() and int(event.unicode) != 0:
                                board.sketch(int(event.unicode))


                            elif event.key == pygame.K_RETURN:
                                if board.selected_cell.sketch != 0:
                                    board.place_number(board.selected_cell.sketch)


                                    if board.is_full() == True:
                                        if board.check_board() == True:
                                            current_state = 'won'
                                        else:
                                            current_state = 'lost'


elif current_state == 'won' or current_state == 'lost':
    if current_state == 'won':
        btn = draw_game_over(screen,True)
    else:
        btn = draw_game_over(screen, False)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if btn.collidepoint(event.pos):
            if current_state == 'won':

                pygame.quit()
                sys.exit()
            else:

                current_state = 'start'

if current_state == 'playing':
    screen.fill(BG_COLOR)
    board.draw()
    draw_game_ui(screen)

pygame.display.update()

If __name__ == "__main__":
main()
