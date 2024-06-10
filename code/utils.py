import pygame
import csv
import os

LIST_ACTIONS_TO_DISPLAY = []

def update_list_actions_to_display(text):
    if len(LIST_ACTIONS_TO_DISPLAY) < 5:
        LIST_ACTIONS_TO_DISPLAY.append(text)
    else:
        LIST_ACTIONS_TO_DISPLAY.pop(0)
        LIST_ACTIONS_TO_DISPLAY.append(text)

def display_action_massages(screen, font_actions_text):
    rect_background_text = pygame.Rect(1210, 800, 375, 150)
    pygame.draw.rect(screen, "black", rect_background_text)

    start_x_text = rect_background_text.x + 10
    start_y_text = rect_background_text.y + 15

    for text_to_display in LIST_ACTIONS_TO_DISPLAY:
        text = font_actions_text.render(text_to_display, True, "green")
        screen.blit(text, (start_x_text, start_y_text))
        start_y_text += 25


def overlapping(sprite_player, group):
    collision = pygame.sprite.spritecollide(sprite_player, group, False)

    if collision:
        for sprite in collision:
            if sprite_player.rect.bottomleft[1] < sprite.rect.bottomleft[1]:
                return True
            

def import_layout_csv(path):
    terrain_map = []
    with open(path) as level_map:   
        layout = csv.reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    

def import_folder(path):
    surface_dict = {}

    for _,__,img_files in os.walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()

            surface_dict[image] = image_surf

    return surface_dict    


tileset_image = pygame.image.load("../assets/player_images/player_images.png")

tile_width = 64
tile_height = 64

tileset_width, tileset_height = tileset_image.get_size()
tiles_per_row = tileset_width // tile_width

def get_tile(tile_id):
    tile_x = (tile_id % tiles_per_row) * tile_width
    tile_y = (tile_id // tiles_per_row) * tile_height
    tile_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
    tile_surface.blit(tileset_image, (0, 0), (tile_x, tile_y, tile_width, tile_height))
    return tile_surface

# Create a dictionary to map tile IDs to Pygame surfaces
tiles = {}
for tile_id in range((tileset_width // tile_width) * (tileset_height // tile_height)):
    tiles[tile_id] = get_tile(tile_id)