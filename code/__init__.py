import pygame

pygame.init()
pygame.font.init()

SIZE_WINDOW = (1600, 960)
SCREEN = pygame.display.set_mode(SIZE_WINDOW)
BACKGROUND = pygame.Surface(SIZE_WINDOW)
CLOCK = pygame.time.Clock()

pygame.display.set_caption("A zelda like game")

FONT_SIZE_20 = pygame.font.SysFont("Arial", 20)
FONT_SIZE_15 = pygame.font.SysFont("Arial", 15)
FONT_SIZE_10 = pygame.font.SysFont("Arial", 10)

 # type: ignore