


class Armors:
    types = {
        "helmet": {"health": 0, "protection": 0, "cost": 15, "type": "wood", "class": "armors"},
        "chest": {"health": 0, "protection": 0, "cost": 25, "type": "wood", "class": "armors"},
        "pants": {"health": 0, "protection": 0, "cost": 20, "type": "wood", "class": "armors"},
        "shoes": {"health": 0, "protection": 0, "cost": 10, "type": "wood", "class": "armors"},
    }


class Weapons:
    types = {
        "hands": {"damage": 2, "velocity": 1, "damage_trees": 5, "speed": 0, "cost": 0, "type": None, "class": "weapons"},
        "axe": {"damage": 15, "velocity": 4, "damage_trees": 20, "speed": 0, "cost": 15, "type": "wood", "class": "weapons"},
        "knife": {"damage": 3, "velocity": 2, "damage_trees": 10, "speed": 0, "cost": 10, "type": "wood", "class": "weapons"},
        "spade": {"damage": 10, "velocity": 3, "damage_trees": 5, "speed": 0, "cost": 25, "type": "wood", "class": "weapons"}
    }


# attack = damage_player - defense_zombie
class Types_of_enemies:
    types = {
        "zombie_l_01": {"health": 10, "damage": 10, "defense": 1, "cooldown": 2000, "size": (10, 15)},
        "zombie_l_02": {"health": 10, "damage": 15, "defense": 2, "cooldown": 2000, "size": (10, 20)}
    }


class Foods:
    def __init__(self):
        ...