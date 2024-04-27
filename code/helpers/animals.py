import pygame
import numpy as np


class Spawns(pygame.sprite.Sprite):
    def __init__(self, name, pos):
        super().__init__()
        self.pos = pos 

        self.name = name
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("red")

        self.max_animals_to_spawn = 5

    
    def coordinate_to_spawn(self):
        x = np.random.randint(self.pos[0]-100, self.pos[0]+10)
        y = np.random.randint(self.pos[1]-100, self.pos[1]+100)

        return (x,y)


class Animals(pygame.sprite.Sprite):

    def __init__(self, class_sprite, size, pos, spawn):
        super().__init__()

        self.class_sprite = class_sprite
        self.spawn = spawn

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("pink")

        self.health = 50
        self.damage = 15




animals_sprite = pygame.sprite.Group()

def spawn_animals(pos, spawn_name):
    x,y = pos

    sprite_animal = Animals("animals", (15, 10), (x,y), spawn_name)
    animals_sprite.add(sprite_animal)


animals_spawns_sprite = pygame.sprite.Group()
spawns = [
    ("1", (530, 388)),
    ("2", (1009, 293)),
    ("3", (1166, 559))
]

def init_spawns():
    for spawn in spawns:
        sprite_spawn = Spawns(spawn[0], spawn[1])
        animals_spawns_sprite.add(sprite_spawn)