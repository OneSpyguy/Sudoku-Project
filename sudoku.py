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
