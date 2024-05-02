import pygame

pygame.init()
pygame.font.init()

SIZE_WINDOW = (1600, 960)
SCREEN = pygame.display.set_mode(SIZE_WINDOW)
BACKGROUND = pygame.Surface(SIZE_WINDOW)
CLOCK = pygame.time.Clock()

pygame.display.set_caption("A zelda like game")

FONT = pygame.font.SysFont("Arial", 20)
FONT_ACTIONS_TEXT = pygame.font.SysFont("Arial", 15)

 # type: ignore