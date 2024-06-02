import pygame 

class Home_screen:
    def __init__(self):
        self.font_title = pygame.font.Font("../assets/font/orbitron-master/Orbitron Medium.ttf", 42)
        self.font_secondary = pygame.font.Font("../assets/font/orbitron-master/Orbitron Medium.ttf", 16)

    def draw(self, screen, size_window):

        title = self.font_title.render("Ethereal Explorers", False, "white")
        screen.blit(title, (size_window[0]/2.7, size_window[1]/6))
    
        instruction_to_start = self.font_secondary.render("Press space to start", False, "white")
        screen.blit(instruction_to_start, (size_window[0]/2.3, size_window[1]/2))

        create_character = self.font_secondary.render("Press c to create character", False, "white")
        screen.blit(create_character, (size_window[0]/2.4, size_window[1]/2+50))