import pygame
import random
from ...data import enemies_data
import numpy as np
import math


enemies_sprite = pygame.sprite.Group()


class Enemie(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups):
        super().__init__(groups)

        self.image = enemies_data[name]["graphic"]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        # movements
        self.status = "idle"
        self.speed = enemies_data[name]["speed"]

        # combat
        self.damage = enemies_data[name]["damage"]
        self.defense = enemies_data[name]["defense"]
        self.cooldown = enemies_data[name]["cooldown"]
        self.attack_radius = enemies_data[name]["attack_radius"]

        # stats
        self.health = enemies_data[name]["health"]

        # others
        self.name = name
