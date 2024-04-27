import pygame
import time
import numpy as np

from helpers.player import Player
from helpers.world import World, ground_sprites, water_sprites
from helpers.animals import spawn_animals, init_spawns, animals_spawns_sprite, animals_sprite
from helpers.zombie import create_zombies, zombies_sprites

class Button:
    def __init__(self):
        ...

    def render(self):
        ...
        

pygame.init()
pygame.font.init()

SIZE_WINDOW = (1600, 960)
screen = pygame.display.set_mode(SIZE_WINDOW)
background = pygame.Surface(SIZE_WINDOW)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
running = True

t0 = time.time()
t0_2 = time.time()

PLAYER = Player()

WORLD = World()
WORLD.create_map()
ground_sprites=ground_sprites
water_sprites=water_sprites

init_spawns()
animals_spawns_sprite = animals_spawns_sprite
spawns_sprite_list = animals_spawns_sprite.sprites()

DAY = True

while running:
    t1 = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PLAYER.actions(attack=True)
            if event.key == pygame.K_l:
                PLAYER.actions(eat=True)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            DAY = False

    time_elapsed = t1 - t0
    if time_elapsed >= 120:
        PLAYER.health -= 3
        print("-10 of health removed for not eating")
        t0 = t1

    time_elapsed_spawn_animals = t1-t0_2
    if time_elapsed_spawn_animals >= 60:
        sprite_spawn = np.random.choice(spawns_sprite_list)
        pos = sprite_spawn.coordinate_to_spawn()
        spawn_animals(pos, sprite_spawn.name)
        print("Spawned animal")
        t0_2 = t1

    if not DAY:
        create_zombies(5)
        DAY = True

    screen.fill("white")

    WORLD.draw_map(screen)

    #obstacle_sprites.draw(screen, background)
    animals_spawns_sprite.draw(screen, background)
    animals_sprite.draw(screen, background)
    zombies_sprites.draw(screen, background)

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
