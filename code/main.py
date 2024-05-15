import pygame
import time
import random

from helpers.sprites.player import Player
from helpers.world import World, ground_sprites, water_sprites, tree_sprites, spawn_tree, spawn_trees_sprites
from helpers.sprites.animals import spawn_animals, animals_sprite, sensors_data
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

# Timers
timer_no_food_damage = pygame.time.get_ticks()
timer_day_night_cicle = pygame.time.get_ticks()
timer_zombies_spawn = pygame.time.get_ticks()
timer_trees_spawn = pygame.time.get_ticks()
timer_animals_spawn = pygame.time.get_ticks()

GILDERMONT = Gildermont()
MURWOOD = Murwood()
NPCs_sprite_group.add(GILDERMONT)
NPCs_sprite_group.add(MURWOOD)

WORLD = World()
WORLD.create_map()
ground_sprites=ground_sprites
list_ground_sprites = [sprite for sprite in ground_sprites]
water_sprites=water_sprites
spawn_trees_sprites = spawn_trees_sprites
list_spawn_trees_sprites = [sprite for sprite in spawn_trees_sprites]

random_spawn_player = random.choice(list_spawn_trees_sprites)
PLAYER = Player(pos=random_spawn_player.rect.center)

for _ in range(MAX_TREES_TO_SPAWN):
    spawn_tree(list_spawn_trees_sprites)
    COUNT_OBJECTS_ON_MAPS["trees"] = MAX_TREES_TO_SPAWN
START_TIMER_TREE = False

DAY = True

button_to_open_inventory = Button_to_open_inventory()
BUTTON_INVENTORY_CLICKED = False
INVENTORY_OPENED = False
INVENTORY = Inventory()

BUTTON_BUILD_PRESSED = False

def draw_sprites():
    tree_sprites.draw(SCREEN, BACKGROUND)
    animals_sprite.draw(SCREEN, BACKGROUND)
    zombies_sprites.draw(SCREEN, BACKGROUND)

    for NPC in NPCs_sprite_group:
        NPC.draw(SCREEN)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PLAYER.actions(attack=True)
            if event.key == pygame.K_e:
                PLAYER.actions(eat=True)

            if BUTTON_BUILD_PRESSED:
                if event.key == pygame.K_b:
                    update_list_actions_to_display("Build mode disabled")
                    BUTTON_BUILD_PRESSED = False
            else:
                if event.key == pygame.K_b:
                    update_list_actions_to_display("Build mode activated")
                    BUTTON_BUILD_PRESSED = True


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()

            if BUTTON_INVENTORY_CLICKED:
                if INVENTORY.rect.collidepoint(pos_mouse) or INVENTORY.rect_character.collidepoint(pos_mouse):
                    INVENTORY_OPENED = True
                else:
                    INVENTORY_OPENED = False
                    BUTTON_INVENTORY_CLICKED = False
            else:
                if button_to_open_inventory.rect.collidepoint(pos_mouse):
                    BUTTON_INVENTORY_CLICKED = True
                    INVENTORY_OPENED = True
                else:
                    INVENTORY_OPENED = False
            
            print(pygame.mouse.get_pos())

    timer_now = pygame.time.get_ticks()
    PLAYER.actions(SCREEN)

    t1 = time.time()
    #################################################### Timers section
    
    # NOTE: PLAYER HEALTH TIMER
    if (timer_now - timer_no_food_damage) >= 120*1000:
        PLAYER.health -= 5 
        update_list_actions_to_display("-5 of health removed for not eating")
        timer_no_food_damage = timer_now
    
    # NOTE: SPAWN ANIMALS TIMER
    if (timer_now - timer_animals_spawn) >= 60*1000 and COUNT_OBJECTS_ON_MAPS["animals"] != MAX_ANIMALS_TO_SPAWN:
        spawn_animals()
        COUNT_OBJECTS_ON_MAPS["animals"] += 1
        update_list_actions_to_display("Spawned animal")
        timer_animals_spawn = timer_now

    # NOTE: SPAWN TREES
    if (timer_now - timer_trees_spawn) >= 100*1000 and COUNT_OBJECTS_ON_MAPS["trees"] != MAX_TREES_TO_SPAWN:
        spawn_tree(list_spawn_trees_sprites)
        update_list_actions_to_display("Trees spawned on a random map point")
        COUNT_OBJECTS_ON_MAPS["trees"] += 1
        timer_trees_spawn = timer_now

    # NOTE: CICLE DAY/NIGHT TIMER
    if (timer_now - timer_day_night_cicle) >= 240*1000:
        DAY = False
        update_list_actions_to_display("Night has come!! Good luck")
        create_zombies(5)
        timer_day_night_cicle = timer_now

    if DAY == False:
        if (timer_now - timer_day_night_cicle) >= 30*1000:
            DAY = True
            update_list_actions_to_display("Day has come!! Prepare for the night")
            timer_day_night_cicle = timer_now

    ##################################################### Draw section

    SCREEN.fill("white")
    WORLD.draw_map(SCREEN)

    if overlapping(PLAYER, tree_sprites) or overlapping(PLAYER, animals_sprite) or overlapping(PLAYER, zombies_sprites) or overlapping(PLAYER, NPCs_sprite_group):
        PLAYER.draw(SCREEN)
        draw_sprites()
    else:
        draw_sprites()
        PLAYER.draw(SCREEN)


    for NPC in NPCs_sprite_group:
        NPC.interaction_section(PLAYER, SCREEN, FONT_SIZE_15, FONT_SIZE_10, SIZE_WINDOW[1])

    
    if BUTTON_BUILD_PRESSED:
        PLAYER.actions(SCREEN, build=True)
    
    for animal in animals_sprite:
        animal.sensors_position_update()
        animal.draw_sensors(SCREEN)
        animal.check_collision_sensors(water_sprites)

    for sensor in sensors_data:
        if sensors_data[sensor]["point_of_collision"] != None:
            print(f"{sensor}: {sensors_data[sensor]['distance_collision']}")

    SCREEN.blit(button_to_open_inventory.image, (button_to_open_inventory.rect.x, button_to_open_inventory.rect.y))
    inventory_text = FONT_SIZE_10.render("Inventory", True, "white")
    SCREEN.blit(inventory_text, (button_to_open_inventory.rect.x+7, button_to_open_inventory.rect.y+7))

    if INVENTORY_OPENED:
        INVENTORY.draw(SCREEN, FONT_SIZE_20)
        INVENTORY.show_character(SCREEN, PLAYER, FONT_SIZE_15, FONT_SIZE_10)
        INVENTORY.show_items(SCREEN, FONT_SIZE_15, FONT_SIZE_10, PLAYER)
        INVENTORY.check_click_button(PLAYER)

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