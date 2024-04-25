from helpers.obstacles import create_obstacles, obstacle_sprites
from helpers.sprites import create_animals, animal_sprites

import pytmx

class World:
    def __init__(self):
        path_map = "../maps/test_map/tmx/map.tmx"
        self.gameMap = pytmx.load_pygame(path_map)

    def draw_map(self, screen):
        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                if(tile != None):
                    screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))
    
    def init_obstacles(self):
        create_obstacles()
        return obstacle_sprites
    
    def init_animals(self):
        create_animals()
        return animal_sprites