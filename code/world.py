import pytmx
import pygame
from player import Player
from utils import import_layout_csv, import_folder
import random
import numpy as np
from settings import *
from animals import Animal

class Tile(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups, type, layout_level):
        super().__init__(groups)
        self.sprite_type = type

        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.layout_level = layout_level

        self.old_rect = self.rect


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, groups, layout_level):
        super().__init__(groups)

        self.image = pygame.image.load("../assets/tileset/Resources/Trees/single_tree.png")
        self.rect = self.image.get_rect(bottomleft=pos)

        self.rect.x -= 64

        self.hitbox = self.rect.inflate(-155, -40)
        self.hitbox.y += 130
        self.hitbox.height -= 124

        self.sprite_type = "tree"

        self.layout_level = 3
        

class Bushes(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(bottomleft=pos)
        
        self.rect.x -= 32
        self.rect.y += 10

        self.hitbox = self.rect.inflate(-20,-30)
        
        self.sprite_type = "bushes"

        self.layout_level = 1


class Rocks(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(bottomleft=pos)

        self.rect.x -= 32
        self.rect.y += 10

        self.hitbox = self.rect.inflate(-25,-25)
        
        self.sprite_type = "rocks"

        self.layout_level = 1


class World:
    def __init__(self):
        path_map = "../maps/test_map/tmx/map.tmx"
        self.gameMap = pytmx.load_pygame(path_map)

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.list_ground_tiles = []
        
        self.create_map()

        get_random_tile_spawn_player = random.choice(self.list_ground_tiles)
        self.player = Player(get_random_tile_spawn_player.center, self.obstacle_sprites, self.visible_sprites)


    def create_map(self):
        layout = {
            "map_ground": import_layout_csv("../maps/test_map/csv/map_ground.csv"),
            "map_boundaries": import_layout_csv("../maps/test_map/csv/map_boundaries.csv"),
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESET_SIZE
                        y = row_index * TILESET_SIZE

                        if style == "map_boundaries":
                            Tile(pygame.Surface((TILESET_SIZE,TILESET_SIZE)), (x,y), self.obstacle_sprites,"invisible",0)

                        if style == "map_ground":
                            self.list_ground_tiles.append(pygame.Rect(x, y, TILESET_SIZE, TILESET_SIZE))

        self.generate_trees()
        self.generate_bushes()
        self.generate_rocks()
        self.generate_animals()


    def generate_trees(self):
        random_number_to_generate = random.randint(80, 90)

        for _ in range(random_number_to_generate):
            get_random_tile = random.choice(self.list_ground_tiles)
            Tree(get_random_tile.bottomleft, [self.visible_sprites, self.obstacle_sprites], 2)


    def generate_bushes(self):
        random_number_to_generate = random.randint(50, 60)
    
        for _ in range(random_number_to_generate):
            get_random_tile = random.choice(self.list_ground_tiles)
            random_number_image = random.randint(7, 11)


            image_to_load = f"../assets/tileset/Deco/{random_number_image:02d}.png"
            image_surface = pygame.image.load(image_to_load)

            Bushes(image_surface, get_random_tile.center, [self.visible_sprites])


    def generate_rocks(self):
        random_number_to_generate = random.randint(5, 10)
        
        for _ in range(random_number_to_generate):
            get_random_tile = random.choice(self.list_ground_tiles)
            random_number_image = random.randint(4, 6)

            path_image_to_load = f"../assets/tileset/Deco/{random_number_image:02d}.png"
            image_surface = pygame.image.load(path_image_to_load)

            Rocks(image_surface, get_random_tile.center, [self.visible_sprites, self.obstacle_sprites])

    
    def generate_animals(self):
        random_number_to_generate = random.randint(60, 70)

        for _ in range(random_number_to_generate):
            get_random_tile = random.choice(self.list_ground_tiles)
            Animal(get_random_tile.center, [self.visible_sprites, self.obstacle_sprites])

    def draw_map(self):
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load("../maps/test_map/png/map.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        
    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        sorted_sprites_by_y = sorted(self.sprites(), key=lambda sprite: sprite.hitbox.bottomleft[1])

        for sprite in sorted_sprites_by_y:

            try:
                offset_hitbox = sprite.hitbox.topleft - self.offset
                new_rect = pygame.Rect(offset_hitbox, sprite.hitbox.size)
                pygame.draw.rect(self.display_surface, "red", new_rect)
            except AttributeError: pass

            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

                



# TODO: adjust spawn trees