import pygame


from helpers.player import Player
from helpers.obstacles import obstacle_sprites, create_obstacles


pygame.init()
SIZE_WINDOW = (1280, 720)
screen = pygame.display.set_mode(SIZE_WINDOW)
background = pygame.Surface(SIZE_WINDOW)
clock = pygame.time.Clock()
running = True


PLAYER = Player()

create_obstacles()
OBSTACLE_SPRITES = obstacle_sprites


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    OBSTACLE_SPRITES.draw(screen, background)
    
    PLAYER.move()
    PLAYER.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()