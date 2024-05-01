import pygame
import random


class Zombies(pygame.sprite.Sprite):
    
    class temp_area(pygame.sprite.Sprite):
        def __init__(self, zombie_center):
            self.image = pygame.Surface((25, 30))
            self.rect = self.image.get_rect(center=zombie_center)


    def __init__(self, size, pos):
        super().__init__()

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("blue")

        self.health = 50


    def area_to_attack(self, player_rect):
        sprite_area = self.temp_area(self.rect.center)
        collision = sprite_area.rect.colliderect(player_rect)

        if collision:
            print("Damage from zombies")


    def move(self):
        ...


zombies_sprites = pygame.sprite.Group()
zombies_spawns = [
    (23, 542),
    (782, 28)
]

def create_zombies(n_zombies_to_spawn):
    for _ in range(n_zombies_to_spawn):
        random_spawn = random.choice([(3, 542), (782, 8)])

        random_x = random.randrange(random_spawn[0]-20, random_spawn[0]+20)
        random_y = random.randrange(random_spawn[1]-20, random_spawn[1]+20)

        zombie_sprite = Zombies((10, 15), (random_x, random_y))
        zombies_sprites.add(zombie_sprite)
