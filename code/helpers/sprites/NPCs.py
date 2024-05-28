import pygame
from helpers.inventory import Inventory
from helpers.utils import update_list_actions_to_display
from helpers.objects import *
import random

# Gildermont = vendor weapons
# Murwood = vendor armors

NPCs_sprite_group = pygame.sprite.Group()

class NPC_base:

    class Area_interaction(pygame.sprite.Sprite):
        def __init__(self, center_NPC_pos):
            super().__init__()

            self.rect = pygame.Rect(center_NPC_pos[0]-20, center_NPC_pos[1]-20, 40, 40)


    def __init__(self):
        self.image = self.IMAGE
        self.rect = self.image.get_rect(center=self.POS_CENTER)
        self.image.fill("pink")

        self.type = self.TYPE


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


    def interaction_section(self, PLAYER, screen, font, font2, size_window_y):
        rect_area = self.Area_interaction(self.rect.center)

        if rect_area.rect.colliderect(PLAYER.rect):
            events = pygame.event.get()

            items_in_exchange, dict_rect_item_deal = self.draw_interaction_section(screen, font, font2, size_window_y)
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point_mouse = pygame.mouse.get_pos()

                    for key, value in dict_rect_item_deal.items():

                        clicked_button_deal_check = value.collidepoint(point_mouse)

                        if clicked_button_deal_check:
                            item_to_buy = key
                            cost = items_in_exchange[key]["cost"]
                            value = items_in_exchange[key]["type"]

                            if Inventory.INVENTORY[value] >= cost:
                                Inventory.INVENTORY[value] -= cost
                                Inventory.INVENTORY[self.TYPE].append(item_to_buy)
                                
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

        dict_rect_item_deal = {}

        for key, value in items_in_exchange.items():
            item_listed = font.render(f"{key} = {value['cost']} {value['type']}", True, "white")
            screen.blit(item_listed, (rect_dialogue.topleft[0]+10, start_y_row))

            rect_button_deal = pygame.Rect(rect_dialogue.topleft[0]+150, start_y_row, 30, 15)
            pygame.draw.rect(screen, "green", rect_button_deal)
            screen.blit(text_button_deal, (rect_button_deal.topleft[0]+5, rect_button_deal[1]))

            start_y_row += 20
            dict_rect_item_deal[key] = rect_button_deal

        return items_in_exchange, dict_rect_item_deal    


class Gildermont(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (538, 310)
    TYPE = "weapons"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

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
    

class Murwood(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (422, 398)
    TYPE = "armors"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

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