import pygame 
import random

towers_sprite_group = pygame.sprite.Group()

class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, size, rect, group):
        super().__init__(group)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.rect = rect

        self.area_of_attack_rect = pygame.Rect(0, 0, 130, 130)
        self.area_of_attack_rect.center = self.rect.center

        self.cooldown = 400


class Base:
    def __init__(self, spawn_base_tiles):
        tile_spawn = random.choice(spawn_base_tiles)

        topleft = (tile_spawn.rect.centerx-16, tile_spawn.rect.centery-16)
        size = (150, 150)

        self.area_base_rect = pygame.Rect(topleft, size)

        self.create_defense_tower()

        self.last_timing = pygame.time.get_ticks()


    def draw(self, screen):
        pygame.draw.rect(screen, "blue", self.area_base_rect)


    def draw_towers(self, screen):
        for key, value in self.dict_rect_towers.items():
            pygame.draw.rect(screen, "red", value.rect)
            # pygame.draw.rect(screen, "red", value.area_of_attack_rect)


    def towers_defense_action(self, zombies_sprite, player):
        for key, value in self.dict_rect_towers.items():
            for zombie in zombies_sprite:
                if value.area_of_attack_rect.colliderect(zombie.rect):

                    now = pygame.time.get_ticks()
                    if now-self.last_timing >= value.cooldown:
                        zombie.kill()
                        print("zombie killed")
                        
                        self.last_timing = now
                        

    def create_defense_tower(self):
        self.dict_rect_towers = {}
        size_towers = (15, 45)

        rect_tower_topleft = pygame.Rect(
            self.area_base_rect.topleft[0], self.area_base_rect.topleft[1]-size_towers[1]+size_towers[0], 
            size_towers[0], size_towers[1])
        sprite_tower_topleft = Sprite(size_towers, rect_tower_topleft, towers_sprite_group)
        self.dict_rect_towers["topleft"] = sprite_tower_topleft


        rect_tower_topright = pygame.Rect(
            self.area_base_rect.topright[0]-size_towers[0], self.area_base_rect.topright[1]-size_towers[1]+size_towers[0], 
            size_towers[0], size_towers[1])
        sprite_tower_topright = Sprite(size_towers, rect_tower_topright, towers_sprite_group)
        self.dict_rect_towers["topright"] = sprite_tower_topright

        rect_tower_bottomleft = pygame.Rect(
            self.area_base_rect.bottomleft[0], self.area_base_rect.bottomleft[1]-size_towers[1], 
            size_towers[0], size_towers[1])
        sprite_tower_bottomleft = Sprite(size_towers, rect_tower_bottomleft, towers_sprite_group)
        self.dict_rect_towers["bottomleft"] = sprite_tower_bottomleft

        rect_tower_bottomright = pygame.Rect(
            self.area_base_rect.bottomright[0]-size_towers[0], self.area_base_rect.bottomright[1]-size_towers[1], 
            size_towers[0], size_towers[1])
        sprite_tower_bottomright = Sprite(size_towers, rect_tower_bottomright, towers_sprite_group)
        self.dict_rect_towers["bottomright"] = sprite_tower_bottomright