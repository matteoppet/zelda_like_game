import pytmx
import pygame
import random


ground_sprites = pygame.sprite.Group()
water_sprites = pygame.sprite.Group()
spawn_trees_sprites = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, pos, layer):
        super().__init__()

        self.layer = layer
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)

        self.old_rect = self.rect.copy()


class World:
    def __init__(self):
        path_map = "../maps/test_map/tmx/map.tmx"
        self.gameMap = pytmx.load_pygame(path_map)


    def create_map(self):
        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                if(tile != None):
                    
                    sprite = Tile(
                        size=(self.gameMap.tilewidth, self.gameMap.tileheight),
                        pos=(x * self.gameMap.tilewidth,y * self.gameMap.tileheight),
                        layer=layer)
                    
                    layer_name = layer.name
                    
                    if layer_name == "ground":
                        ground_sprites.add(sprite)
                    elif layer_name == "water": 
                        water_sprites.add(sprite)
                    elif layer_name == "spawn_trees":
                        spawn_trees_sprites.add(sprite)

    def draw_map(self, screen):
        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                if(tile != None):
                    screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))


tree_sprites = pygame.sprite.Group()
SIZE_TREE = (10, 40)
trees_spawn_position = []

class Trees(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center=pos)
        self.image.fill("brown")

        self.health = 80


def spawn_tree(list_ground_sprite):
    r = True
    while r:
        random_tile = random.choice(list_ground_sprite)

        if random_tile.rect.center in trees_spawn_position:
            random_tile = random.choice(list_ground_sprite)
        else:
            trees_spawn_position.append(random_tile.rect.center)

            sprite_tree = Trees(SIZE_TREE, random_tile.rect.center)
            tree_sprites.add(sprite_tree)
            r = False
            
