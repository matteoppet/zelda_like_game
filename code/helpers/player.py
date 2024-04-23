import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        size = (20, 30)
        pos = (200, 200)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

    def move(self):
        keys = pygame.key.get_pressed()
        vel = 1.3

        if keys[pygame.K_w]:
            self.rect.y -= vel
        if keys[pygame.K_s]:
            self.rect.y += vel
        if keys[pygame.K_a]:
            self.rect.x -= vel
        if keys[pygame.K_d]:
            self.rect.x += vel

    def draw(self, screen):
        screen.blit(self.image, self.rect)