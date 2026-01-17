#IMPORTING LIBRARIES
import pygame
from os import path
from random import randint

#IMPORTING FILES
from settings import *
from efects import add_glitch_lines, add_static, flicker_brightness, Lamp


#CAMERA CLASS / CAMERA SUBSYSTEM FOR LEVEL
class Camera:

    #CAMERA CLASS CONSTRUCTOR
    def __init__(s, game):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #CAMERA ATTRIBUTES
        s.current_camera = 'Stage'
        s.camera_views = {
            1 : {'name' : 'Hallway_left', 'button_pos' : (970,550)},
            2 : {'name' : 'Hallway_right', 'button_pos' : (1055,550)},
            3 : {'name' : 'Stage', 'button_pos' : (995, 380)},
            4 : {'name' : 'Dinning_room', 'button_pos' : (970,435)},
            5 : {'name' : 'Storage', 'button_pos' : (850, 435)},
            6 : {'name' : 'Bathroom', 'button_pos' : (1170, 555)},
            7 : {'name' : 'Pirates_cove', 'button_pos' : (905, 495)}
            }
        
        #CAMERA IMAGES WITH AND WITHOUT ANIMATRONICS
        s.camera_images = {
            'Hallway_left': pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'hallway_left.png')).convert_alpha(),
            'Hallway_right': pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'hallway_right.png')).convert_alpha(),
            'Stage': pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'stage.png')).convert_alpha(),
            'Dinning_room': pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'dinning_room.png')).convert_alpha(),
            'Storage' : pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'storage.png')).convert_alpha(),
            'Bathroom' : pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'bathroom.png')).convert_alpha(),
            'Pirates_cove' : pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_images', 'pirates_cove.png')).convert_alpha(),
        }

        # Resize images
        for key in s.camera_images:
            s.camera_images[key] = pygame.transform.scale(s.camera_images[key], (WINDOW_WIDTH, WINDOW_HEIGHT))

        #CAMERA LAYOUTS
        s.full_camera_layout = pygame.image.load(path.join('..', 'assets', 'camera_assets', 'full_camera_layout.png')).convert_alpha()
        s.full_camera_layout = pygame.transform.scale(s.full_camera_layout, (350,270))
        s.full_camera_layout_rect = s.full_camera_layout.get_rect(bottomright = (WINDOW_WIDTH-50, WINDOW_HEIGHT-60))

        #CREATING THE CAMERA BUTTONS
        s.buttons = [
            Button(
                game=game,
                index=i,
                pos_x=s.camera_views[i]['button_pos'][0],
                pos_y=s.camera_views[i]['button_pos'][1],
                callback=lambda i=i: s.set_camera(i)
            )
            for i in s.camera_views.keys()
        ]

        #LIGHT EFFECT IN SOME CAMERAS - FOR INSTANCE THE HALLWAYS
        s.hallway_right_light = Lamp(s.game, (-10, -408), 385, 10.0, (50, 50, 50))
        s.hallway_left_light = Lamp(s.game, (673, 30), 50, 20.0, (55, 50, 30))


    #METHOD FOR UPDATING LOGIC
    def update(s):
        
        #UPDATING BUTTON STATES
        for button in s.buttons:
            button.update()

        #UPDATING THE LIGHT IN SOME CAMERAS
        if s.current_camera == 'Hallway_right':
            s.hallway_right_light.update()
        if s.current_camera == 'Hallway_left':
            s.hallway_left_light.update()
    

    #METHOD FOR DRAWING CAMERA ELEMENTS
    def draw(s):
        
        #CREATING A NEW SURFACE TO COMBINE ALL LAYERS - FOR APPLYING CAMERA EFFECTS
        combined_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        #DRAWING THE CAMERA IMAGE ONTO THE COMBIEND SURFACE
        camera_name = s.current_camera
        combined_surface.blit(s.camera_images[camera_name], (0, 0))

        #OVERLAYING ANIMATRONICS IF PRESENT
        animatronics_in_view = [anim for anim in s.game.level.animatronics if anim.position == camera_name]
        for anim in animatronics_in_view:
            try:
                anim_sprite = pygame.image.load(path.join('..', 'assets', 'animatronics', f'{anim.name.lower()}_{camera_name.lower()}.png')).convert_alpha()
                anim_sprite = pygame.transform.scale(anim_sprite, (WINDOW_WIDTH, WINDOW_HEIGHT))  #ADJUSTING SIZE TO THE DISPLAY
                combined_surface.blit(anim_sprite, (0, 0))  #ADJUSTING ANIMATRONICS POSITION
            except FileNotFoundError:
                print(f"Error: File for {anim.name.lower()} at {camera_name.lower()} not found.")

        # IF CURRENT CAMERA HAS A LIGHT - DRAW LIGHT GLOW ON THE COMBINED SURFACE
        if s.current_camera == 'Hallway_right':
            s.hallway_right_light.draw_on_surface(combined_surface)
        if s.current_camera == 'Hallway_left':
            s.hallway_left_light.draw_on_surface(combined_surface)

        #APPLYING EFECTS TO THE COMBIEND SURFACE
        if randint(0, 10) < 5:  #50% CHANCE TO ADD STATIC NOISE
            combined_surface = add_static(combined_surface, intensity=300)

        if randint(0, 10) < 3:  #30% CHACNE TO FLICKER BRIGHTNESS
            combined_surface = flicker_brightness(combined_surface, intensity=randint(-50, 50))

        if randint(0, 10) < 2:  #20% CHANCE TO ADD GLITCH LINES
            combined_surface = add_glitch_lines(combined_surface)

        #BLITING THE FINAL COMBIENED AND MODIFIED SURFACE ONTO THE DISPLAY
        s.game.display.blit(combined_surface, (0, 0))

        #DRAWING THE CAMERA LAYOUT
        s.game.display.blit(s.full_camera_layout, s.full_camera_layout_rect)

        #DRAWING THE BUTTONS
        for button in s.buttons:
            button.draw()


    #METHOD FOR SETTIGN CAMERA INDEX
    def set_camera(s, camera_index):
        s.current_camera = s.camera_views[camera_index]['name']


#BUTTON CLASS
class Button(pygame.sprite.Sprite):

    #BUTTON CLASS CONSTRUCTOR
    def __init__(s, game, index, pos_x, pos_y, callback):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #BUTTON ATTRIBUTES
        s.index = index
        s.transperancy = 255
        s.image = pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_buttons', f'{s.index}.png')).convert()
        s.image = pygame.transform.scale(s.image, (55, 31))
        s.rect = s.image.get_rect(topleft = (pos_x, pos_y))
        s.selected_image = pygame.image.load(path.join('..', 'assets', 'camera_assets', 'camera_buttons', '0.png')).convert()
        s.selected_image = pygame.transform.scale(s.selected_image, (55, 31))
        s.callback = callback

        #BUTTON SOUND EFFECT
        s.sound = pygame.mixer.Sound(path.join('..', 'audio', 'camera_switch_button.mp3'))
        s.sound.set_volume(0.4)

        # TIMER FOR BUTTON PRESS DELAY
        s.last_pressed = 0  #STORES LAST TIME BUTTON WAS PRESSED
        s.press_delay = 200  # 0.1 SECOND DELAY IN MILISECONS


    #METHOD FOR DRAWING THE BUTTONS
    def draw(s):
        
        # DRAWING GREEN CAMERA BUTTON IF IT'S SELECTED
        if s.game.level.cameras.current_camera == s.game.level.cameras.camera_views[s.index]['name']:
            s.game.display.blit(s.selected_image, s.rect)
        else:
            s.game.display.blit(s.image, s.rect)

    #METHOD FOR UPDATING THE BUTTONS
    def update(s):

        #GETTING USER INPUT
        s.input()

    #METHOD FOR GETTING PLAYER INPUT
    def input(s):

        #GETTING THE MOUSE POSITION AND STATE
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        current_time = pygame.time.get_ticks()


        #ADJUST TRANSPARENCY WHEN HOVERING OVER BUTTON
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(s.transperancy - 60)
        else:
            s.image.set_alpha(s.transperancy)

        #MAKING THE BUTTON CHANGE THE VIEW WITH THE CALLBACK METHOD
        if mouse_pressed and current_time - s.last_pressed > s.press_delay:
            if s.rect.collidepoint(mouse_pos):
                if not pygame.mixer.get_busy():  #CHECKING IF THE SOUND IS NOT ALREADY PLAYING
                    s.sound.play()
                s.callback()
                s.last_pressed = current_time  #UPDATING THE LAST PRESSED TIME