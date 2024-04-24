import pygame


from helpers.player import Player
from helpers.world import World


pygame.init()
pygame.font.init()

SIZE_WINDOW = (1280, 720)
screen = pygame.display.set_mode(SIZE_WINDOW)
background = pygame.Surface(SIZE_WINDOW)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
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
    
    # display fps
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, "black")
    screen.blit(fps_text, (20, 10))
    # display health player
    player_health_text = font.render(f'Health: {PLAYER.health}', True, "black")
    screen.blit(player_health_text, (20,50))
    # display owned food
    food_text = font.render(f"Food: {PLAYER.food}", True, "black") 
    screen.blit(food_text, (20, 90))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()