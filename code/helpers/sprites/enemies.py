import pygame
import random
from ..objects import Types_of_enemies
import numpy as np


class Enemie(pygame.sprite.Sprite):
    
    class temp_area(pygame.sprite.Sprite):
        def __init__(self, zombie_center, zombie_size, orientation):

            if orientation == "right":
                pos = (zombie_center[0]+zombie_size[0], zombie_center[1])
            elif orientation == "left":
                pos = (zombie_center[0]-zombie_size[0], zombie_center[1])
            elif orientation == "up":
                pos = (zombie_center[0], zombie_size[1]-(zombie_center[1]/2))
            elif orientation == "down":
                pos = (zombie_center[0], zombie_size[1]+(zombie_center[1]/2))

            self.image = pygame.Surface(zombie_size)
            self.rect = self.image.get_rect(center=pos)


    def __init__(self, name, pos):
        super().__init__()
        self.size = Types_of_enemies.types[name]["size"]
        self.pos = pos
        self.name = name
        self.health = Types_of_enemies.types[name]["health"]
        self.damage = Types_of_enemies.types[name]["damage"]
        self.defense = Types_of_enemies.types[name]["defense"]
        self.cooldown = Types_of_enemies.types[name]["cooldown"]
        self.orientation = "right" # standard
        self.last = pygame.time.get_ticks()

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.image.fill("red")



    def area_to_attack(self, player):
        distance = np.linalg.norm(np.array(self.rect.center) - np.array(player.rect.center))

        if distance < 25:
            print(distance, "attack")

            now = pygame.time.get_ticks()
            if now-self.last >= self.cooldown:
                self.last = now

                player.health -= self.damage - player.defense


    def move(self, action):
        self.velocity = 1
        if action == 0:
            self.rect.x -= self.velocity
            self.orientation = "left"
        elif action == 1:
            self.rect.x += self.velocity
            self.orientation = "right"
        elif action == 2:
            self.rect.y -= self.velocity
            self.orientation = "up"
        elif action == 3:
            self.rect.y += self.velocity
            self.orientation = "down"


enemies_sprites = pygame.sprite.Group()
enemies_spawns = [
    (23, 542),
    (782, 28),
    (1435, 298),
    (1179, 279),
    (692, 431)
]


def create_enemies(n_enemies_to_spawn):
    for _ in range(n_enemies_to_spawn):
        # pos random
        random_spawn = random.choice(enemies_spawns)
        random_x = random.randrange(random_spawn[0]-20, random_spawn[0]+20)
        random_y = random.randrange(random_spawn[1]-20, random_spawn[1]+20)

        name_zombies = [k for k in Types_of_enemies.types.keys()]
        random_enemies = random.choice(name_zombies)

        enemie_sprite = Enemie(random_enemies, (random_x, random_y))
        enemies_sprites.add(enemie_sprite)