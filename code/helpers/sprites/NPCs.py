import pygame
from helpers.inventory import Inventory
from helpers.utils import update_list_actions_to_display
from helpers.objects import *
import random

# Gildermont = vendor weapons
# Murwood = vendor armors

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

            items_in_exchange, rect_button_deal = self.draw_interaction_section(screen, font, font2, size_window_y)
            
            rect_mouse = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button_deal_check = rect_button_deal.colliderect(rect_mouse)
                    if clicked_button_deal_check:

                        for key, value in items_in_exchange.items():
                            if Inventory.INVENTORY["wood"] >= value:
                                Inventory.INVENTORY["wood"] -= value
                                Inventory.INVENTORY[self.TYPE].append(key)
                                
                                update_list_actions_to_display(f"You have bought: {key} for {value} wood")
                            else:
                                update_list_actions_to_display(f"You don't have enought wood for: {key}")


    def draw_interaction_section(self, screen, font, font2, size_window_y):
        # Text dialogue
        text_dialogue = self.dialogue()
        text_to_render = font.render(text_dialogue, True, "white")
        
        # Rect dialogue
        rect_dialogue = pygame.Rect(10, size_window_y/2-100, 250, 200)
        pygame.draw.rect(screen, "black", rect_dialogue)
        screen.blit(text_to_render, (rect_dialogue.x+10, rect_dialogue.y+10))

        # Button deal
        text_button_deal = font2.render("Accept", True, "black") 
        rect_button_deal = pygame.Rect(rect_dialogue.bottomright[0]-40, rect_dialogue.bottomright[1]-20, 35, 15)
        pygame.draw.rect(screen, "green", rect_button_deal)
        screen.blit(text_button_deal, (rect_button_deal.topleft[0], rect_button_deal[1]))

        # List item in exchange
        items_in_exchange = self.items_in_exchange()
        for key, value in items_in_exchange.items():
            item_value_exchange = font.render(f"{key} = {value} wood", True, "white")
            screen.blit(item_value_exchange, (rect_dialogue.topleft[0]+10, rect_dialogue.topleft[1]+50))

        return items_in_exchange, rect_button_deal    


class Gildermont(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (538, 310)
    TYPE = "weapon"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.item_to_sell = random.choice(Weapons.types)


    def dialogue(self):
        return "Hello Mr.., I'm Gildermont."
    
    def items_in_exchange(self):
        return {self.item_to_sell: 10} # 10 wood
    

class Murwood(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (422, 398)
    TYPE = "armor"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.item_to_sell = random.choice(Armors.types)

    def dialogue(self):
        return "Hello Mr.., I'm Murwood."
    
    def items_in_exchange(self):
        return {self.item_to_sell: 20} # 20 wood
    

NPCs_sprite_group = pygame.sprite.Group()