


class Armors:
    types = {
        "Helmet": {"health": 0, "protection": 0},
        "Chest": {"health": 0, "protection": 0},
        "Pants": {"health": 0, "protection": 0},
        "Shoes": {"health": 0, "protection": 0},
        "Gloves": {"health": 0, "protection": 0}
    }


class Weapons:
    types = {
        "Hands": {"damage": 2, "velocity": 1, "damage_trees": 5},
        "Axe": {"damage": 15, "velocity": 4, "damage_trees": 20},
        "Knife": {"damage": 3, "velocity": 2, "damage_trees": 10},
        "Spade": {"damage": 10, "velocity": 3, "damage_trees": 5}
    }


class Foods:
    def __init__(self):
        ...