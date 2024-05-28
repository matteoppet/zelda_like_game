


class Armors:
    types = {
        "Helmet": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "Chest": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "Pants": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "Shoes": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"},
        "Gloves": {"health": 0, "protection": 0, "cost": 0, "type": "wood", "class": "armors"}
    }


class Weapons:
    types = {
        "Hands": {"damage": 2, "velocity": 1, "damage_trees": 5, "cost": 0, "type": None, "class": "weapons"},
        "Axe": {"damage": 15, "velocity": 4, "damage_trees": 20, "cost": 15, "type": "wood", "class": "weapons"},
        "Knife": {"damage": 3, "velocity": 2, "damage_trees": 10, "cost": 10, "type": "wood", "class": "weapons"},
        "Spade": {"damage": 10, "velocity": 3, "damage_trees": 5, "cost": 25, "type": "wood", "class": "weapons"}
    }


class Foods:
    def __init__(self):
        ...