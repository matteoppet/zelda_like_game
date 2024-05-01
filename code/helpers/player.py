import pygame
from helpers.animals import animals_sprite
from helpers.world import water_sprites
from helpers.zombie import zombies_sprites

from helpers.utils import update_list_actions_to_display

class Player(pygame.sprite.Sprite):

    # used as view area
    class temp_rect(pygame.sprite.Sprite):
        def __init__(self, player_center, orentation, player_size):
            # positioning the area rect of attack based on the direction of the player
            if orentation == "right":
                pos = (player_center[0]+player_size[0], player_center[1])
            elif orentation == "left":
                pos = (player_center[0]-player_size[0], player_center[1])
            elif orentation == "up":
                pos = (player_center[0], player_center[1]-(player_size[1]/2))
            elif orentation == "down":
                pos = (player_center[0], player_center[1]+(player_size[1]/2))

            self.image = pygame.Surface(size=player_size)
            self.rect = self.image.get_rect(center=pos)


    def __init__(self):
        super().__init__()

        self.size = (15, 25)
        pos = (700, 500)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

        self.old_rect = self.rect.copy()

        self.health = 100
        self.damage = 15 # punch

        self.food = 0

        self.orentation = "right"


    def actions(self, attack=False, eat=False):
        keys = pygame.key.get_pressed()
        vel = 1.3
        self.old_rect = self.rect.copy()

        if keys[pygame.K_w]:
            self.rect.y -= vel
            self.collisions("vertical", water_sprites)
            self.orentation = "up"
        if keys[pygame.K_s]:
            self.rect.y += vel
            self.collisions("vertical", water_sprites)
            self.orentation = "down"
        if keys[pygame.K_a]:
            self.rect.x -= vel
            self.collisions("horizontal", water_sprites)
            self.orentation = "left"
        if keys[pygame.K_d]:
            self.rect.x += vel
            self.collisions("horizontal", water_sprites)
            self.orentation = "right"
    
        if attack:
            self.attack()

        if eat:
            self.eat()

    
    def eat(self):
        if self.food == 0:
            update_list_actions_to_display("You don't have food")
        elif self.health == 100:
            update_list_actions_to_display("Your health is fully recovered, no need to eat!")
        else:
            tot_health = 100
            food_to_eat = tot_health - self.health
            
            food_copy = self.food

            if food_to_eat >= self.food:
                self.health += self.food
                self.food -= food_copy
            else:
                self.health += self.food
                self.food -= food_to_eat


    def collisions(self, direction, group_sprites):
        # video of collisions: https://youtu.be/W9uKzPFS1CI?si=BM5kFdmDDPSZhXO4
        collision = pygame.sprite.spritecollide(self, group_sprites, False)

        if collision:
            if direction == "horizontal":
                for sprite in collision:
                    # collision right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    # collision left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

            elif direction == "vertical":
                for sprite in collision:
                    # collision up
                    if self.rect.top+10 <= sprite.rect.bottom and self.old_rect.top+10 >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom-10
                    # collisions down
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top


    def attack(self):
        temp_sprite = self.temp_rect(self.rect.center, self.orentation, self.size)
        collision_animals = pygame.sprite.spritecollide(temp_sprite, animals_sprite, False)
        collision_zombies = pygame.sprite.spritecollide(temp_sprite, zombies_sprites, False)

        if collision_animals:
            for sprite_animal in collision_animals:
                sprite_animal.health -= self.damage

                if sprite_animal.health <= 0:
                    self.food += 5
                    sprite_animal.kill()
                    update_list_actions_to_display("Animal killed, +5 of food gained")
        if collision_zombies:
            for sprite_zombie in collision_zombies:
                sprite_zombie.health -= self.damage

                if sprite_zombie.health <= 0:
                    sprite_zombie.kill()
                    update_list_actions_to_display("Zombie killed")

        else:
            update_list_actions_to_display("No enemies or animals around")


    def draw(self, screen):
        screen.blit(self.image, self.rect)