import pytmx
import pygame
from project.code.player import Player
from project.code.utils import import_layout_csv, import_folder
import random

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
        self.old_rect = self.rect.copy()

        self.hitbox = self.rect.inflate(-155, -40)

        self.hitbox.y += 130
        self.hitbox.height -= 125

        self.sprite_type = "tree"

        self.layout_level = layout_level


class World:
    def __init__(self):
        path_map = "../maps/test_map/tmx/map.tmx"
        self.gameMap = pytmx.load_pygame(path_map)

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.list_ground_tiles = []
        
        self.create_map()

        self.player = Player((100, 100), self.obstacle_sprites, self.visible_sprites)


    def create_map(self):
        layout = {
            "map_ground": import_layout_csv("../maps/test_map/csv/map_ground.csv"),
            "map_boundaries": import_layout_csv("../maps/test_map/csv/map_boundaries.csv"),
        }

        graphic = {
            "grass": import_folder("../assets/tileset/terrain_single_images"),
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        TILESET_SIZE = 64

                        x = col_index * TILESET_SIZE
                        y = row_index * TILESET_SIZE

                        if style == "map_boundaries":
                            Tile(pygame.Surface((TILESET_SIZE,TILESET_SIZE)), (x,y), self.obstacle_sprites,"invisible",0)

                        if style == "map_ground":
                            self.list_ground_tiles.append(pygame.Rect(x, y, TILESET_SIZE, TILESET_SIZE))

        self.generate_trees()


    def generate_trees(self):
        random_number_to_generate = random.randint(10, 20)
        for _ in range(random_number_to_generate):
            get_random_tile = random.choice(self.list_ground_tiles)
            Tree(get_random_tile.center, [self.visible_sprites, self.obstacle_sprites], 2)


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


        for sprite in self.sprites():
            if sprite.sprite_type != "invisible":
                offset_position = sprite.rect.topleft - self.offset

                offset_hitbox = sprite.hitbox.topleft - self.offset
                new_rect = pygame.Rect(offset_hitbox, sprite.hitbox.size)
                pygame.draw.rect(self.display_surface, "red", new_rect)
                
                self.display_surface.blit(sprite.image, offset_position)



# TODO: adjust spawn trees