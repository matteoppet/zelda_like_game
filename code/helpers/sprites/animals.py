import pygame
import random
import math
import numpy as np


spawns = [
    (105, 147),
    (1409, 150),
]
DEFAULT_DISTANCE_COLLISION = 999
sensors_data = {
        "1": {"start_pos": None, "end_pos": None, "angle": 0, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "2": {"start_pos": None, "end_pos": None, "angle": 45, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "3": {"start_pos": None, "end_pos": None, "angle": 90, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "4": {"start_pos": None, "end_pos": None, "angle": 135, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "5": {"start_pos": None, "end_pos": None, "angle": 180, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "6": {"start_pos": None, "end_pos": None, "angle": 225, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "7": {"start_pos": None, "end_pos": None, "angle": 270, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
        "8": {"start_pos": None, "end_pos": None, "angle": 315, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION}
    }
LINE_LENGTH = 200

class Base_animal:
    def __init__(self):
        super().__init__()
        pos = (0,0)

        self.image = pygame.Surface((15, 10))
        self.image.fill("pink")
        self.rect = self.image.get_rect(topleft=pos)

        self.health = 50


    def actions(self, action):
        if action == 0:
            # move up
            self.rect.y -= 1
        elif action == 1:
            # move down 
            self.rect.y += 1
        elif action == 2:
            # move left
            self.rect.x -= 1
        elif action == 3:
            # move right
            self.rect.x += 1


    def collisions_in_gym(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
            
    
    def target_reached(self, target_point):
        temp_rect = pygame.Rect(target_point[0], target_point[1], 10, 10)

        if self.rect.colliderect(temp_rect):
            return True
        
    
    def random_position_spawn(self, size_window):
        x = np.random.randint(size_window[0])
        y = np.random.randint(size_window[1])

        return (x,y)


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


    def check_collision_sensors(self, obstacles):
        for sensor in sensors_data:
            start_sensor = sensors_data[sensor]["start_pos"]
            end_sensor = sensors_data[sensor]["end_pos"]

            start_sensor = (
                start_sensor[0]+(self.rect.width/2), 
                start_sensor[1]+(self.rect.height/2))

            for obstacle in obstacles:
                points_collision = obstacle.rect.clipline(start_sensor, end_sensor)

                if points_collision:
                    coord = points_collision[0]

                    distance = np.linalg.norm(
                        np.array([*start_sensor]) - np.array([*coord]))

                    sensors_data[sensor]["point_of_collision"] = coord
                    sensors_data[sensor]["distance_collision"] = distance


class Animals(Base_animal, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        sprite_spawn = random.choice(spawns)
        x = random.randint(sprite_spawn[0]-60, sprite_spawn[0]+60)
        y = random.randint(sprite_spawn[1]-60, sprite_spawn[1]+60)
        POS = (x,y)
        
        self.image = pygame.Surface((15, 10))
        self.rect = self.image.get_rect(topleft=POS)



animals_sprite = pygame.sprite.Group()
def spawn_animals():
    sprite_animal = Animals()
    animals_sprite.add(sprite_animal)