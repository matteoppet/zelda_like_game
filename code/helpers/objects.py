


class Armors:
    types = {
        "Chest": 0,
        "Helmet": 0,
        "Gloves": 0
    }


class Weapons:
    types = {
        "Hands": {"damage": 5, "velocity": 1, "damage_trees": 5},
        "Axe": {"damage": 15, "velocity": 3, "damage_trees": 20},
        "Knife": {"damage": 0, "velocity": 0, "damage_trees": 0},
        "Spade": {"damage": 0, "velocity": 0, "damage_trees": 0}
    }


class Foods:
    def __init__(self):
        ...