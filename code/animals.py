import pygame
import random
import math
import numpy as np


class Animal(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        path_to_image = "../assets/tileset/Resources/Sheep/single_sheep_image.png"
        self.image = pygame.image.load(path_to_image)
        self.rect = self.image.get_rect(center=pos)

        self.rect.x += 30
        self.rect.y -= 40

        self.hitbox = self.rect.inflate(-85,-95)

        self.sprite_type = "animal"




# DEFAULT_DISTANCE_COLLISION = 999
# sensors_data = {
#         "1": {"start_pos": None, "end_pos": None, "angle": 0, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "2": {"start_pos": None, "end_pos": None, "angle": 45, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "3": {"start_pos": None, "end_pos": None, "angle": 90, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "4": {"start_pos": None, "end_pos": None, "angle": 135, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "5": {"start_pos": None, "end_pos": None, "angle": 180, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "6": {"start_pos": None, "end_pos": None, "angle": 225, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "7": {"start_pos": None, "end_pos": None, "angle": 270, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION},
#         "8": {"start_pos": None, "end_pos": None, "angle": 315, "point_of_collision": None, "distance_collision": DEFAULT_DISTANCE_COLLISION}
#     }


    # def sensors_position_update(self):
    #     for sensor in sensors_data: 
    #         start_pos = self.rect.center
    #         angle = sensors_data[sensor]["angle"]

    #         end_pos = (
    #             start_pos[0] + math.cos(math.radians(-angle)) * LINE_LENGTH,
    #             start_pos[1] + math.sin(math.radians(-angle)) * LINE_LENGTH
    #         )
    #         sensors_data[sensor]["start_pos"] = start_pos
    #         sensors_data[sensor]["end_pos"] = end_pos


    # def draw_sensors(self, screen):
    #     for sensor in sensors_data:
    #         pygame.draw.line(screen, "white", sensors_data[sensor]["start_pos"], sensors_data[sensor]["end_pos"])


    # def check_collision_sensors(self, obstacles):
    #     for sensor in sensors_data:
    #         start_sensor = sensors_data[sensor]["start_pos"]
    #         end_sensor = sensors_data[sensor]["end_pos"]

    #         start_sensor = (
    #             start_sensor[0]+(self.rect.width/2), 
    #             start_sensor[1]+(self.rect.height/2))

    #         collisions = {}
    #         for obstacle in obstacles:
    #             points_collision = obstacle.rect.clipline(start_sensor, end_sensor)

    #             if points_collision:
    #                 coord = points_collision[0]

    #                 distance = np.linalg.norm(
    #                     np.array([*start_sensor]) - np.array([*coord]))

    #                 collisions[distance] = coord



    #                 sensors_data[sensor]["point_of_collision"] = coord
    #                 sensors_data[sensor]["distance_collision"] = distance

    #         if collisions != {}:
    #             collision_lessfar = min(collisions)
    #             point_of_collision = collisions[collision_lessfar]

    #             sensors_data[sensor]["point_of_collision"] = point_of_collision
    #             sensors_data[sensor]["distance_collision"] = distance
    #         else:
    #             sensors_data[sensor]["point_of_collision"] = None
    #             sensors_data[sensor]["distance_collision"] = DEFAULT_DISTANCE_COLLISION
                