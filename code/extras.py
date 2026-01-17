#IMPORTING LIBRARIES
import pygame
from os import path, listdir

#IMPORTING FILES
from settings import *


#EXTRAS CLASS
class Extras:

    #EXTRAS CLASS CONSTRUCTOR
    def __init__(s, game):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #CLASS ATTRIBUTES
        s.background = pygame.image.load(path.join('..', 'assets', 'extras_assets', 'background.png')).convert()
        

        #TEXT FONTS
        s.font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 20)

        #MESSAGE FOR THE PLAYER
        s.lines = [
            "You've made it this far... Impressive.",
            "First, thank you for playing.",
            "This project is more than just a game—it's a glimpse into what I can create.",
            "My name is Dariusz, a programmer seeking new challenges. If my work speaks to you...",
            "You know where to find me.",
            "                                                                                              - Dariusz J. Mironczuk",
            "                                                                                              - Rose Violet"
        ]
        
        #RENDERING EACH LINE OF THE TEXT
        s.text = []
        for i, line in enumerate(s.lines):
            s.text.append(s.font.render(line, False, (255, 255, 255)))
        s.rect = [text.get_rect(topleft=(60, 50 + i * 40)) for i, text in enumerate(s.text)]

        #BUTTONS GROUP AND INITALIZING
        s.button_group = pygame.sprite.Group()
        for i, file in enumerate(listdir(path.join('..', 'audio', 'phone_guy'))):  
            Button(s.game, s.button_group, 380 + i * 60, i+1)
        StopButton(s.game, s.button_group)
        s.back_button = BackButton(s.game)



    #METHOD FOR RUNNING THE EXTRAS 'MENU'
    def run(s):
        
        #GETTING USER INPUT
        s.input()

        #UPDATING THE EXTRAS
        s.update()

        #DRAWING THE EXTRAS
        s.draw()



    #METHOD FOR UPDATING THE EXTRAS 'MENU'
    def update(s):
        
        #UPDATING THE BUTTONS
        s.button_group.update()
        s.back_button.update()
        

    #METHOD FOR DRAWING THE ELEMENTS
    def draw(s):

        #DRAWING THE BACKGROUND
        s.game.display.blit(s.background, (0,0))

        #DRAWING THE MESSAGE
        for i, line in enumerate(s.text):
            s.game.display.blit(line, s.rect[i])

        #DRAWING THE BUTTONS
        for button in s.button_group:
            button.draw()
        s.back_button.draw()        


    #METHOD FOR USER INPUT
    def input(s):
        pass



#BUTTON CLASS
class Button(pygame.sprite.Sprite):

    #BUTTON CLASS CONSTRUCTOR
    def  __init__(s, game, groups, pos_y, night):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #INITIALIZNG INHERITANCE
        super().__init__(groups)

        #BUTTON ATTRIBUTES
        s.image = pygame.image.load(path.join('..', 'assets', 'extras_assets', 'extras_button.png')).convert()
        s.image = pygame.transform.scale(s.image, (580, 50))
        s.rect = s.image.get_rect(topleft = (660, pos_y))
        s.night = night

        #FONT AND TEXT
        s.font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 35)
        s.text = s.font.render(f"NIGHT {s.night}", False, (0,0,0))
        s.text_rect = s.text.get_rect(center = (s.rect.centerx, s.rect.centery+5))

        #AUDIO 
        s.sound = pygame.mixer.Sound(path.join('..', 'audio', 'phone_guy', f"{s.night}.mp3"))
        s.sound.set_volume(1)


    #METHOD FOR UPDATING BUTTON
    def update(s):

        #GETTING USER INPUT
        s.input()


    #METHOD FOR DRAWING BUTTONS
    def draw(s):

        s.game.display.blit(s.image, s.rect)
        s.game.display.blit(s.text, s.text_rect)


    #METHOD FOR BUTTON INPUT
    def input(s):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # MAKING THE BUTTON TRANSPARENT WHEN HOVERING OVER IT
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(100)
        else:
            s.image.set_alpha(255)

        # PRESSING THE BUTTON
        if s.rect.collidepoint(mouse_pos) and mouse_pressed:
            pygame.mixer.stop()  # STOP ALL OTHER SOUNDS FIRST
            s.sound.play()  # PLAY THE NEW SOUND

#STOP BUTTON CLASS
class StopButton(pygame.sprite.Sprite):

    #BUTTON CLASS CONSTRUCTOR
    def  __init__(s, game, group):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #INITIALIZNG INHERITANCE
        super().__init__(group)

        #BUTTON ATTRIBUTES
        s.image = pygame.image.load(path.join('..', 'assets', 'extras_assets', 'extras_button.png')).convert()
        s.image = pygame.transform.scale(s.image, (300, 70))
        s.image = pygame.transform.rotate(s.image, 90)
        s.rect = s.image.get_rect(topleft = (580, 378))

        #FONT AND TEXT
        s.font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)
        s.text = s.font.render('STOP', False, (0,0,0))
        s.text = pygame.transform.rotate(s.text, 90)
        s.text_rect = s.text.get_rect(center = (s.rect.centerx+10, s.rect.centery))


    #METHOD FOR UPDATING BUTTON
    def update(s):

        #GETTING USER INPUT
        s.input()


    #METHOD FOR DRAWING BUTTONS
    def draw(s):

        s.game.display.blit(s.image, s.rect)
        s.game.display.blit(s.text, s.text_rect)


    #METHOD FOR BUTTON INPUT
    def input(s):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # MAKING THE BUTTON TRANSPARENT WHEN HOVERING OVER IT
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(100)
        else:
            s.image.set_alpha(255)

        # PRESSING THE BUTTON
        if s.rect.collidepoint(mouse_pos) and mouse_pressed:
            pygame.mixer.stop()  # STOP ALL OTHER SOUNDS FIRST

class BackButton():

    #SAVE / CANCEL BUTTON CLASS
    def __init__(s, game):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #SAVE / CANCEL BUTTON ATTRIBUTES
        s.image = pygame.image.load(path.join('..', 'assets', 'options_assets', 'save_cancel_button.png')).convert()
        s.image = pygame.transform.scale(s.image, (350, 100))
        s.rect = s.image.get_rect(bottomleft = (100, WINDOW_HEIGHT - 100))

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
            s.game.game_state = 'menu'
            