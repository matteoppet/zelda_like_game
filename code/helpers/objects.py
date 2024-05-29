


class Armors:
    types = {
        "helmet": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "chest": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "pants": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "shoes": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
    }


class Weapons:
    types = {
        "hands": {"damage": 2, "velocity": 1, "damage_trees": 5, "cost": 0, "type": None, "class": "weapons"},
        "axe": {"damage": 15, "velocity": 4, "damage_trees": 20, "cost": 15, "type": "wood", "class": "weapons"},
        "knife": {"damage": 3, "velocity": 2, "damage_trees": 10, "cost": 10, "type": "wood", "class": "weapons"},
        "spade": {"damage": 10, "velocity": 3, "damage_trees": 5, "cost": 25, "type": "wood", "class": "weapons"}
    }


class Foods:
    def __init__(self):
        ...