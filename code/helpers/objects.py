import pygame

""" 
Object in game:
    - Weapons = ["Knife", "Axe", "sword"]
    - Armors = ["Chest", "Helmet", "Gloves"]
    - Foods = ["Apple", "Banana", "Meat"]
"""


class Armors:
    types = ["chest", "helmet", "gloves"]


class Weapons:
    types = ["knife", "axe", "sword"]

    def hands(self):
        return {"damage": 0, "velocity": 0, "damage_trees": 0}

    def axe(self):
        return {"damage": 0, "velocity": 0, "damage_trees": 0}

    def knife(self):
        return {"damage": 0, "velocity": 0, "damage_trees": 0}
    
    def spade(self):
        return {"damage": 0, "velocity": 0, "damage_trees": 0}


class Foods:
    def __init__(self):
        ...