import pygame

obstacle_sprites = pygame.sprite.Group()

obstacles_data = [
    ((50,50), (300, 200)),
    ((50, 50), (200, 300))
]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("red")


def create_obstacles():
    for data in obstacles_data:
        sprite = Obstacle(data[0], data[1])
        obstacle_sprites.add(sprite)