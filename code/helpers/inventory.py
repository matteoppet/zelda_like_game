import pygame

class Button_to_open_inventory:
    def __init__(self):
        self.image = pygame.Surface((55, 30))
        self.rect = self.image.get_rect(topleft=(20, 900))
        self.image.fill("black")


class Inventory:
    INVENTORY = {
        "wood": 0,
        "food": 0,
        "weapons": [],
        "armors": [],
        "gold": 0
    }

    def __init__(self):
        size = (600, 400)
        pos = (550, 200)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

        width_rect = 230
        self.rect_character = pygame.Rect(self.rect.x-width_rect-10, self.rect.y, width_rect, self.rect.height)

        self.inventory_equip_buttons = {}
        self.character_unequip_buttons = {}


    def draw_inventory(self, screen, font, font_2):
        pygame.draw.rect(screen, "black", self.rect)

        # draw buttons
        start_y_pos_buttons = self.rect.y+20
        for button in self.inventory_equip_buttons.values():
            button.size = (35, 15)
            button.topleft = (self.rect.topright[0]-button.width-20, start_y_pos_buttons)

            pygame.draw.rect(screen, "green", button)

            font_equip_text = font_2.render("equip", True, "black")
            screen.blit(font_equip_text, (button.topleft[0]+5, button.topleft[1]))

            start_y_pos_buttons += 25
        
        # draw items
        start_y_pos_items = self.rect.y+20
        for key, value in self.INVENTORY.items():
            items_text = font.render(f"{key} = {value}", True, "white")
            screen.blit(items_text, (self.rect.x+20, start_y_pos_items))

            start_y_pos_items += 25

    def functionality_inventory(self):
        for key, value in self.INVENTORY.items():
            equip_button = pygame.Rect(0, 0, 0, 0)
            
            self.inventory_equip_buttons[key] = equip_button



    def draw_character(self, screen, player, font, font_2):
        pygame.draw.rect(screen, "black", self.rect_character)

        # draw buttons
        start_y_pos_buttons = self.rect_character.y+20
        for button in self.character_unequip_buttons.values():
            button.size = (47, 15)
            button.topleft = (self.rect_character.topright[0]-button.width-20, start_y_pos_buttons)

            pygame.draw.rect(screen, "red", button)

            font_equip_text = font_2.render("unequip", True, "black")
            screen.blit(font_equip_text, (button.topleft[0]+5, button.topleft[1]))

            start_y_pos_buttons += 25

        # draw items
        start_y_pos_items = self.rect_character.y+20
        for key, value in player.EQUIPMENT.items():
            items_text = font.render(f"{key} = {value}", True, "white")
            screen.blit(items_text, (self.rect_character.x+20, start_y_pos_items))

            start_y_pos_items += 25

    
        # TODO: fix armors text and unequip buttons 
    

    def functionality_character(self, player):
        for key, value in player.EQUIPMENT.items():
            unequip_button = pygame.Rect(0, 0, 0, 0)
            
            self.character_unequip_buttons[key] = unequip_button



    def check_button_activity(self, point_mouse, player):
        if self.rect.collidepoint(point_mouse):
            for key, button in self.inventory_equip_buttons.items():

                if button.collidepoint(point_mouse):
                    self.equip_system(key, player)

        elif self.rect_character.collidepoint(point_mouse):
            for key, button in self.character_unequip_buttons.items():

                if button.collidepoint(point_mouse):
                    self.unequip_system(key, player)


    def equip_system(self, class_item, player):
        if class_item in ["armors", "weapons"]:
            items = self.INVENTORY[class_item]

            try:
                item = items[0] # take the first item in the list

                player.EQUIPMENT[class_item] = item
                self.INVENTORY[class_item].remove(item)

            except IndexError: pass

    
    def unequip_system(self, class_item, player):
        items = player.EQUIPMENT[class_item]

        if isinstance(items, list):
            item = items[0]
            player.EQUIPMENT[class_item].remove(item)

        else:
            item = player.EQUIPMENT[class_item]
            player.EQUIPMENT[class_item] = "hands"

        self.INVENTORY[class_item].append(item)
