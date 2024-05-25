import pygame
import random


class Zombies(pygame.sprite.Sprite):
    
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

            


    def __init__(self, size, pos):
        super().__init__()
        self.size = size

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("blue")

        self.health = 50
        self.damage = 20
        self.orientation = "right"

        self.cooldown = 500
        self.last = pygame.time.get_ticks()


    def area_to_attack(self, player):
        sprite_area = self.temp_area(self.rect.center, self.size, self.orientation)
        collision = sprite_area.rect.colliderect(player.rect)

        if collision:
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                player.health -= self.damage
                print("Damage from zombies")


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


zombies_sprites = pygame.sprite.Group()
zombies_spawns = [
    (23, 542),
    (782, 28),
    (1435, 298),
    (1179, 279),
    (692, 431)
]

def create_zombies(n_zombies_to_spawn):
    for _ in range(n_zombies_to_spawn):
        random_spawn = random.choice(zombies_spawns)

        random_x = random.randrange(random_spawn[0]-20, random_spawn[0]+20)
        random_y = random.randrange(random_spawn[1]-20, random_spawn[1]+20)

        zombie_sprite = Zombies((10, 15), (random_x, random_y))
        zombies_sprites.add(zombie_sprite)
