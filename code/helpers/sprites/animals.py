import pygame
import random
import math


spawns = [
    (105, 147),
    (1409, 150),
]
sensors_data = {
        "1": {"start_pos": None, "end_pos": None, "angle": 0},
        "2": {"start_pos": None, "end_pos": None, "angle": 45},
        "3": {"start_pos": None, "end_pos": None, "angle": 90},
        "4": {"start_pos": None, "end_pos": None, "angle": 135},
        "5": {"start_pos": None, "end_pos": None, "angle": 180},
        "6": {"start_pos": None, "end_pos": None, "angle": 225},
        "7": {"start_pos": None, "end_pos": None, "angle": 270},
        "8": {"start_pos": None, "end_pos": None, "angle": 315}
    }
LINE_LENGTH = 200

class Base_animal:
    def __init__(self):
        super().__init__()
        pos = (0,0)

        self.image = pygame.Surface(self.IMAGE)
        self.image.fill("pink")
        self.rect = self.image.get_rect(topleft=pos)

        self.health = 50

    def sensors_position_update(self):
        for sensor in sensors_data: 
            start_pos = self.rect.center
            angle = sensors_data[sensor]["angle"]

            end_pos = (
                start_pos[0] + math.cos(math.radians(-angle)) * LINE_LENGTH,
                start_pos[1] + math.sin(math.radians(-angle)) * LINE_LENGTH
            )
            sensors_data[sensor]["start_pos"] = start_pos
            sensors_data[sensor]["end_pos"] = end_pos

    def draw_sensors(self, screen):
        for sensor in sensors_data:
            pygame.draw.line(screen, "white", sensors_data[sensor]["start_pos"], sensors_data[sensor]["end_pos"])

class Animals(Base_animal, pygame.sprite.Sprite):
    IMAGE = (15, 10)


    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        sprite_spawn = random.choice(spawns)
        x = random.randint(sprite_spawn[0]-60, sprite_spawn[0]+60)
        y = random.randint(sprite_spawn[1]-60, sprite_spawn[1]+60)
        POS = (x,y)

        self.rect = self.image.get_rect(topleft=POS)



animals_sprite = pygame.sprite.Group()
def spawn_animals():
    sprite_animal = Animals()
    animals_sprite.add(sprite_animal)