import pygame


from helpers.player import Player
from helpers.world import World


pygame.init()
SIZE_WINDOW = (1280, 720)
screen = pygame.display.set_mode(SIZE_WINDOW)
background = pygame.Surface(SIZE_WINDOW)
clock = pygame.time.Clock()
running = True


PLAYER = Player()

WORLD = World()
obstacle_sprites = WORLD.init_obstacles()
animals_sprites = WORLD.init_animals()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    obstacle_sprites.draw(screen, background)
    animals_sprites.draw(screen, background)
    
    PLAYER.actions()
    PLAYER.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()