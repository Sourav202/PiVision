# IMPORTING LIBRARIES
import pygame
from os import path
from random import randint, random
import time

# IMPORTING FILES
from settings import *
from efects import Lamp, add_static, flicker_brightness, add_glitch_lines
from math import sin


class Office:
    def __init__(s, game):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        # POWER ATTRIBUTES
        s.POWER = 100
        s.LIGHT_POWER_CONSUMPTION = 0.01
        s.DOOR_POWER_CONSUMPTION = 0.03

        #ANIMATRONIC TIME TO JUMPSCARE IF DOOR ISN'T CLOSED
        s.time_for_animatronic_to_jumpscare = 15000     #15 SEC IN MILISECONDS

        # LIGHT ATTRIBUTES
        s.left_light_on = False
        s.right_light_on = False

        #DOOR ATTRIBUTES
        s.left_door_on = False
        s.right_door_on = False

        #WINDOW OCCUPATION ATTRIBUTES
        s.left_window_occupied_by = None
        s.right_window_occupied_by = None

        # OFFICE BACKGROUND
        s.office_width = 2000  #FULL WIDTH OF THE BACKGROUND
        s.office = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_background.png')).convert_alpha()
        s.office = pygame.transform.scale(s.office, (s.office_width, WINDOW_HEIGHT))  #SCALING THE BACKGROUND TO FIT CORRECTLY AND WORK WITH THE OFFSET

        #OFFICE BACKGROUND - NO POWER
        s.office_no_power = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_background_no_power.png')).convert_alpha()
        s.office_no_power = pygame.transform.scale(s.office_no_power, (s.office_width, WINDOW_HEIGHT))

        #POWER METER ICON
        s.power_icon = pygame.image.load(path.join('..', 'assets', 'office_assets', 'power_icon.png')).convert_alpha()
        s.power_icon = pygame.transform.scale(s.power_icon, (150, 75))
        s.power_icon_rect = s.power_icon.get_rect(topleft = (10, 10))
        s.power_meter = pygame.Surface((s.POWER*1.15, 42))
        s.power_meter.fill('green')

        #OFFICE WINDOWS
        s.left_window = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_left_window.png')).convert_alpha()
        s.right_window = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_right_window.png')).convert_alpha()
        s.left_window = pygame.transform.scale(s.left_window, (s.office_width, WINDOW_HEIGHT))        #SCALING THE LEFT WINDOW
        s.right_window = pygame.transform.scale(s.right_window, (s.office_width, WINDOW_HEIGHT))      #SCALING THE RIGHT WINDOW

        #ANIMATRONIC WINDOW POSITIONS
        s.left_window_position = 'Left_window'
        s.right_window_position = 'Right_window'

        #ANIMATRONIC IMAGES AT WINDOWS
        s.animatronic_images = {
            'Chicka': pygame.transform.scale(pygame.image.load(path.join('..', 'assets', 'animatronics', 'chicka_right_window.png')).convert_alpha(), (s.office_width, WINDOW_HEIGHT)),
            'Freddy': pygame.transform.scale(pygame.image.load(path.join('..', 'assets', 'animatronics', 'freddy_right_window.png')).convert_alpha(), (s.office_width, WINDOW_HEIGHT)),
            'Bonnie': pygame.transform.scale(pygame.image.load(path.join('..', 'assets', 'animatronics', 'bonnie_left_window.png')).convert_alpha(), (s.office_width, WINDOW_HEIGHT))
        }

        #TIMEOUT FOR ANIMATRONICS AT WINDOWS
        s.animatronic_reset_time = 5000     #5 SECONS
        s.animatronic_timers = {}

        #JUMPSCARE ATTRIBUTES
        s.jumpscare_triggered = False   #TRACKS IF JUMPSCARE IS ACTIVE
        s.jumpscare_animatronic = None  #STORES WHICH ANIMATRONIC TRIGGERED THE JUMPSCARE
        s.jumpscare_timer = {}      #TRACKS TIME SPENT AT THE WINDOW FOR EACH ANIMATRONIC

        #JUMPSCARE AUDIO ATTRIBUTES
        s.jumpscare_sound = pygame.mixer.Sound(path.join('..', 'audio', 'jumpscare.mp3'))
        s.jumpscare_sound.set_volume(1)  # 100% VOLUME

        #OFFICE ENTRANCES
        s.left_entrance = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_background_door_entrance_left.png')).convert_alpha()
        s.right_entrance = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_background_door_entrance_right.png')).convert_alpha()
        s.right_entrance = pygame.transform.scale(s.right_entrance, (s.office_width, WINDOW_HEIGHT))
        s.left_entrance = pygame.transform.scale(s.left_entrance, (s.office_width, WINDOW_HEIGHT))

        #OFFICE DOORS
        s.left_door = pygame.image.load(path.join('..', 'assets', 'office_assets', 'left_door.png')).convert_alpha()
        s.right_door = pygame.image.load(path.join('..', 'assets', 'office_assets', 'right_door.png')).convert_alpha()
        s.left_door = pygame.transform.scale(s.left_door, (s.office_width, WINDOW_HEIGHT))
        s.right_door = pygame.transform.scale(s.right_door, (s.office_width, WINDOW_HEIGHT))

        #VIEW OFFSET FOR TRACKING THE CURRENT OFFSET
        s.offset = 0

        #LEFT / RIGHT BUTTONS
        s.left_button = Button(s.game, s, 'movement_button_left.png', 'left', 180)
        s.right_button = Button(s.game, s, 'movement_button_right.png', 'right', 400)

        #LIGHT BUTTON LEFT IMAGE
        s.left_light_button = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_left_light_button.png')).convert_alpha()
        s.left_light_button = pygame.transform.scale(s.left_light_button, (s.office_width, WINDOW_HEIGHT))

        #RIGHT BUTTON RIGHT IMAGE
        s.right_light_button = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_right_light_button.png')).convert_alpha()
        s.right_light_button = pygame.transform.scale(s.right_light_button, (s.office_width, WINDOW_HEIGHT))

        #RECTANGLE FOR THE LIGHT BUTTON
        s.transparent_surface_light_button = pygame.Surface((90,200))
        s.transparent_surface_light_button.fill((255,255,255))
        s.transparent_surface_light_button.set_alpha(10)
        s.right_light_button_rect = s.transparent_surface_light_button.get_rect(topright = (s.office_width-50, WINDOW_HEIGHT-260))
        s.left_light_button_rect = s.transparent_surface_light_button.get_rect(topleft = (10, WINDOW_HEIGHT-260))

        #DOOR BUTTON LEFT IMAGE
        s.left_door_button = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_left_door_button.png')).convert_alpha()
        s.left_door_button = pygame.transform.scale(s.left_door_button, (s.office_width, WINDOW_HEIGHT))

        #DOOR BUTTON RIGHT IMAGE
        s.right_door_button = pygame.image.load(path.join('..', 'assets', 'office_assets', 'office_right_door_button.png')).convert_alpha()
        s.right_door_button = pygame.transform.scale(s.right_door_button, (s.office_width, WINDOW_HEIGHT))

        #LIGHT ON AND OFF SOUND
        s.light_on_sound = pygame.mixer.Sound(path.join('..', 'audio', 'light_on.mp3'))
        s.light_on_sound.set_volume(1)

        #RECTANGLE FOR THE DOOR BUTTON
        s.transparent_surface_door_button = pygame.Surface((90,200))
        s.transparent_surface_door_button.fill((255,0,0))
        s.transparent_surface_door_button.set_alpha(10)
        s.right_door_button_rect = s.transparent_surface_door_button.get_rect(topright = (s.office_width-50, WINDOW_HEIGHT-480))
        s.left_door_button_rect = s.transparent_surface_door_button.get_rect(topleft = (10, WINDOW_HEIGHT-480))

        #DOOR CLOSED AND OPEN SOUND
        s.door_open_sound = pygame.mixer.Sound(path.join('..', 'audio', 'door_open.mp3'))
        s.door_open_sound.set_volume(1)  # 100% VOLUME
        s.door_closed_sound = pygame.mixer.Sound(path.join('..', 'audio', 'door_closed.mp3'))
        s.door_closed_sound.set_volume(1)  # 100% VOLUME

        #COOLDOWN DICTONARY FOR DOOR TOGGLES
        s.key_cooldowns = {
            pygame.K_a: 0,  #COOLDOWN FOR THE 'A' KEY - LEFT DOOR
            pygame.K_s: 0,  #COOLDOWN FOR THE 'S' KEY - RIGHT DOOR
            'right_door_button': 0, #COOLDOWN FOR THE MOUSE INPUET - RIGHT DOOR
            'left_door_button': 0    #COOLDOWN FOR THE MOUSE INPUET - LEFT DOOR
        }
        s.cooldown_duration = 0.5  #COOLDOWN DURATION IN SECONDS FOR BUTTON DOOR INPUT
        s.mouse_cooldown_duration = 0.5 #COOLDOWN DURETION IN SECONDS FOR MOUSE DOOR INPUT

        #LAMP FOR ATMOSPHERE
        s.lamp = Lamp(s.game, pos = (860, -105), radius = 110)


    #METHOD FOR UPDATING OFFICE
    def update(s):

        #HANDLING USER INPUT
        s.input()

        #LIGHT POWER LOGIC
        if s.left_light_on or s.right_light_on:
            s.POWER -= s.LIGHT_POWER_CONSUMPTION

        #DOOR POWER LOGIC
        if s.left_door_on:
            s.POWER -= s.DOOR_POWER_CONSUMPTION
        if s.right_door_on:
            s.POWER -= s.DOOR_POWER_CONSUMPTION

        #UPDATING LAMP FOR FLICKERING
        s.lamp.update()

        #UPDATING MOVEMENT BUTTONS
        s.left_button.update()
        s.right_button.update()

        #UPDARING THE POWER METER
        s.power_meter = pygame.Surface((s.POWER*1.15, 42))
        s.power_meter.fill('dark green')

        #HANDLING ANIMATRONICS AT WINDOWS
        s.update_animatronics()


    #METHOD FOR UPDATING THE ANIMATRONICS
    def update_animatronics(s):
        s.left_window_occupied_by = None  #RESETTING TRACKING FOR THIS FRAME
        s.right_window_occupied_by = None  #RESETTING TRACKING FOR THIS FRAME

        #CORRECTING THE VIEW IF IT IS OCCUPIED
        for animatronic in s.game.level.animatronics:
            if animatronic.position == s.left_window_position:
                if s.left_window_occupied_by is None:  #CHECKING IF THE WINDOW IS UNOCCUPIED
                    s.left_window_occupied_by = animatronic.name
                    s.handle_window_interaction(animatronic, 'left')
            elif animatronic.position == s.right_window_position:
                if s.right_window_occupied_by is None:  #CHECKING IF THE WINDOW IS UNOCCUPIED
                    s.right_window_occupied_by = animatronic.name
                    s.handle_window_interaction(animatronic, 'right')


    #METHOD FOR DRAWING OFFICE ELEMENTS
    def draw(s):

        #DRAWING THE JUMPSCARE! 
        if s.jumpscare_triggered:
            s.draw_jumpscare()
            return  #SKIPPING THE REST OF THE LOGIC

        # FILLING THE BACKGROUND BLACK TO STOP GHOSTING
        s.game.display.fill((0, 0, 0))

        #DRAWING THE OFFICE ENTRANCES
        s.game.display.blit(s.right_entrance, (s.offset, 0))
        s.game.display.blit(s.left_entrance, (s.offset, 0))

        #DRAWING DOORS IF DOORS ON
        if s.left_door_on:
            s.game.display.blit(s.left_door, (s.offset, 0))
        if s.right_door_on:
            s.game.display.blit(s.right_door, (s.offset, 0))

        # DRAWING THE OFFICE WINDOWS IF LIGHT IS ON
        if s.left_light_on:
            s.game.display.blit(s.left_window, (s.offset, 0))
            s.draw_animatronic_at_window('left')

        if s.right_light_on:
            s.game.display.blit(s.right_window, (s.offset, 0))
            s.draw_animatronic_at_window('right')


        #DRAWING OFFICE ELEMENTS WHEN THERE IS POWER
        if s.POWER > 0:
            #DRAWING THE OFFICE WITH THE OFFSET
            s.game.display.blit(s.office, (s.offset, 0))

            #DRAWING LAMP / GLOW EFFECT 
            s.lamp.draw(s.offset)

        #DARING THE BACKGROUND WITH NO POWER
        else:
            s.game.display.blit(s.office_no_power, (s.offset, 0))

        #DRAWING LIGHT BUTTONS IF LIGHT IS ON
        if s.left_light_on:
            s.game.display.blit(s.left_light_button, (s.offset, 0))
        if s.right_light_on:
            s.game.display.blit(s.right_light_button, (s.offset, 0))

        #DRAWING/CHANGING THE DOOR BUTTON IF DOORS IS ON
        if s.left_door_on:
            s.game.display.blit(s.left_door_button, (s.offset, 0))
        if s.right_door_on:
            s.game.display.blit(s.right_door_button, (s.offset, 0))

        #DRAWING MOVEMENT BUTTONS
        s.left_button.draw()
        s.right_button.draw()

        #DRAWING LIGHT BUTTONS
        s.game.display.blit(s.transparent_surface_light_button, s.right_light_button_rect.move(s.offset, 0))
        s.game.display.blit(s.transparent_surface_light_button, s.left_light_button_rect.move(s.offset, 0))

        #DRAWING THE DOOR BUTTONS
        s.game.display.blit(s.transparent_surface_door_button, s.right_door_button_rect.move(s.offset, 0))
        s.game.display.blit(s.transparent_surface_door_button, s.left_door_button_rect.move(s.offset, 0))

        #DRAWING POWER ICON
        s.game.display.blit(s.power_icon, s.power_icon_rect)
        s.game.display.blit(s.power_meter, (s.power_icon_rect.x+12, s.power_icon_rect.y+16))


    #METHOD FOR HANDLING USER INPUT
    def input(s):

        #GETTING MOUSE POSITION AND INPUT
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        #GETTING ALL KEYS PRESSED BY USER
        keys = pygame.key.get_pressed()

        #CURRENT TIME
        current_time = time.time()

        #SLIDING BACKGROUND LOGIC
        if keys[pygame.K_RIGHT]:  #SLIDE LEFT
            s.offset = max(s.offset - 10, -s.office_width + 1280)  #LIMIT TO LEFT EDGE OF THE BACKGROUND
        if keys[pygame.K_LEFT]:  #SLIDE RIGHT
            s.offset = min(s.offset + 10, 0)  #LIMIT TO RIGHT EDGE OF THE BACKGROUND

        
        #CHECKING IF THE PLAYER HAS POWER
        if s.POWER > 0:     #IF YES, DO THE ON AND OFF STUFF

            # LIGHT ON/OFF LOGIC WITH BUTTONS
            if keys[pygame.K_q]: 
                if not s.left_light_on:  # Play sound only when changing state
                    s.light_on_sound.play()
                s.left_light_on = True
            else:
                s.left_light_on = False

            if keys[pygame.K_w]: 
                if not s.right_light_on:  # Play sound only when changing state
                    s.light_on_sound.play()
                s.right_light_on = True
            else:
                s.right_light_on = False

            #LEFT DOOR TOGGLE LOGIC
            if keys[pygame.K_a] and current_time > s.key_cooldowns[pygame.K_a]:
                s.left_door_on = not s.left_door_on
                s.key_cooldowns[pygame.K_a] = current_time + s.cooldown_duration

                #PLAY SOUND EFFENCT BASED ON DOOR STATE
                if s.left_door_on:
                    s.door_closed_sound.play()  #PLAY CLOSING SOUND
                else:
                    s.door_open_sound.play()  #PLAY OPENING SOUND

            #RIGHT DOOR TOGGLE LOGIC
            if keys[pygame.K_s] and current_time > s.key_cooldowns[pygame.K_s]:
                s.right_door_on = not s.right_door_on
                s.key_cooldowns[pygame.K_s] = current_time + s.cooldown_duration

                #PLAY SOUND EFFENCT BASED ON DOOR STATE
                if s.right_door_on:
                    s.door_closed_sound.play()  #PLAY CLOSING SOUND
                else:
                    s.door_open_sound.play()  #PLAY OPENING SOUND

            #LIGHT ON/OFF LOGIC WITH MOUSE
            if s.right_light_button_rect.collidepoint(mouse_pos) and mouse_pressed:
                s.right_light_on = True
            if s.left_light_button_rect.collidepoint(mouse_pos) and mouse_pressed:
                s.left_light_on = True

            #DOOR ON/OFF LOFIC WITH MOUSE
            #ADJUSTING COLLISIONCHECKS FOR THE RIGHT DOOR BUTTON
            if (
                s.right_door_button_rect.move(s.offset, 0).collidepoint(mouse_pos)
                and mouse_pressed
                and current_time > s.key_cooldowns['right_door_button']
            ):
                s.right_door_on = not s.right_door_on
                s.key_cooldowns['right_door_button'] = current_time + s.mouse_cooldown_duration

                #PLAY SOUND EFFENCT BASED ON DOOR STATE
                if s.right_door_on:
                    s.door_closed_sound.play()  #PLAY CLOSING SOUND
                else:
                    s.door_open_sound.play()  #PLAY OPENING SOUND

            #ADJUSTING COLLISIONCHECKS FOR THE LEFT DOOR BUTTON
            if (
                s.left_door_button_rect.move(s.offset, 0).collidepoint(mouse_pos)
                and mouse_pressed
                and current_time > s.key_cooldowns['left_door_button']
            ):
                s.left_door_on = not s.left_door_on
                s.key_cooldowns['left_door_button'] = current_time + s.mouse_cooldown_duration

                #PLAY SOUND EFFENCT BASED ON DOOR STATE
                if s.left_door_on:
                    s.door_closed_sound.play()  #PLAY CLOSING SOUND
                else:
                    s.door_open_sound.play()  #PLAY OPENING SOUND


            #ADJUSTING COLLISIONCHECKS FOR THE RIGHT LIGHT BUTTON
            if s.right_light_button_rect.move(s.offset, 0).collidepoint(mouse_pos) and mouse_pressed:
                s.right_light_on = True

            #ADJUSTING COLLISIONCHECKS FOR THE LEFT LIGHT BUTTON
            if s.left_light_button_rect.move(s.offset, 0).collidepoint(mouse_pos) and mouse_pressed:
                s.left_light_on = True

        #IF THE IS NO MORE POWER, TURN OFF EVERYTHING
        else:
            s.left_door_on = False
            s.right_door_on = False
            s.left_light_on = False
            s.right_light_on = False


    #METHOD FOR HANDLING ANIMATRONICS AT WINDOWS
    def handle_window_interaction(s, animatronic, side):
        #CHECKING WHICK SIDE OF THE WINDOW IS OCCUPIED
        occupied_by = s.left_window_occupied_by if side == 'left' else s.right_window_occupied_by

        if occupied_by != animatronic.name:
            return  #EXIT IF ANOTHER ANIMATRONIC IS OCCUPYING THE WINDOW

        #CHECKING THE DOOR STATE
        door_state = s.left_door_on if side == 'left' else s.right_door_on

        current_time = pygame.time.get_ticks()

        #IF DOOR IS CLOSED START TRACKING RESET TIME
        if door_state:
            if animatronic.name not in s.animatronic_timers:
                s.animatronic_timers[animatronic.name] = current_time  #START TIMER

            elif current_time - s.animatronic_timers[animatronic.name] >= s.animatronic_reset_time:
                #IF DOOR IS CLOSED FOR 5 SECONDS, SENDING ANIMATRONIC BACK TO BEGUINING OF PATH
                animatronic.position = s.game.level.animatronic_paths.get(animatronic.name, [None])[0]  #RESET POSITION
                s.animatronic_timers.pop(animatronic.name, None)  #REMOVE TIMER
                s.jumpscare_timer.pop(animatronic.name, None)  #RESET ATTACK TIMER
        else:
            #IF DOOR IS OPEN RESETING THE 'CLOSED' TIMER AND TRACKING TIME AT WINDOW
            if animatronic.name in s.animatronic_timers:
                del s.animatronic_timers[animatronic.name]  #RESET DOOR IF OPEN

            if animatronic.name not in s.jumpscare_timer:
                s.jumpscare_timer[animatronic.name] = current_time
            else:
                elapsed_time = current_time - s.jumpscare_timer[animatronic.name]
                if elapsed_time >= s.time_for_animatronic_to_jumpscare:  
                    s.trigger_jumpscare(animatronic)


    #METHOD FOR TRIGGERING JUMPSCARES
    def trigger_jumpscare(s, animatronic):
        s.jumpscare_triggered = True
        s.jumpscare_animatronic = animatronic
        s.jumpscare_timer.clear()  #CLEARING ALL TIMERS

        #MUTE ALL SOUNDS
        pygame.mixer.stop()  #STOPS ALL CURRENTLY PLAYING SOUNDS

    #METHOD FOR DRAWING JUMPSCARES
    def draw_jumpscare(s):
        if not s.jumpscare_animatronic:
            return

        #JUMPSCARE 'ATTRIBUTES'
        jumpscare_frames = s.jumpscare_animatronic.jumpscare_frames
        num_frames = len(jumpscare_frames)
        frame_duration = 70  #EACH FRAME LASTS 70 MILISECONDS - 'IDEAL' FOR 21 FRAMES OF THE JUMPSCARE
        total_animation_time = num_frames * frame_duration  #TOTAL DURATION OF ANIMATION

        #INITIALIZING START TIME IF NOT SET
        if not hasattr(s, "jumpscare_start_time"):
            s.jumpscare_start_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - s.jumpscare_start_time
        current_frame = min(elapsed_time // frame_duration, num_frames - 1)  #PREVENTING INDEX OUT OF RANGE

        #RANDOM CAMERA SHAKE
        shake_x = randint(-20, 20)
        shake_y = randint(-20, 20)

        #DARKENING OF THE OFFICE
        darkened_office = s.office_no_power.copy()
        darkened_office.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_SUB)
        s.game.display.blit(darkened_office, (s.offset + shake_x, shake_y))

        #TAKING THE CURRENT JUMPSCARE FRAME TO ADDING EDDECTS
        jumpscare_image = jumpscare_frames[current_frame].copy()
        
        #ADDING EFFECTS
        jumpscare_image = flicker_brightness(jumpscare_image, intensity=randint(30, 80))
        jumpscare_image = add_static(jumpscare_image, intensity=100)
        jumpscare_image = add_glitch_lines(jumpscare_image)

        #DRAWING THE IMAGE WITH THE CAMERA SHAKE
        s.game.display.blit(jumpscare_image, (shake_x, shake_y))

        #FLASHING LIGHT EFFERCT (20%)
        if random() < 0.2:
            flash_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            flash_overlay.fill((255, 255, 255, 100))
            s.game.display.blit(flash_overlay, (0, 0))

        #PILSATING BLOOD EFFECT
        blood_overlay = pygame.image.load(path.join('..', 'assets', 'effects', 'blood_overlay.png')).convert_alpha()
        blood_overlay = pygame.transform.scale(blood_overlay, (WINDOW_WIDTH, WINDOW_HEIGHT))

        #PULSATING TRANSPARENCY EFFECT
        pulsate_alpha = 80 + 40 * sin(elapsed_time * 0.005)
        blood_overlay.set_alpha(int(pulsate_alpha))
        s.game.display.blit(blood_overlay, (0, 0))


        #PLAYING THE JUMPSCARE AUDIO
        if s.jumpscare_triggered:  #THE JUMPSCARE STARTS
            if not pygame.mixer.get_busy():  #PREVENT OVERLAPPING SOUNDS
                s.jumpscare_sound.play()

        #IF THE JUMPSCARE ANIMATION IS FINISHED, SWITCHING THE VIEW
        if elapsed_time >= total_animation_time:

            #CHANGING THE LEVEL STATE TO SHOW THE FADE OUT
            s.game.level.current_view = 'fade_out'


    #METHOD FOR DRAWING ANIMATRONICS AT THE WINDOW
    def draw_animatronic_at_window(s, side):
        if side == 'left' and s.left_window_occupied_by:
            animatronic_name = s.left_window_occupied_by
            animatronic_image = s.animatronic_images.get(animatronic_name)
            if animatronic_image:
                s.game.display.blit(animatronic_image, (s.offset, 0))

        elif side == 'right' and s.right_window_occupied_by:
            animatronic_name = s.right_window_occupied_by
            animatronic_image = s.animatronic_images.get(animatronic_name)
            if animatronic_image:
                s.game.display.blit(animatronic_image, (s.offset, 0))


#BUTTON CLASS
class Button:

    #BUTTON CLASS CONSTRUCTOR
    def __init__(s, game, office, image, direction, pos_x):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #TURNING OFFICE IN TO AN ATTRIBUTE
        s.office = office

        #TURNING DIRECTION IN TO AN ATTRIBUTE
        s.direction = direction

        #BUTTON ATTRIBUTES
        s.image = pygame.image.load(path.join('..', 'assets', 'office_assets', image)).convert_alpha()
        s.image = pygame.transform.scale(s.image, (200, 40))
        s.rect = s.image.get_rect(bottomleft = (pos_x, WINDOW_HEIGHT-5))

        #TRANSPARANCY LOGIC
        s.transperancy = 150


    #METHOD TO UPDATE THE BUTTON
    def update(s):

        #HANDELING USER INPUT
        s.input()
    

    #METHOD FOR DRAWING BUTTON
    def draw(s):

        #DRAWING THE BUTOTN TO DISPLAY    
        s.game.display.blit(s.image, s.rect)


    #METHOD FOR GETTING USER INPUT
    def input(s):

        #GETTING THE MOUSE POSITION AND STATE
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        #ADJUST TRANSPARENCY WHEN HOVERING OVER BUTTONS
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(s.transperancy - 50)
        else:
            s.image.set_alpha(s.transperancy)

        #CONTINUOUS MOVEMENT WHEN BUTTON IS CLICKED
        if s.rect.collidepoint(mouse_pos) and mouse_pressed:
            if s.direction == 'left':
                #MOVE BACKGROUND TO THE LEFT
                s.office.offset = min(s.office.offset + 10, 0)
            elif s.direction == 'right':
                #MOVE BACKGROUND TO THE RIGHT
                s.office.offset = max(s.office.offset - 10, -s.office.office_width + 1280)
        