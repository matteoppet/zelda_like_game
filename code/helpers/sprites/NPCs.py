import pygame
from helpers.objects import *
import random
import numpy as np
from ..inventory import Inventory
from ..utils import update_list_actions_to_display

# Gildermont = vendor weapons
# Murwood = vendor armors


class NPC_base:
    def __init__(self):
        self.buttons_deal = {}

    def interaction_section(self, pos_mouse):
        items_in_exchange = self.items_in_exchange()
        for key, value in self.buttons_deal.items():
            button_clicked = value.collidepoint(pos_mouse)
            
            if button_clicked:
                item_to_buy = key
                cost = items_in_exchange[key]["cost"]
                value = items_in_exchange[key]["type"]

                if Inventory.INVENTORY[value] >= cost:
                    Inventory.INVENTORY[value] -= cost
                    Inventory.INVENTORY[self.type].append(item_to_buy)
                    
                    update_list_actions_to_display(f"You have bought: {item_to_buy} for {cost} {value}")
                else:
                    update_list_actions_to_display(f"You don't have enought {value} for: {item_to_buy}")



    def draw_interaction_section(self, screen, font, font2, size_window_y):
        # Text dialogue
        text_dialogue = self.dialogue()
        text_to_render = font.render(text_dialogue, True, "white")
        
        # Rect dialogue
        rect_dialogue = pygame.Rect(10, size_window_y/2-100, 250, 200)
        pygame.draw.rect(screen, "black", rect_dialogue)
        screen.blit(text_to_render, (rect_dialogue.x+10, rect_dialogue.y+10))


        items_in_exchange = self.items_in_exchange()
        start_y_row = rect_dialogue.topleft[1]+50
        text_button_deal = font2.render("Buy", True, "black")


        for key, value in items_in_exchange.items():
            item_listed = font.render(f"{key} = {value['cost']} {value['type']}", True, "white")
            screen.blit(item_listed, (rect_dialogue.topleft[0]+10, start_y_row))

            rect_button_deal = pygame.Rect(rect_dialogue.topleft[0]+150, start_y_row, 30, 15)
            pygame.draw.rect(screen, "green", rect_button_deal)
            screen.blit(text_button_deal, (rect_button_deal.topleft[0]+5, rect_button_deal[1]))

            start_y_row += 20
            self.buttons_deal[key] = rect_button_deal
        

        return items_in_exchange 
    

    def distance_from_vendor(self, PLAYER, sprite_vendor):
        distance_from_vendors = {}

        for sprite in sprite_vendor:
            distance = np.linalg.norm(np.array(sprite.rect.center) - np.array(PLAYER.rect.center))
            distance_from_vendors[distance] = sprite.type

        less_distance = min(distance_from_vendors.keys())

        if less_distance < 50:
            return distance_from_vendors[less_distance]
        else:
            return False


class Gildermont(NPC_base, pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.image = pygame.Surface((15, 25))
        self.rect = self.image.get_rect(center=(538, 310))
        self.image.fill("pink")

        self.type = "weapons"

        self.dict_sell = self.reload_items_on_sale()

    def reload_items_on_sale(self):
        list_items_avaible_to_sell = [key for key in Weapons.types.keys()]
        dict_items_on_sale = {}

        count = 0
        while count <= 2:
            random_item_picked = random.choice(list_items_avaible_to_sell)
            dict_items_on_sale[random_item_picked] = {"cost": Weapons.types[random_item_picked]["cost"], "type": Weapons.types[random_item_picked]["type"]}
            count += 1

        return dict_items_on_sale


    def dialogue(self):
        return "Hello Mr.., I'm Gildermont."
    

    def items_in_exchange(self):
        return self.dict_sell
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    

class Murwood(NPC_base, pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.image = pygame.Surface((15, 25))
        self.rect = self.image.get_rect(center=(422, 398))
        self.image.fill("pink")

        self.type = "armors"

        self.dict_sell = self.reload_items_on_sale()

    def reload_items_on_sale(self):
        list_items_avaible_to_sell = [key for key in Armors.types.keys()]
        dict_items_on_sale = {}

        count = 0
        while count <= 2:
            random_item_picked = random.choice(list_items_avaible_to_sell)
            dict_items_on_sale[random_item_picked] = {"cost": Armors.types[random_item_picked]["cost"], "type": Armors.types[random_item_picked]["type"]}
            count += 1

        return dict_items_on_sale

    def dialogue(self):
        return "Hello Mr.., I'm Murwood."
    
    def items_in_exchange(self):
        return self.dict_sell
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))