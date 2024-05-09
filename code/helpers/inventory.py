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

    def draw(self, screen, font):
        title = font.render("Inventory", True, "white")
        pygame.draw.rect(screen, "black", self.rect)
        screen.blit(title, (self.rect.x+20, self.rect.y+20))

    def show_items(self, screen, font, font_2):
        buttons_equip = {}
        actual_y_pos = self.rect.y
        for key, value in self.INVENTORY.items():
            text = font.render(f"{key} = {value}", True, "white")
            screen.blit(text, (self.rect.x+20, actual_y_pos+80))

            rect_button_equip = pygame.Rect(self.rect.x+150, actual_y_pos+80, 35, 15)
            pygame.draw.rect(screen, "green", rect_button_equip)
            text_equip_button = font_2.render("equip", True, "black")
            screen.blit(text_equip_button, (rect_button_equip.topleft[0]+5, rect_button_equip.topleft[1]))

            buttons_equip[key] = rect_button_equip

            actual_y_pos += 20



    def show_character(self, screen, EQUIPMENT, font):
        width_rect = 200
        rect_character = pygame.Rect(self.rect.x-width_rect-10, self.rect.y, width_rect, self.rect.height)
        pygame.draw.rect(screen, "black", rect_character)
        
        start_item_y = rect_character.y+20
        start_item_x = rect_character.x+20
        for item_equipped in EQUIPMENT:
            text = font.render(f"{item_equipped}: {EQUIPMENT[item_equipped]}", True, "white")
            screen.blit(text, (start_item_x, start_item_y))

            start_item_y += 20

        

    def equip_item(self):
        ...