import pygame
from pygame_widgets.button import Button
from .player import Player


CLASS_CHARACTER_DICT = {
    "fighter": {
        "strength": 5,
        "constitution": 4,
        "intelligence": 2,
        "charisma": 1,
    },

    "wizard": {
        "strength": 3,
        "constitution": 2,
        "intelligence": 4,
        "charisma": 3
    },
    
    "adventurer": {
        "strength": 2,
        "constitution": 4,
        "intelligence": 3,
        "charisma": 3
    }
}


class Character_creation:
    def __init__(self):
        self.font_title = pygame.font.Font("../assets/font/orbitron-master/Orbitron Medium.ttf", 42)
        self.font_secondary = pygame.font.Font("../assets/font/orbitron-master/Orbitron Medium.ttf", 16)
        self.font_third = pygame.font.Font("../assets/font/arial/ARIAL.TTF", 20)

        self.points_available = 10

        self.show_second_screen = False
        self.start_game = False


    def draw_second_screen(self, screen):
        title_window = self.font_title.render("Creation character (upgrade skills)", False, "white")
        screen.blit(title_window, (40, 40))

        current_skills_character_text = self.font_secondary.render("Current skills character:", False, "white")
        screen.blit(current_skills_character_text, (40, 200))

        ############### creation left-part of the screen skills
        start_y_skills = 250
        for name_skill, points in Player.CHARACTER_INFO["skills"].items():
            skill_text = self.font_secondary.render(f"> {name_skill}: {points}", False, "white")
            screen.blit(skill_text, (40, start_y_skills))

            start_y_skills += 30

        ############### creation center-part of the screen skills 
        pos_x_second_part = 600
        start_y_skills_second_part = 250

        points_available_text = self.font_secondary.render(f"Points available: {self.points_available}", False, "white")
        screen.blit(points_available_text, (pos_x_second_part, 200))

        buttons_list = []
        for name_skill_to_increase, points_to_increase in Player.CHARACTER_INFO["skills"].items():
            #text
            skills_information_text = self.font_secondary.render(f"> {name_skill_to_increase}: {points_to_increase}", False, "white") 
            screen.blit(skills_information_text, (pos_x_second_part, start_y_skills_second_part))

            #button
            pos_y_for_button = start_y_skills_second_part
            pos_y_for_button += 30
            button_increase = Button(
                screen, 
                pos_x_second_part, pos_y_for_button, 30, 30, 
                text="+",
                onClick=lambda skill=name_skill_to_increase: self.increase_skill(skill))
            button_decrease = Button(
                screen, 
                pos_x_second_part+50, pos_y_for_button, 30, 30, 
                text="-",
                onClick=lambda skill=name_skill_to_increase: self.decrease_skill(skill))

            buttons_list.append(button_increase)
            buttons_list.append(button_decrease)

            start_y_skills_second_part += 100


        ########### creation right-part of the screen
        background_rect = pygame.Rect(1050, 200, 450, 600)
        pygame.draw.rect(screen, (51, 51, 51), background_rect)

        info_character_text = self.font_third.render("Info character", False, "white")
        screen.blit(info_character_text, (1070, 220))

        class_character_text = self.font_third.render(f"Class: {Player.CHARACTER_INFO['class']}", False, "white")
        screen.blit(class_character_text, (1070, 300))

        start_y_third_part = 350
        for name_skill_info, points_given in Player.CHARACTER_INFO["skills"].items():
            name_skill_points_text = self.font_third.render(
                f"{name_skill_info}: {CLASS_CHARACTER_DICT[Player.CHARACTER_INFO['class']][name_skill_info]} + ({points_given})", False, "white")
            screen.blit(name_skill_points_text, (1070, start_y_third_part))

            start_y_third_part += 30

        end_button_to_start_game = Button(
            screen, 1500, 150, 50, 50,
            onClick=lambda: self.save()
        )
        buttons_list.append(end_button_to_start_game)


        return buttons_list
    

    def draw_first_screen(self, screen):
        list_buttons = []

        title_window = self.font_title.render("Creation character (choose type)", False, "white")
        screen.blit(title_window, (40, 40))

        fighter_text = self.font_title.render("Fighter", False, "white")
        screen.blit(fighter_text, (300, 300))
        fighter_button = Button(
            screen,
            300, 400, 160, 300,
            onClick=lambda class_character='fighter': self.change_to_second_screen(class_character) 
        )
        list_buttons.append(fighter_button)

        wizard_text = self.font_title.render("Wizard", False, "white")
        screen.blit(wizard_text, (700, 300))
        wizard_button = Button(
            screen,
            705, 400, 160, 300,
            onClick=lambda class_character='wizard': self.change_to_second_screen(class_character) 
        )
        list_buttons.append(wizard_button)

        adventurer_text = self.font_title.render("Adventurer", False, "white")
        screen.blit(adventurer_text, (1100, 300))
        adventurer_button = Button(
            screen,
            1150, 400, 160, 300,
            onClick=lambda class_character='adventurer': self.change_to_second_screen(class_character) 
        )
        list_buttons.append(adventurer_button)

        return list_buttons
    
    
    def save(self):

        self.start_game = True
        
        for name_skill, points in Player.CHARACTER_INFO["skills"].items():
            Player.CHARACTER_INFO["skills"][name_skill] = points + CLASS_CHARACTER_DICT[Player.CHARACTER_INFO["class"]][name_skill]

    def change_to_second_screen(self, class_character):
        Player.CHARACTER_INFO["class"] = class_character

        self.show_second_screen = True

    
    def increase_skill(self, skill):
        if self.points_available != 0:
            self.points_available -= 1

            Player.CHARACTER_INFO["skills"][skill] += 1

    def decrease_skill(self, skill):
        if self.points_available < 10:
            self.points_available += 1

            Player.CHARACTER_INFO["skills"][skill] -= 1


# TODO: save