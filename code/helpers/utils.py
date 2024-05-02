import pygame

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