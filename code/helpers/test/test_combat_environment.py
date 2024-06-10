import pygame
from ...data import weapon_data

class Combat_Environment:
    def __init__(self, player, enemie_sprites):
        player.data["equipment"]["weapons"] = "spade"

        self.font = pygame.font.Font("../assets/font/arial/ARIAL.TTF", 20)

        self.enemie_sprites = enemie_sprites
        self.enemie = self.enemie_sprites.sprites()[0]

        self.PLAYER = player

    def draw(self, screen, bg):
        # draw enemy
        self.enemie_sprites.draw(screen, bg)

        # draw player
        screen.blit(self.PLAYER.image, self.PLAYER.rect)

        # information panel
        weapon_equipped = self.font.render(f"Weapon: {self.PLAYER.data['equipment']['weapons']}", False, "black")
        screen.blit(weapon_equipped, (100, 100))
        
        health_player = self.font.render(f"Health player: {self.PLAYER.health}", False, "black")
        screen.blit(health_player, (100, 130))

        health_enemie = self.font.render(f"Health enemie: {self.enemie.health}", False, "black")
        screen.blit(health_enemie, (100, 160))

        level_enemie = self.font.render(f"Level enemie: {self.enemie.name}", False, "black")
        screen.blit(level_enemie, (100, 190))
        
        damage_weapon_calc = weapon_data[self.PLAYER.data["equipment"]["weapons"]]["damage"] - self.enemie.defense
        damage_weapon = self.font.render(f"({damage_weapon_calc})", False, "black")
        screen.blit(damage_weapon, (280, 160))
        
        start_y = 250
        for k,v in self.PLAYER.data['equipment']['armors'].items():
            armor_equipped = self.font.render(f"Armor equipped: {k} > {v}", False, "black")
            screen.blit(armor_equipped, (100, start_y))

            start_y += 30

        # all the variables changes with the enemie, if the enemie die, respawn and reset all variables



# armi potenti che puoi usare in base alla forza DONE

# costituzione puoi usare armature più potenti cioè piu pesanti TODO 

# creare il livello system TODO 

# make the inventory that you can see skills level etc TODO 