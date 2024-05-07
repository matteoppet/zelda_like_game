import pygame
import time

from helpers.sprites.player import Player
from helpers.world import World, ground_sprites, water_sprites, tree_sprites, spawn_tree, spawn_trees_sprites
from helpers.sprites.animals import spawn_animals, init_spawns, animals_spawns_sprite, animals_sprite
from helpers.sprites.zombie import create_zombies, zombies_sprites
from helpers.inventory import Button_to_open_inventory, Inventory
from functionality import *
from helpers.utils import update_list_actions_to_display, display_action_massages, overlapping
from helpers.sprites.NPCs import Gildermont, Murwood, NPCs_sprite_group

from __init__ import SCREEN, BACKGROUND, CLOCK, FONT_SIZE_10, FONT_SIZE_15, FONT_SIZE_20, SIZE_WINDOW

# Timers initialization
t0 = time.time()
t0_2 = time.time()
t_day = time.time()
t_zombies = time.time()
t_trees = time.time()

GILDERMONT = Gildermont()
MURWOOD = Murwood()
NPCs_sprite_group.add(GILDERMONT)
NPCs_sprite_group.add(MURWOOD)

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

for _ in range(MAX_TREES_TO_SPAWN):
    spawn_tree(list_spawn_trees_sprites)
    COUNT_OBJECTS_ON_MAPS["trees"] = MAX_TREES_TO_SPAWN
START_TIMER_TREE = False

DAY = True

button_to_open_inventory = Button_to_open_inventory()
INVENTORY_OPENED = False
INVENTORY = Inventory()


def draw_sprites():
    tree_sprites.draw(SCREEN, BACKGROUND)
    animals_sprite.draw(SCREEN, BACKGROUND)
    zombies_sprites.draw(SCREEN, BACKGROUND)

    for NPC in NPCs_sprite_group:
        NPC.draw(SCREEN)


running = True
while running:
    t1 = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PLAYER.actions(attack=True)
            if event.key == pygame.K_e:
                PLAYER.actions(eat=True)


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            rect_mouse = pygame.Rect(pos_mouse[0], pos_mouse[1], 1, 1)

            if button_to_open_inventory.rect.colliderect(rect_mouse):
                print("Open inventory")
                INVENTORY_OPENED = True
            else:
                INVENTORY_OPENED = False
            
            print(pygame.mouse.get_pos())

    PLAYER.actions()

    #################################################### Timers section
    
    # NOTE: PLAYER HEALTH TIMER
    time_elapsed = t1 - t0
    if time_elapsed >= 120:
        PLAYER.health -= 5 
        update_list_actions_to_display("-5 of health removed for not eating")
        t0 = t1
    
    # NOTE: SPAWN ANIMALS TIMER
    time_elapsed_spawn_animals = t1-t0_2
    if time_elapsed_spawn_animals >= 60 and COUNT_OBJECTS_ON_MAPS["animals"] != MAX_ANIMALS_TO_SPAWN:
        spawn_animals(spawns_sprite_list)
        COUNT_OBJECTS_ON_MAPS["animals"] += 1
        update_list_actions_to_display("Spawned animal")
        t0_2 = t1

    # NOTE: SPAWN TREES
    time_trees_elapsed = t1 - t_trees
    if time_trees_elapsed >= 100 and COUNT_OBJECTS_ON_MAPS["trees"] != MAX_TREES_TO_SPAWN:
        spawn_tree(list_spawn_trees_sprites)
        update_list_actions_to_display("Trees spawned on a random map point")
        t_trees = t1
        COUNT_OBJECTS_ON_MAPS["trees"] += 1


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

    ##################################################### Draw section

    SCREEN.fill("white")
    WORLD.draw_map(SCREEN)

    animals_spawns_sprite.draw(SCREEN, BACKGROUND)
    
    if overlapping(PLAYER, tree_sprites) or overlapping(PLAYER, animals_sprite) or overlapping(PLAYER, zombies_sprites) or overlapping(PLAYER, NPCs_sprite_group):
        PLAYER.draw(SCREEN)
        draw_sprites()
    else:
        draw_sprites()
        PLAYER.draw(SCREEN)


    for NPC in NPCs_sprite_group:
        NPC.interaction_section(PLAYER, SCREEN, FONT_SIZE_15, FONT_SIZE_10, SIZE_WINDOW[1])
    

    SCREEN.blit(button_to_open_inventory.image, (button_to_open_inventory.rect.x, button_to_open_inventory.rect.y))
    inventory_text = FONT_SIZE_10.render("Inventory", True, "white")
    SCREEN.blit(inventory_text, (button_to_open_inventory.rect.x+7, button_to_open_inventory.rect.y+7))

    if INVENTORY_OPENED:
        INVENTORY.draw(SCREEN, FONT_SIZE_20)
        INVENTORY.show_items(SCREEN, FONT_SIZE_15)

    for zombie in zombies_sprites:
        zombie.area_to_attack(PLAYER)
    
    display_action_massages(SCREEN, FONT_SIZE_15)

    # display fps
    fps_text = FONT_SIZE_20.render(f"FPS: {int(CLOCK.get_fps())}", True, "black")
    SCREEN.blit(fps_text, (20, 10))
    # display health player
    player_health_text = FONT_SIZE_20.render(f'Health: {PLAYER.health}', True, "black")
    SCREEN.blit(player_health_text, (20,50))

    pygame.display.flip()

    CLOCK.tick(60)

pygame.quit()



# display notification in the up-right of the screen, always the last 5