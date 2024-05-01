import pygame
import time
import numpy as np
import random

from helpers.player import Player
from helpers.world import World, ground_sprites, water_sprites, Trees, tree_sprites, spawn_tree
from helpers.animals import spawn_animals, init_spawns, animals_spawns_sprite, animals_sprite
from helpers.zombie import create_zombies, zombies_sprites

from helpers.utils import update_list_actions_to_display, LIST_ACTIONS_TO_DISPLAY


pygame.init()
pygame.font.init()

SIZE_WINDOW = (1600, 960)
screen = pygame.display.set_mode(SIZE_WINDOW)
background = pygame.Surface(SIZE_WINDOW)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
font_actions_text = pygame.font.SysFont("Arial", 15)
running = True

t0 = time.time()
t0_2 = time.time()
t_day = time.time()
t_zombies = time.time()
t_trees = time.time()

PLAYER = Player()

WORLD = World()
WORLD.create_map()
ground_sprites=ground_sprites
list_ground_sprites = [sprite for sprite in ground_sprites]
water_sprites=water_sprites

init_spawns()
animals_spawns_sprite = animals_spawns_sprite
spawns_sprite_list = animals_spawns_sprite.sprites()

COUNT_TREES = 0
MAX_TREES = 15
SIZE_TREE = (10, 15)

for _ in range(MAX_TREES):
    spawn_tree()

DAY = True

while running:
    t1 = time.time()

    screen.fill("white")

    WORLD.draw_map(screen)

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

    # PLAYER HEALTH TIMER
    time_elapsed = t1 - t0
    if time_elapsed >= 120:
        PLAYER.health -= 5 
        update_list_actions_to_display("-5 of health removed for not eating")
        t0 = t1
    
    # SPAWN ANIMALS TIMER
    time_elapsed_spawn_animals = t1-t0_2
    if time_elapsed_spawn_animals >= 60:
        spawn_animals(spawns_sprite_list)
        update_list_actions_to_display("Spawned animal")
        t0_2 = t1
    
    # CICLE DAY/NIGHT TIMER
    time_day_elapsed = t1 - t_day
    if time_day_elapsed >= 240:
        DAY = False
        update_list_actions_to_display("Night has come!! Good luck")
        # todo: create zombies in ordes
        create_zombies(5)
        t_day = t1
    
    if DAY == False:
        if time_day_elapsed >= 30:
            DAY = True
            update_list_actions_to_display("Day has come!! Prepare for the night")
            t_day= t1

    time_trees_elapsed = t1 - t_trees
    if time_trees_elapsed >= 300 and COUNT_TREES != MAX_TREES:
        spawn_tree()
        update_list_actions_to_display("Trees spawned on a random map point")
        t_trees = t1
        COUNT_TREES += 1

    #obstacle_sprites.draw(screen, background)
    animals_spawns_sprite.draw(screen, background)
    animals_sprite.draw(screen, background)
    zombies_sprites.draw(screen, background)
    tree_sprites.draw(screen, background)

    PLAYER.actions()
    PLAYER.draw(screen)

    for zombie in zombies_sprites:
        zombie.area_to_attack(PLAYER.rect)
    
    # display actions massages
    rect_background_text = pygame.Rect(1210, 800, 375, 150)
    pygame.draw.rect(screen, "black", rect_background_text)
    start_x_text = rect_background_text.x + 10
    start_y_text = rect_background_text.y + 15
    for text_to_display in LIST_ACTIONS_TO_DISPLAY:
        text = font_actions_text.render(text_to_display, True, "green")
        screen.blit(text, (start_x_text, start_y_text))
        start_y_text += 25


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



# display notification in the up-right of the screen, always the last 5