import pygame
import time
import random

from helpers.sprites.player import Player
from helpers.world import World, ground_sprites, water_sprites, tree_sprites, spawn_tree, spawn_trees_sprites, spawn_base_sprites
from helpers.sprites.animals import spawn_animals, animals_sprite, sensors_data
from helpers.sprites.zombie import create_zombies, zombies_sprites
from helpers.inventory import Button_to_open_inventory, Inventory
from functionality import *
from helpers.utils import update_list_actions_to_display, display_action_massages, overlapping
from helpers.sprites.NPCs import Gildermont, Murwood, NPC_base
from helpers.home_screen import Home_screen
from helpers.base_spawn import Base, towers_sprite_group

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
NPC_BASE = NPC_base()
NEAR_VENDORS = False
NPC_sprite_group = pygame.sprite.Group()
NPC_sprite_group.add(GILDERMONT)
NPC_sprite_group.add(MURWOOD)


WORLD = World()
WORLD.create_map()
ground_sprites=ground_sprites
list_ground_sprites = [sprite for sprite in ground_sprites]
water_sprites=water_sprites
spawn_trees_sprites = spawn_trees_sprites
list_spawn_trees_sprites = [sprite for sprite in spawn_trees_sprites]
spawn_base_sprites = spawn_base_sprites
list_spawn_base_sprites = [sprite for sprite in spawn_base_sprites]

BASE_SPAWN = Base(list_spawn_base_sprites)
towers_sprite_group = towers_sprite_group

PLAYER = Player(pos=BASE_SPAWN.area_base_rect.center)

for _ in range(MAX_TREES_TO_SPAWN):
    spawn_tree(list_spawn_trees_sprites, BASE_SPAWN)
    COUNT_OBJECTS_ON_MAPS["trees"] = MAX_TREES_TO_SPAWN
START_TIMER_TREE = False

DAY = True

button_to_open_inventory = Button_to_open_inventory()
BUTTON_INVENTORY_CLICKED = False
INVENTORY_OPENED = False
INVENTORY = Inventory()

BUTTON_BUILD_PRESSED = False

SHOW_HOME_SCREEN = False
HOME_SCREEN = Home_screen()

running = True
while running:
    if SHOW_HOME_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SHOW_HOME_SCREEN = False

        SCREEN.fill("black")
        HOME_SCREEN.draw(SCREEN, SIZE_WINDOW)

    else:

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
                        INVENTORY.check_button_activity(pos_mouse, PLAYER)
                    else:
                        INVENTORY_OPENED = False
                        BUTTON_INVENTORY_CLICKED = False
                else:
                    if button_to_open_inventory.rect.collidepoint(pos_mouse):
                        BUTTON_INVENTORY_CLICKED = True
                        INVENTORY_OPENED = True
                    else:
                        INVENTORY_OPENED = False

                if NEAR_VENDORS:
                    if NEAR_VENDORS == "armors": 
                        MURWOOD.interaction_section(pos_mouse)
                    else:
                        GILDERMONT.interaction_section(pos_mouse)


        if PLAYER.health <= 0:
            # respawn
            ...

        timer_now = pygame.time.get_ticks()
        PLAYER.actions()

        NEAR_VENDORS = NPC_BASE.distance_from_vendor(PLAYER, NPC_sprite_group)

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
        if (timer_now - timer_day_night_cicle) >= 240*1000: #240
            DAY = False
            update_list_actions_to_display("Night has come!! Good luck")
            create_zombies(15)
            timer_day_night_cicle = timer_now

        if DAY == False:
            if (timer_now - timer_day_night_cicle) >= 30*1000:
                DAY = True
                update_list_actions_to_display("Day has come!! Prepare for the night")
                timer_day_night_cicle = timer_now

        ##################################################### Draw section

        SCREEN.fill("white")
        WORLD.draw_map(SCREEN)

        BASE_SPAWN.draw(SCREEN)

        if overlapping(PLAYER, tree_sprites) or overlapping(PLAYER, animals_sprite) or overlapping(PLAYER, zombies_sprites) or overlapping(PLAYER, NPC_sprite_group) or overlapping(PLAYER, towers_sprite_group):
            PLAYER.draw(SCREEN)
            tree_sprites.draw(SCREEN, BACKGROUND)
            animals_sprite.draw(SCREEN, BACKGROUND)
            zombies_sprites.draw(SCREEN, BACKGROUND)
            BASE_SPAWN.draw_towers(SCREEN)

            for NPC in NPC_sprite_group:
                NPC.draw(SCREEN)

        else:
            tree_sprites.draw(SCREEN, BACKGROUND)
            animals_sprite.draw(SCREEN, BACKGROUND)
            zombies_sprites.draw(SCREEN, BACKGROUND)
            BASE_SPAWN.draw_towers(SCREEN)

            for NPC in NPC_sprite_group:
                NPC.draw(SCREEN)

            PLAYER.draw(SCREEN)

        if NEAR_VENDORS:
            if NEAR_VENDORS == "armors": 
                MURWOOD.draw_interaction_section(SCREEN, FONT_SIZE_15, FONT_SIZE_10, SIZE_WINDOW[1])
            else:
                GILDERMONT.draw_interaction_section(SCREEN, FONT_SIZE_15, FONT_SIZE_10, SIZE_WINDOW[1])
        
        for animal in animals_sprite:
            animal.sensors_position_update()
            animal.draw_sensors(SCREEN)
            animal.check_collision_sensors(water_sprites)

        for sensor in sensors_data:
            if sensors_data[sensor]["point_of_collision"] != None:
                # print(f"{sensor}: {sensors_data[sensor]['distance_collision']}")
                ...

        SCREEN.blit(button_to_open_inventory.image, (button_to_open_inventory.rect.x, button_to_open_inventory.rect.y))
        inventory_text = FONT_SIZE_10.render("Inventory", True, "white")
        SCREEN.blit(inventory_text, (button_to_open_inventory.rect.x+7, button_to_open_inventory.rect.y+7))

        if INVENTORY_OPENED:
            INVENTORY.functionality_inventory()
            INVENTORY.draw_inventory(SCREEN, FONT_SIZE_15, FONT_SIZE_10)

            INVENTORY.functionality_character(PLAYER)
            INVENTORY.draw_character(SCREEN, PLAYER, FONT_SIZE_15, FONT_SIZE_10)

        for zombie in zombies_sprites:
            zombie.area_to_attack(PLAYER)

        BASE_SPAWN.towers_defense_action(zombies_sprites, PLAYER)
        
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
