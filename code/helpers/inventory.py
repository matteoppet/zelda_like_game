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
        "weapon": [],
        "armor": [],
        "gold": 0
    }

    def __init__(self):
        size = (600, 400)
        pos = (550, 200)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

        width_rect = 200
        self.rect_character = pygame.Rect(self.rect.x-width_rect-10, self.rect.y, width_rect, self.rect.height)

        self.all_buttons = {}


    def draw(self, screen, font):
        title = font.render("Inventory", True, "white")
        pygame.draw.rect(screen, "black", self.rect)
        pygame.draw.rect(screen, "black", self.rect_character)
        screen.blit(title, (self.rect.x+20, self.rect.y+20))


    def show_items(self, screen, font, font_2, player):
        actual_y_pos = self.rect.y
        for key, value in self.INVENTORY.items():
            text = font.render(f"{key} = {value}", True, "white")
            screen.blit(text, (self.rect.x+20, actual_y_pos+80))

            rect_button_equip = pygame.Rect(self.rect.x+150, actual_y_pos+80, 35, 15)
            pygame.draw.rect(screen, "green", rect_button_equip)
            text_equip_button = font_2.render("equip", True, "black")
            screen.blit(text_equip_button, (rect_button_equip.topleft[0]+5, rect_button_equip.topleft[1]))

            self.all_buttons[key] = rect_button_equip

            actual_y_pos += 20


    def show_character(self, screen, player, font, font_2):
        start_item_y = self.rect_character.y+20
        start_item_x = self.rect_character.x+20
        for item_equipped in player.EQUIPMENT:
            text = font.render(f"{item_equipped}: {player.EQUIPMENT[item_equipped]}", True, "white")
            screen.blit(text, (start_item_x, start_item_y))

            rect_button_unequip = pygame.Rect(start_item_x+130, start_item_y, 45, 15)
            pygame.draw.rect(screen, "red", rect_button_unequip)
            text_unequip_button = font_2.render("unequip", True, "black")
            screen.blit(text_unequip_button, (rect_button_unequip.topleft[0]+3, rect_button_unequip.topleft[1]))

            self.all_buttons[item_equipped] = rect_button_unequip

            start_item_y += 20


    def equip_item(self, class_item, player):
        items = self.INVENTORY[class_item]

        if isinstance(items, list):
            player.EQUIPMENT[class_item.capitalize()] = items[0]
            self.INVENTORY[class_item].remove(items[0])


    def unequip_item(self, class_item, player):
        item_equipped = player.EQUIPMENT[class_item]

        self.INVENTORY[class_item.lower()].append(item_equipped)
        player.EQUIPMENT[class_item] = "Hands"


    def check_click_button(self, player):
        events = pygame.event.get()
        for class_item, rect_button in self.all_buttons.items():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if rect_button.collidepoint(point):
                        
                        # temporary solution:
                        if rect_button.x > 500:
                            # inventory
                            self.equip_item(class_item, player)
                        else:
                            # equipped
                            self.unequip_item(class_item, player)