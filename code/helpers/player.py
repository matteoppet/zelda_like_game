import pygame
from helpers.obstacles import obstacle_sprites

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.size = (20, 30)
        pos = (200, 200)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill("black")

        self.old_rect = self.rect.copy()

    def move(self):
        keys = pygame.key.get_pressed()
        vel = 1.3
        self.old_rect = self.rect.copy()

        if keys[pygame.K_w]:
            self.rect.y -= vel
            self.collisions("vertical", obstacle_sprites)
        if keys[pygame.K_s]:
            self.rect.y += vel
            self.collisions("vertical", obstacle_sprites)
        if keys[pygame.K_a]:
            self.rect.x -= vel
            self.collisions("horizontal", obstacle_sprites)
        if keys[pygame.K_d]:
            self.rect.x += vel
            self.collisions("horizontal", obstacle_sprites)
            
    def collisions(self, direction, group_sprites):
        # video of collisions: https://youtu.be/W9uKzPFS1CI?si=BM5kFdmDDPSZhXO4
        collision = pygame.sprite.spritecollide(self, group_sprites, False)
        
        if collision:
            if direction == "horizontal":
                for sprite in collision:
                    # collision right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    # collision left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

            elif direction == "vertical":
                for sprite in collision:
                    # collision up
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # collisions down
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

    def draw(self, screen):
        screen.blit(self.image, self.rect)