from helpers.obstacles import create_obstacles, obstacle_sprites
from helpers.sprites import create_animals, animal_sprites

class World:
    def __init__(self):
        ...

    
    def init_obstacles(self):
        create_obstacles()
        return obstacle_sprites
    
    def init_animals(self):
        create_animals()
        return animal_sprites