import pytmx
import pygame


ground_sprites = pygame.sprite.Group()
water_sprites = pygame.sprite.Group()


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

    def draw_map(self, screen):
        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                if(tile != None):
                    screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))
    

    def init_obstacles(self):
        create_obstacles()
        return obstacle_sprites
