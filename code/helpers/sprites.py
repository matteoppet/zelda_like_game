import pygame


class Animals(pygame.sprite.Sprite):

    def __init__(self, class_sprite, name, size, pos):
        super().__init__()

        self.class_sprite = class_sprite
        self.name = name

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("pink")

        self.health = 50
        self.damage = 15


class Zombies(pygame.sprite.Sprite):
    def __init__(self):
        ...


def create_animals():
    for animal in animals_data:
        sprite = Animals("animals", animal[0], animal[1], animal[2])
        animal_sprites.add(sprite)


animal_sprites = pygame.sprite.Group()
animals_data = [
    ("1", (35, 25), (400, 400)),
    ("2", (35, 25), (100, 100))
]

zombies_sprites = pygame.sprite.Group()
zombies_data = []