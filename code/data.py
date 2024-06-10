import pygame

armor_data = {
    "helmet": {"health": 0, "protection": 0, "cost": 15, "type": "gold", "class": "armors"},
    "chest": {"health": 0, "protection": 0, "cost": 25, "type": "gold", "class": "armors"},
    "pants": {"health": 0, "protection": 0, "cost": 20, "type": "gold", "class": "armors"},
    "shoes": {"health": 0, "protection": 0, "cost": 10, "type": "gold", "class": "armors"},
}


weapon_data = {
    "hands": {"damage": 2, "velocity": 1, "speed": 5, "cost": 0, "type": None, "class": "weapons", "skill_required": {"strength": 10}},
    "axe": {"damage": 15, "velocity": 4, "speed": 5, "cost": 15, "type": "gold", "class": "weapons", "skill_required": {"strength": 10}},
    "knife": {"damage": 3, "velocity": 2, "speed": 5, "cost": 10, "type": "gold", "class": "weapons", "skill_required": {"strength": 10}},
    "spade": {"damage": 10, "velocity": 3, "speed": 5, "cost": 25, "type": "gold", "class": "weapons", "skill_required": {"strength": 0}}
}


enemies_data = {
    "zombie_l_01": {"health": 10, "damage": 10, "defense": 1, "cooldown": 2000, "xp": 10, "graphic": pygame.Surface((10,15)), "attack_type": "normal", "speed": 0.5, "attack_radius": 80, "alert_radius": 150},
    "zombie_l_02": {"health": 10, "damage": 15, "defense": 2, "cooldown": 2000, "xp": 15, "graphic": pygame.Surface((10, 20)), "attack_type": "normal", "speed": 0.5, "attack_radius": 80, "alert_radius": 150}
}
