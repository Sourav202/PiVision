#IMPORTING LIBRARIES
import pygame
from os import path
from random import randint

#IMPORTING FILES
from settings import *
from efects import add_glitch_lines, add_static, flicker_brightness
from level import Level


#MENU CLASS
class Menu:

    #MENU CONSTRUCTOR
    def __init__(s, game, data):  #PASSING IN THE GAME AND MENU DATA

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #TURNING MENU DATA IN TO AN ATTRIBUTE
        s.data = data

        #FONT ATTRIBUTES
        s.title_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 70)
        s.night_info_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 30)
        s.button_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)

        #MENU ATTRIBUTES
        s.background = pygame.image.load(path.join('..', 'assets', 'menu', 'background.jpg')).convert()
        s.background = pygame.transform.scale(s.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        s.title = s.title_font.render("Five nights at Python's", False, (255,255,255))
        s.night_info = s.night_info_font.render(f"Night {s.data['NIGHT_DATA']}", False, (255,255,255))

        #COMPLETION ATTRIBUTES
        s.completion_star = pygame.image.load(path.join('..', 'assets', 'menu', 'star.png')).convert_alpha()
        s.completion_star = pygame.transform.scale(s.completion_star, (70, 70))
        s.completion_star_rect = s.completion_star.get_rect(bottomleft = (20, WINDOW_HEIGHT-20))

        #BUTTONS GROUP
        s.buttons = pygame.sprite.Group()

        #INITIALIZNG MENU BUTTONS
        s.new_game_button = Button('New game', 250, s.button_font, 'new_game', s.buttons)
        s.continue_game_button = Button('Continue', 300, s.button_font, 'continue_game', s.buttons, s.data['NIGHT_DATA'] == 1)
        s.options_button = Button('Options', 350, s.button_font, 'options', s.buttons)
        s.extras_button = Button('Extras', 400, s.button_font, 'extras', s.buttons)
        s.exit_button = Button('Exit', 450, s.button_font, 'exit', s.buttons)

        #FRAME SKIP COUNTER
        s.frame_skip_counter = 0

        #MENU BACKGROUND SOUND
        s.menu_background_sound = pygame.mixer.Sound(path.join('..', 'audio', 'menu_background.mp3'))
        s.menu_background_sound.set_volume(0.5)


    #METHOD FOR RUNNING THE MENU
    def run(s):

        #PLAYING MENU BACKGROUND SOUND
        if s.game.game_state == 'menu':
            s.menu_background_sound.play()
        else:
            s.menu_background_sound.stop()

        #UPDATING THE MENU
        s.update()

        #DRAWING ELEMENTS OF MENU TO DISPLAY
        s.draw()

        #HANDELING THE BUTTON INPUT
        for button in s.buttons:
            button.input(s.game)


    #METHOD FOR DRAWING MENU ELEMENTS
    def draw(s):
            
        #FRAME SKIPPING LOGIC
        frame_skip = randint(0, 10) < 2  #SKIP FRAME WITH 20% CHANCE
        if frame_skip:
            s.frame_skip_counter += 1
            if s.frame_skip_counter % 3 == 0:  #SKIP EVERY THIRD FRAME
                return

        #APPLYING EFFECTS FOR CAMERA STATIC
        modified_image = s.background.copy()
        if randint(0, 10) < 5:  #50% CHANCE TO ADD STATIC NOISE
            modified_image = add_static(modified_image, intensity=300)

        if randint(0, 10) < 3:  #30% CHACNE TO FLICKER BRIGHTNESS
            modified_image = flicker_brightness(modified_image, intensity=randint(-50, 50))

        if randint(0, 10) < 2:  #20% CHANCE TO ADD GLITCH LINES
            modified_image = add_glitch_lines(modified_image)
            
        #DRAWING BACKGROUND
        s.game.display.blit(modified_image, (0,0))

        #DARWING TITLE
        s.game.display.blit(s.title, (20,40))

        #DRAWING NIGHT INFO
        s.game.display.blit(s.night_info, (40, 120))

        #DRAWING BUTTONS
        s.buttons.draw(s.game.display)

        #DRAWING COMPPLETION STATE
        if s.data['COMPLETION_STATE']:
            s.game.display.blit(s.completion_star, s.completion_star_rect)
        
    
    #METHOD FOR UPDATING MENU - FOR THE NIGHT INFO
    def update(s):

        #UPDATNG NIGHT INFO
        s.night_info = s.night_info_font.render(f"Night {s.data['NIGHT_DATA']}", False, (255,255,255))

        #UPDATING MENU ELEMENTS BEFORE DRAWING THEM
        s.buttons.update()
        s.continue_game_button.transparency = s.data['NIGHT_DATA'] == 1
        if s.data['NIGHT_DATA'] > 1:
            s.continue_game_button.image.set_alpha(255)


#BUTTON CLASS
class Button(pygame.sprite.Sprite):

    #BUTTON CONSTRUCTOR
    def __init__(s, text, y_pos, font, game_state_index_return, group, transparancy = False):

        # INITIALIZE PARENT CLASS AND ADD BUTTON TO GROUP
        super().__init__(group)  #AUTOMATICALLY ADD THE BUTTON TO THE BUTTONS GROUP

        #BUTTON ATTRIBUTES
        s.text = text
        s.width = 300
        s.height = 40
        s.x_pos = 20    #STARTING POSITION FOR THE BUTTON
        s.y_pos = y_pos
        s.font = font
        s.game_state_index_return = game_state_index_return
        s.transparency = transparancy

        #INITIALIZING BUTTON
        s.image = s.font.render(s.text, False, (255,255,255))
        s.rect = s.image.get_rect(topleft = (s.x_pos, s.y_pos))

        #MAKING THE BUTTON TRANSPARENT - FOR THE CONTINUE BUTTON IN CASE PLAYER CAN'T CONTINUE
        if s.transparency:
            s.image.set_alpha(80)

        #REACTION RECT
        s.reaction_rect = pygame.Rect(s.x_pos, s.y_pos, WINDOW_WIDTH*0.4, s.height)


    #METHOD FOR UPDATING BUTTON LOOK
    def update(s):

        #GETTING THE MOUSE POSITION
        mouse_pos = pygame.mouse.get_pos()

        #CHECKING IF IT'S THE TRANSPARENT 'CONTINUE' BUTTON
        if s.transparency == False:
            #ANIMATING THE MENU BUTTONS
            if s.reaction_rect.collidepoint(mouse_pos) and s.rect.x < 250:
                s.rect.x += 10  #MOVING TO THE RIGHT
            elif not s.reaction_rect.collidepoint(mouse_pos) and s.rect.x > s.x_pos:
                s.rect.x -= 10  #MOVING BACK TO ORIGINAL POSITION



    #METHOD FOR DRAWING BUTTON TO THE DISPLAY
    def draw(s, game):
            game.display.blit(s.image, s.rect)


    def input(s, game):
        if s.transparency == False:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]


            #HANDING INPUT
            if s.reaction_rect.collidepoint(mouse_pos) and mouse_pressed:

                #RESETTING THE FADE IN BORDER
                if s.text == 'New game':
                    game.data['NIGHT_DATA'] = 1
                    game.level.fade_in_border.reset()
                if s.text == 'Continue':
                    game.level.fade_in_border.reset()

                #TURNING OFF MENU BACKGROUND MUSIC OFF
                game.menu.menu_background_sound.stop()

                #CHANGING THE GAME STATE
                game.game_state = s.game_state_index_return
        