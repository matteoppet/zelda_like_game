import pygame
from data import weapon_data 
from utils import tiles

class Player(pygame.sprite.Sprite):
    data = {
        "equipment": {
            "armors": {
                "helmet": None,
                "chest": None,
                "pants": None,
                "shoes": None
            },
            "weapons": "hands"
        },

        "skills": {
            "strength": 0,
            "constitution": 0,
            "intelligence": 0,
            "charisma": 0
        },

        "exp": 0,
        "class": None
    }

    def __init__(self, pos, obstacle_sprites, group):
        super().__init__(group)
        pygame.sprite.Sprite.__init__(self)

        # basic variable
        self.image = tiles[26]
        self.rect = self.image.get_rect(center=pos)

        # movements
        self.hitbox = self.rect.inflate(-40, -50)
        self.hitbox.y += 25
    
        self.speed = 1.3
        self.direction = pygame.math.Vector2()
        self.orientation = "down"
        self.status = "idle"

        # stats
        self.health = 100

        # others
        self.last_timing = pygame.time.get_ticks()
        self.old_rect= self.rect.copy()
        self.obstacle_sprites = obstacle_sprites
        self.sprite_type = "player"
        self.layout_level = 3



    def actions(self, enemies_sprites):
        keys = pygame.key.get_pressed()

        # movements
        if keys[pygame.K_w]:
            self.direction.y = -self.speed
            self.update_movements_variables("up")
        elif keys[pygame.K_s]:
            self.direction.y = self.speed
            self.update_movements_variables("down")
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -self.speed
            self.update_movements_variables("left")
        elif keys[pygame.K_d]:
            self.direction.x = self.speed
            self.update_movements_variables("right")
        else:
            self.direction.x = 0

        # update status to idle if no movements
        if not any(keys):
            self.status = "idle"

        # update the position only in case of a movement
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.update()

        # attack
        if keys[pygame.K_SPACE]:
            self.attack(enemies_sprites)

        # eat
        if keys[pygame.K_e]:
            self.eat()

    
    def update_movements_variables(self, direction):
        self.status = direction
        self.orientation = direction


    def update(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        self.rect.center = (self.hitbox.center[0], self.hitbox.center[1]-25)

        self.update_graphic(self.orientation)


    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:

                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == "vertical":
            for sprite in self.obstacle_sprites:

                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom


    def attack(self, enemies_sprites):
        self.status = "attack"

        for enemie in enemies_sprites:
            if self.hitbox.colliderect(enemie.hitbox):
                print("hitbox hit")


    def eat(self):
        ...

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update_graphic(self, orientation):
        if orientation == "right":
            self.image = tiles[39]
        if orientation == "up":
            self.image = tiles[0]
        if orientation == "down":
            self.image = tiles[26]
        if orientation == "left":
            self.image = tiles[13]
        