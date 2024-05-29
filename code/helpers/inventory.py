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
        self.character_items_equipped_pos = {}


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
        
        # draw items
        start_y_pos_items = self.rect_character.y+20
        for class_type, items in player.EQUIPMENT.items():

            if isinstance(items, dict): # verify that items is a dictionary
                class_type_text = font.render(f"{class_type}: ", True, "white")
                screen.blit(class_type_text, (self.rect_character.x+20, start_y_pos_items))

                for part, equipped in items.items():
                    start_y_pos_items += 25

                    pos_to_draw = (self.rect_character.x+20, start_y_pos_items) # save position to draw
                    single_item_text = font.render(f"> {part}: {equipped}", True, "white") # initialize the text
                    screen.blit(single_item_text, pos_to_draw) # draw on the screen
                    self.character_items_equipped_pos[part] = pos_to_draw # save in the dictionary

            else:
                start_y_pos_items += 25
                pos_to_draw = (self.rect_character.x+20, start_y_pos_items)
                item_text = font.render(f"{class_type}: {items}", True, "white")
                screen.blit(item_text, pos_to_draw)

                self.character_items_equipped_pos[class_type] = pos_to_draw 


        # draw buttons
        for class_type, pos in self.character_items_equipped_pos.items():
            try:
                button = self.character_unequip_buttons[class_type]
                button.topleft = (self.rect_character.topright[0]-button.width-20, pos[1])
                self.character_unequip_buttons[class_type] = button

                pygame.draw.rect(screen, "red", button)

                text_button = font_2.render("unequip", True, "black")
                screen.blit(text_button, (button.topleft[0]+5, button.topleft[1]))
            except KeyError:
                pass


    
    def functionality_character(self, player):
        for item, pos in self.character_items_equipped_pos.items():
            unequip_button = pygame.Rect(pos, (47, 15))
            self.character_unequip_buttons[item] = unequip_button


    def check_button_activity(self, point_mouse, player):

        if self.rect.collidepoint(point_mouse):
            for key, button in self.inventory_equip_buttons.items():

                if button.collidepoint(point_mouse):
                    self.equip_system(key, player)

        elif self.rect_character.collidepoint(point_mouse):
            print(self.character_unequip_buttons)
            for key, button in self.character_unequip_buttons.items():
                if button.collidepoint(point_mouse):
                    self.unequip_system(key, player)


    def equip_system(self, class_item, player):
        if class_item in ["armors", "weapons"]:
            items = self.INVENTORY[class_item]

            try:
                if class_item == "armors":
                    item = items[0]
                    player.EQUIPMENT["armors"][item] = item
                else:
                    item = items[0]
                    player.EQUIPMENT[class_item] = item

                self.INVENTORY[class_item].remove(item)
            except IndexError: pass

    
    def unequip_system(self, value, player):

        if value in player.EQUIPMENT["armors"]:
            if player.EQUIPMENT["armors"][value] != None:
                player.EQUIPMENT["armors"][value] = None
                self.INVENTORY["armors"].append(value)

        else:
            item = player.EQUIPMENT[value]
            player.EQUIPMENT[value] = "hands"

            if item != "hands":
                self.INVENTORY[value].append(item)



# fix unequip buttons