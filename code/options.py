#IMPORTING LIBRARIES
import pygame
from os import path

#IMPORTING FILES
from settings import *
from loading_data import save_data

#OPTIONS CLASS
class Options:

    #OPTIONS CLASS CONSTRUCTOR
    def __init__(s, game, aggression_data):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #TURNING MENU DATA IN TO AN ATTRIBUTE
        s.data = aggression_data

        #OPTION CLASS ATTRIBUTE
        s.background = pygame.image.load(path.join('..', 'assets', 'options_assets', 'options_background.png')).convert()

        #FONTS AND TEXT
        s.name_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)
        s.aggression_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)
        s.aggression_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 34)
        s.formula_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 22)

        #AGGRESSION BOX TEXT
        s.aggression_title = s.aggression_font.render('AGGRESSION FORMULA', False, (255,255,255))
        s.aggression_title_rect = s.aggression_title.get_rect(topleft = (742, 50))
        s.formula_text = s.formula_font.render('aggression + night * (3 + night//2)', False, (255,255,255))
        s.formula_text_rect = s.formula_text.get_rect(center = (s.aggression_title_rect.centerx, s.aggression_title_rect.centery+40))

        #AGGRESSION BOX CHANCES
        s.freddy_chance = s.aggression_font.render(f"FREDDY       {s.data['Freddy'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.freddy_chance_rect = s.freddy_chance.get_rect(topleft = (750, s.formula_text_rect.bottom+85))
        s.bonnie_chance = s.aggression_font.render(f"BONNIE        {s.data['Bonnie'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.bonnie_chance_rect = s.bonnie_chance.get_rect(topleft = (750, s.formula_text_rect.bottom+125))
        s.chicka_chance = s.aggression_font.render(f"CHICKA        {s.data['Chicka'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.chicka_chance_rect = s.chicka_chance.get_rect(topleft = (750, s.formula_text_rect.bottom+165))
        s.foxy_chance = s.aggression_font.render(f"FOXY           {s.data['Foxy'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.foxy_chance_rect = s.foxy_chance.get_rect(topleft = (750, s.formula_text_rect.bottom+205))

        #NAMES TEXT
        s.freddy_name_text = s.name_font.render('Freddy', False, (255,255,255))
        s.bonnie_name_text = s.name_font.render('Bonnie', False, (255,255,255))
        s.chicka_name_text = s.name_font.render('Chicka', False, (255,255,255))
        s.foxy_name_text = s.name_font.render('Foxy', False, (255,255,255))

        #ROTATING THE NAMES
        s.freddy_name_text = pygame.transform.rotate(s.freddy_name_text, 90)
        s.bonnie_name_text = pygame.transform.rotate(s.bonnie_name_text, 90)
        s.chicka_name_text = pygame.transform.rotate(s.chicka_name_text, 90)
        s.foxy_name_text = pygame.transform.rotate(s.foxy_name_text, 90)

        #INITIAL AGGRESSION SURFACEES
        s.freddy_aggression_text = s.aggression_font.render(f"{s.data['Freddy']}", False, (255,255,255))
        s.freddy_aggression_text_rect = s.freddy_aggression_text.get_rect(center = (195, 320))
        s.bonnie_aggression_text = s.aggression_font.render(f"{s.data['Bonnie']}", False, (255,255,255))
        s.bonnie_aggression_text_rect = s.bonnie_aggression_text.get_rect(center = (495, 320))
        s.chicka_aggression_text = s.aggression_font.render(f"{s.data['Chicka']}", False, (255,255,255))
        s.chicka_aggression_text_rect = s.chicka_aggression_text.get_rect(center = (195, 630))
        s.foxy_aggression_text = s.aggression_font.render(f"{s.data['Foxy']}", False, (255,255,255))
        s.foxy_aggression_text_rect = s.foxy_aggression_text.get_rect(center = (495, 630))

        #BUTTON GROUPS
        s.left_right_button_group = pygame.sprite.Group()
        s.resolution_button_group = pygame.sprite.Group()

        #INITIALIZING AGGRESSION SELECT BUTTONS
        s.freddy_buttons = LeftRightButton(s.game, s.left_right_button_group, 95, 280, 'Freddy')
        s.bonnie_buttons = LeftRightButton(s.game, s.left_right_button_group, 400, 280, 'Bonnie')
        s.chicka_buttons = LeftRightButton(s.game, s.left_right_button_group, 95, 600, 'Chicka')
        s.foxy_buttons = LeftRightButton(s.game, s.left_right_button_group, 400, 600, 'Foxy')

        #INITIALIZING SAVE / CANCEL BUTTONS
        s.back_button = BackButton(s.game)


    #METHOD FOR RUNNING THE OPTIONS MENU
    def run(s):

        #UPDATING THE OPTIONS MENU
        s.update()

        #DRAWING THE OPTIONS MENU
        s.draw()

    #METHOD FOR DRAWING THE OPTIONS MENU
    def draw(s):

        #DRAWING THE BACKGROUND
        s.game.display.blit(s.background, (0,0))

        #DRAWING AGGRESSION FORMULA BOX
        s.game.display.blit(s.aggression_title, s.aggression_title_rect)
        s.game.display.blit(s.formula_text, s.formula_text_rect)
        s.game.display.blit(s.freddy_chance, s.freddy_chance_rect)
        s.game.display.blit(s.bonnie_chance, s.bonnie_chance_rect)
        s.game.display.blit(s.chicka_chance, s.chicka_chance_rect)
        s.game.display.blit(s.foxy_chance, s.foxy_chance_rect)

        #DRAWING THE ANIMATRONIC NAMES
        s.game.display.blit(s.freddy_name_text, (55,85))
        s.game.display.blit(s.bonnie_name_text, (360,85))
        s.game.display.blit(s.chicka_name_text, (55,420))
        s.game.display.blit(s.foxy_name_text, (360, 465))

        #DRAWING AGGRESSION LEVELS
        s.game.display.blit(s.freddy_aggression_text, s.freddy_aggression_text_rect)
        s.game.display.blit(s.bonnie_aggression_text, s.bonnie_aggression_text_rect)
        s.game.display.blit(s.chicka_aggression_text, s.chicka_aggression_text_rect)
        s.game.display.blit(s.foxy_aggression_text, s.foxy_aggression_text_rect)

        #DRAWING BUTTONS
        for button in s.left_right_button_group:
            button.draw()
        s.back_button.draw()
    
    #METHOD FOR UPDATING THE OPTIONS MENU
    def update(s):

        #RERENDERING THE AGGRESION CHANCES
        s.freddy_chance = s.aggression_font.render(f"FREDDY       {s.data['Freddy'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.bonnie_chance = s.aggression_font.render(f"BONNIE        {s.data['Bonnie'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.chicka_chance = s.aggression_font.render(f"CHICKA        {s.data['Chicka'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))
        s.foxy_chance = s.aggression_font.render(f"FOXY           {s.data['Foxy'] + s.game.data['NIGHT_DATA'] * (3 + s.game.data['NIGHT_DATA'] // 2)} %", False, (255,255,255))

        #RERENDERING THE AGGRESION TEXT BECAUSE THE PLAYER WILL CHANGE THE STATS WITH BUTTONS
        s.freddy_aggression_text = s.aggression_font.render(f"{s.data['Freddy']}", False, (255,255,255))
        s.bonnie_aggression_text = s.aggression_font.render(f"{s.data['Bonnie']}", False, (255,255,255))
        s.chicka_aggression_text = s.aggression_font.render(f"{s.data['Chicka']}", False, (255,255,255))
        s.foxy_aggression_text = s.aggression_font.render(f"{s.data['Foxy']}", False, (255,255,255))

        #UPDATING BUTTONS
        for button in s.left_right_button_group:
            button.update()
        s.back_button.update()

#BACK BUTTON CLASS
class BackButton():

    #SAVE / CANCEL BUTTON CLASS
    def __init__(s, game):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #SAVE / CANCEL BUTTON ATTRIBUTES
        s.image = pygame.image.load(path.join('..', 'assets', 'options_assets', 'save_cancel_button.png')).convert()
        s.image = pygame.transform.scale(s.image, (350, 100))
        s.rect = s.image.get_rect(bottomright = (WINDOW_WIDTH - 80, 650))

        #BUTTON FONT AND TEXT
        s.font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)
        s.text = s.font.render('<<  BACK', False, (0,0,0))
        s.text_rect = s.text.get_rect(center = (s.rect.centerx, s.rect.centery+10))



    #METHOD FOR UPDATING THE BUTTON
    def update(s):

        #METHOD FOR BUTTON INPUT
        s.input()

    
    #METHOD FOR DRAWING BUTTONS
    def draw(s):

        s.game.display.blit(s.image, s.rect)
        s.game.display.blit(s.text, s.text_rect)

    
    #METHOD FOR BUTTON INPUT
    def input(s):

        #GETTING MOUSE POSITION AND INPUT
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        #MAKING THE BUTTONS TRANSPARENT WHEN HOVERING OVER THEM
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(100)
            s.text.set_alpha(100)
        else:
            s.image.set_alpha(255)
            s.text.set_alpha(255)
  
        #PRESSING THE BUTTON
        if s.rect.collidepoint(mouse_pos) and mouse_pressed:

            save_data(s.game.aggression_data, AGGRESSION_DATA_PATH)
            s.game.game_state = 'menu'
            
#BUTTON CLASS
class LeftRightButton(pygame.sprite.Sprite):

    #BUTTON CLASS CONSTRUCTOR
    def __init__(s, game, group, pos_x, pos_y, animatronic_aggression_effected):

        #INITIALIZING INHERITANCE
        super().__init__(group)

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #BUTTON CLASS ATTRIBUTES
        s.left_arrow = pygame.image.load(path.join('..', 'assets', 'options_assets', 'left_arrow.png')).convert()
        s.left_arrow = pygame.transform.scale(s.left_arrow, (30, 65))
        s.left_arrow_rect = s.left_arrow.get_rect(topleft = (pos_x, pos_y))
        s.right_arrow = pygame.transform.flip(s.left_arrow, True, False)
        s.right_arrow_rect = s.right_arrow.get_rect(topleft = (pos_x + 170, pos_y))

        #DATA FOR AFFECTED ANIMATRONIC LEVEL
        s.animatronic_aggression_effected = animatronic_aggression_effected

        # TIMER FOR BUTTON PRESS DELAY
        s.last_pressed = 0  #STORES LAST TIME BUTTON WAS PRESSED
        s.press_delay = 100  # 0.1 SECOND DELAY IN MILISECONS


    #METHOD FOR UPDATING THE BUTTON
    def update(s):

        #METHOD FOR BUTTON INPUT
        s.input()

    
    #METHOD FOR DRAWING BUTTONS
    def draw(s):

        s.game.display.blit(s.left_arrow, s.left_arrow_rect)
        s.game.display.blit(s.right_arrow, s.right_arrow_rect)

    
    #METHOD FOR BUTTON INPUT
    def input(s):

        #GETTING MOUSE POSITION AND INPUT
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        current_time = pygame.time.get_ticks()

        #MAKING THE BUTTONS TRANSPARENT WHEN HOVERING OVER THEM
        if s.left_arrow_rect.collidepoint(mouse_pos):
            s.left_arrow.set_alpha(100)
        else:
            s.left_arrow.set_alpha(255)

        if s.right_arrow_rect.collidepoint(mouse_pos):
            s.right_arrow.set_alpha(100)
        else:
            s.right_arrow.set_alpha(255)

        # CHECKING BUTTON PRESS WITH DELAY
        if mouse_pressed and current_time - s.last_pressed > s.press_delay:
            if s.left_arrow_rect.collidepoint(mouse_pos):
                if s.game.aggression_data[s.animatronic_aggression_effected] > 1:
                    s.game.aggression_data[s.animatronic_aggression_effected] -= 1
                    s.last_pressed = current_time  #UPDATE LAST TIME PRESSED

            if s.right_arrow_rect.collidepoint(mouse_pos):
                if s.game.aggression_data[s.animatronic_aggression_effected] < 20:
                    s.game.aggression_data[s.animatronic_aggression_effected] += 1
                    s.last_pressed = current_time  #UPDATE LAST TIME PRESSED

