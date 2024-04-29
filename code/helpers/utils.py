import pygame

LIST_ACTIONS_TO_DISPLAY = []

def update_list_actions_to_display(text):
    if len(LIST_ACTIONS_TO_DISPLAY) < 5:
        LIST_ACTIONS_TO_DISPLAY.append(text)
    else:
        LIST_ACTIONS_TO_DISPLAY.pop(0)
        LIST_ACTIONS_TO_DISPLAY.append(text)
