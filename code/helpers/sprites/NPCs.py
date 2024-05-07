import pygame

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

    def interaction_section(self, PLAYER, screen, font, size_window_y):
        rect_area = self.Area_interaction(self.rect.center)

        if rect_area.rect.colliderect(PLAYER.rect):
            text_dialogue = self.dialogue()
            text_to_render = font.render(text_dialogue, True, "white")
            
            rect_dialogue = pygame.Rect(10, size_window_y/2-100, 300, 200)
            pygame.draw.rect(screen, "black", rect_dialogue)
            screen.blit(text_to_render, (rect_dialogue.x+10, rect_dialogue.y+10))
            


class Gildermont(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (600, 400)
    TYPE = "weapons"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

    def dialogue(self):
        return "Hello Mr.., I'm Gildermont."
    

class Murwood(NPC_base, pygame.sprite.Sprite):
    IMAGE = pygame.Surface((15, 25))
    POS_CENTER = (700, 400)
    TYPE = "armors"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()

    def dialogue(self):
        return "Hello Mr.., I'm Murwood."
    

NPCs_sprite_group = pygame.sprite.Group()