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
        "armory": [],
        "gold": 0
    }

    def __init__(self):
        size = (600, 400)
        pos = (450, 200)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

    def draw(self, screen, font):
        title = font.render("Inventory", True, "white")
        pygame.draw.rect(screen, "black", self.rect)
        screen.blit(title, (self.rect.x+20, self.rect.y+20))

    def show_items(self, screen, font):
        actual_y_pos = self.rect.y
        for key, value in self.INVENTORY.items():
            text = font.render(f"{key} = {value}", True, "white")
            screen.blit(text, (self.rect.x+20, actual_y_pos+80))
            actual_y_pos += 20