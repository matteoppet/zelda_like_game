import pygame

class Build:
    def __init__(self):
        ...

    def wall(self, side=None, pos=None):
        rect_to_draw = pygame.Rect(pos[0], pos[1], 15, 32)
        rect_to_collide = pygame.Rect(pos[0], pos[1], 15, 15)

        return (rect_to_draw, rect_to_collide)