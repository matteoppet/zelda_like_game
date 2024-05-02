import pygame
import time

from helpers.player import Player
from helpers.world import World, ground_sprites, water_sprites, tree_sprites, spawn_tree, spawn_trees_sprites
from helpers.animals import spawn_animals, init_spawns, animals_spawns_sprite, animals_sprite
from helpers.zombie import create_zombies, zombies_sprites

from helpers.utils import update_list_actions_to_display, display_action_massages

from __init__ import SCREEN, BACKGROUND, CLOCK, FONT_ACTIONS_TEXT, FONT


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
spawn_trees_sprites = spawn_trees_sprites
list_spawn_trees_sprites = [sprite for sprite in spawn_trees_sprites]

init_spawns()
animals_spawns_sprite = animals_spawns_sprite
spawns_sprite_list = animals_spawns_sprite.sprites()

COUNT_TREES = 0
MAX_TREES = 60

COUNT_ANIMALS = 0
MAX_ANIMALS = 15

for _ in range(MAX_TREES):
    spawn_tree(list_spawn_trees_sprites)
    COUNT_TREES = 60

DAY = True


running = True
while running:
    t1 = time.time()

    SCREEN.fill("white")

    WORLD.draw_map(SCREEN)

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

    # NOTE: PLAYER HEALTH TIMER
    time_elapsed = t1 - t0
    if time_elapsed >= 120:
        PLAYER.health -= 5 
        update_list_actions_to_display("-5 of health removed for not eating")
        t0 = t1
    
    # NOTE: SPAWN ANIMALS TIMER
    time_elapsed_spawn_animals = t1-t0_2
    if time_elapsed_spawn_animals >= 60 and COUNT_ANIMALS != MAX_ANIMALS:
        spawn_animals(spawns_sprite_list)
        COUNT_ANIMALS += 1
        update_list_actions_to_display("Spawned animal")
        t0_2 = t1
    
    # NOTE: CICLE DAY/NIGHT TIMER
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
    
    # NOTE: SPAWN TREES
    time_trees_elapsed = t1 - t_trees
    if time_trees_elapsed >= 300 and COUNT_TREES != MAX_TREES:
        spawn_tree(list_spawn_trees_sprites)
        update_list_actions_to_display("Trees spawned on a random map point")
        t_trees = t1
        COUNT_TREES += 1


    animals_spawns_sprite.draw(SCREEN, BACKGROUND)
    animals_sprite.draw(SCREEN, BACKGROUND)
    zombies_sprites.draw(SCREEN, BACKGROUND)
    tree_sprites.draw(SCREEN, BACKGROUND)

    PLAYER.actions()
    PLAYER.draw(SCREEN)

    for zombie in zombies_sprites:
        zombie.area_to_attack(PLAYER.rect)
    
    display_action_massages(SCREEN, FONT_ACTIONS_TEXT)

    # display fps
    fps_text = FONT.render(f"FPS: {int(CLOCK.get_fps())}", True, "black")
    SCREEN.blit(fps_text, (20, 10))
    # display health player
    player_health_text = FONT.render(f'Health: {PLAYER.health}', True, "black")
    SCREEN.blit(player_health_text, (20,50))
    # display owned food
    food_text = FONT.render(f"Food: {PLAYER.food}", True, "black") 
    SCREEN.blit(food_text, (20, 90))

    pygame.display.flip()

    CLOCK.tick(60)

pygame.quit()



# display notification in the up-right of the screen, always the last 5