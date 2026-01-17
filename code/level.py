#IMPORTING LIBRARIES
import pygame
from os import path, listdir
import time

#IMPORTING FILES
from settings import *
from office import Office
from cameras import Camera
from animatronics import Animatronic


#LEVEL CLASS
class Level:

    #LEVEL CONSTRUCTOR
    def __init__(s, game, data):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #TURNING MENU DATA IN TO AN ATTRIBUTE
        s.data = data

        #CREATING A FADE-IN AND FADE-OUT BORDER - FROM CLASS BELLOW
        s.fade_in_border = FadeIn(s.game, s.data)
        s.fade_out_border = FadeOut(s.game)

        #CURRENT CAMERA VIEW
        s.current_view = 'office'     #CURRENT VIEW: 'OFFICE' OR 'CAMERAS'

        #TIME TRACKING
        s.night_leangth = 45000     #HOW LONG THE NIGHT WILL BE - IN MILISECONDS
        s.time = 0      #STARTS AT 0AM
        s.last_time_update = pygame.time.get_ticks()    #TRAK THE LAST TIME UPDATE - IN MILLISECONDS

        #INITIALIZING SUBSYSTEMS
        s.office = Office(s.game)
        s.cameras = Camera(s.game)
        s.view_switch_button = Button(s.game, s)
        s.win_screen = NightEnded(s.game)

        #LEVEL INFO
        s.night_info_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 20)
        s.night_info = s.night_info_font.render(f"Night {s.game.data['NIGHT_DATA']}\n{s.time} AM", False, (255,255,255))
        s.night_info_rect = s.night_info.get_rect(topright = (WINDOW_WIDTH-10, 10))

        #ANIMATRONIC PATHS TO OFFICE
        s.animatronic_paths = {
            'Chicka' : ['Stage', 'Dinning_room', 'Bathroom', 'Hallway_right' 'Right_window'],
            'Freddy' : ['Stage', 'Stage', 'Stage', 'Right_window'],
            'Bonnie' : ['Stage', 'Storage', 'Dinning_room', 'Hallway_left', 'Left_window']
        }

        #INITIALIZNG ANIMATRONICS
        s.animatronics = [
            Animatronic(s.game, 'Chicka', 'Stage', s.animatronic_paths['Chicka']),
            Animatronic(s.game, 'Freddy', 'Stage', s.animatronic_paths['Freddy']),
            Animatronic(s.game, 'Bonnie', 'Stage', s.animatronic_paths['Bonnie'])
        ]

        #NIGHT WON SOUND EFFECT
        s.night_won_sound = pygame.mixer.Sound(path.join('..', 'audio', 'night_won.mp3'))
        s.night_won_sound.set_volume(1.2)

        #CAMERA ON AND OFF SOUND EFFECTS
        s.camera_view_on_sound = pygame.mixer.Sound(path.join('..', 'audio', 'camera_view_on.mp3'))
        s.camera_view_on_sound.set_volume(1)
        s.camera_view_off_sound = pygame.mixer.Sound(path.join('..', 'audio', 'camera_view_off.mp3'))
        s.camera_view_off_sound.set_volume(1)

        #PHONE GUY SOUND
        s.phone_guy_call = pygame.mixer.Sound(path.join('..', 'audio', 'phone_guy', f"{s.data['NIGHT_DATA']}.mp3"))
        s.phone_guy_call.set_volume(1)
        s.phone_guy_played = False


    #METHOD FOR RUNNING THE LEVEL
    def run(s):

        #UPDATING THE LEVEL BEFORE DRAWING IT
        s.update()

        #DRAWING THE LEVEL ELEMENTS
        s.draw()


    #METHOD FOR DRAWING THE LEVEL AND IT'S ELEMENTS
    def draw(s):

        #DRAWING OFFICE ELEMENTS
        if s.current_view == 'office':
            s.office.draw()

        #DRAWING CAMERA ELEMENTS
        elif s.current_view == 'cameras':
            s.cameras.draw()

        #DRAWING THE FADE OUT - (YOU CAN ADD SOME RANDOM SPECIAL ENCOUNTERS OR STUFF)
        elif s.current_view == 'fade_out':
            s.fade_out_border.draw()
            s.fade_out_border.update()

        #DRAWING THE NIGHT AND TIME INFO
        s.game.display.blit(s.night_info, s.night_info_rect)

        #DRAWING THE VIEW CHANING BUTTON
        if s.office.jumpscare_triggered == False:
            s.view_switch_button.draw()

        #DRAWING THE FADE IN BORDER
        s.fade_in_border.draw()

        #IF IT'S 6AM , TRIGGER THE WIN SCREEN FADE IN EFFECT
        if s.time == 6:
            s.win_screen.draw()

    
    #METHOD FOR UPDATING LEVEL ELEMENTS
    def update(s):

        #UPDATING OFFICE ELEMENTS
        s.office.update()

        #UPDATING CAMERA ELEMENTS
        s.cameras.update()

        #UPDATING THE VIEW CHANGE BUTTON
        s.view_switch_button.update()

        #UPDATING THE FADE IN BORDER
        s.fade_in_border.update()

        #TIME PASSING LOGIC
        current_time = pygame.time.get_ticks()  #GETTING CURRENT TIME
        if current_time - s.last_time_update >= s.night_leangth:      #IF CURRENT_TIME - LAST_TIME_UPDATE ARE = TO 45 SEC
            s.last_time_update = current_time
            s.time += 1

        #MOVING THE ANIMATRONICS LOGIC
        for animatronic in s.animatronics:
            animatronic.move(s.data['NIGHT_DATA'], s.game.aggression_data[f'{animatronic.name}'])

        #UPDATING THE NIGHT_INFO WITH CORRECT TIME
        s.night_info = s.night_info_font.render(f"Night {s.data['NIGHT_DATA']}\n{s.time} AM", False, (255,255,255))

        #IF IT'S 6AM , UPDATE THE WIN SCREEN
        if s.time == 6:
            #MUTE ALL SOUNDS
            pygame.mixer.stop()  #STOPS ALL CURRENTLY PLAYING SOUNDS
            s.night_won_sound.play()
            s.win_screen.update()

        #IF IT'S 1AM, PLAY THE PHONE GUY
        if s.time == 1 and not s.phone_guy_played:
            s.phone_guy_call.play()
            s.phone_guy_played = True
        

#NIGHT ENDED
class NightEnded:
    def __init__(s, game):
        # TURNING GAME INTO ATTRIBUTE
        s.game = game

        # NIGHT ENDED ATTRIBUTES
        s.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.image.fill((0, 0, 0))

        # TEXT FONT
        s.night_info_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 40)
        s.night_info = s.night_info_font.render('6 AM', False, (255, 255, 255))
        s.night_info_rect = s.night_info.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # TRANSPARENCY LEVEL - BEGINNING WITH FULL TRANSPARENCY (INVISIBLE)
        s.transparency_level = 0
        s.fading_in = True  #STARTING WITH FADE IN
        s.start_time = None  #WILL BE SET WHEN 6 AM IS REACHED

    def update(s):
        """Handles the fade-in effect and transitions to the menu."""
        if s.start_time is None:
            s.start_time = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - s.start_time

        if s.fading_in:
            #FADE IN OVER 3 SECONDS (3000 MC)
            s.transparency_level = min(255, (elapsed_time / 3000) * 255)
            if s.transparency_level == 255:
                s.fading_in = False  #STOP FADING IN
                s.start_time = pygame.time.get_ticks()  #RESET TIMER FOR HOLD DURATION

        elif elapsed_time >= 5000:  # Hold the screen for 5 seconds
            s.game.data['NIGHT_DATA'] += 1  # Increase the night count
            s.game.level = Level(s.game, s.game.data)  # Reset Level for the new night
            s.game.game_state = 'menu'  # Change game state to 'menu'

    def draw(s):
        """Draws the win screen with transparency."""
        s.image.set_alpha(s.transparency_level)
        s.game.display.blit(s.image, (0, 0))
        s.game.display.blit(s.night_info, s.night_info_rect)

#FADE OUT CLASS
class FadeOut:

    #FADE OUT CLASS CONSTRUCTOR
    def __init__(s, game):
        
        #TURNING GAME IN TO ATTRIBUTE
        s.game = game
        
        #GETTING ALL FADE OUT FRAMES IMPOTED FROM DIR
        s.fade_out_frames = [
            pygame.transform.scale(
                pygame.image.load(path.join('..', 'assets', 'fade_out_frames', f'{i}.png')).convert(), (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            for i in range(1, len([file for file in listdir(path.join('..', 'assets', 'fade_out_frames')) if file.endswith('.png')]) + 1)
        ]

        #SETTING AN INITIAL CURRENT FRAME - THE FIRST ONE
        s.current_frame = 0     #KIND OF AN INDEX


    #METHOD FOR UPDATING THE FADE OUT
    def update(s):
        #UPDATE CURRENT FRAME BASED ON ELAPSED TIME
        s.current_frame = (pygame.time.get_ticks() // 150) % len(s.fade_out_frames)

        #CHECKING IF ALL FRAMES ARE PLAYED AND MOVE TO THE NEXT STATE
        if s.current_frame == len(s.fade_out_frames) - 1:
            s.game.game_state = 'menu'
            time.sleep(1)
            s.game.level = Level(s.game, s.game.data)

    #METHOD FOR DRAWING THE FADE OUT
    def draw(s):
        s.game.display.blit(s.fade_out_frames[s.current_frame], (0, 0))

#CLASS FOR FADE IN EFFECT
class FadeIn:

    #FADE IN CONSTRUCTOR
    def __init__(s, game, data):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #TURNING MENU DATA IN TO AN ATTRIBUTE
        s.data = data

        #FADE IN BORDER
        s.fade_in_border = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.fade_in_border.fill((0,0,0))

        #FADE IN INFO TEXT
        s.fade_info_font = pygame.font.Font((path.join('..', 'fonts', 'Pixelated.ttf')), 50)
        s.fade_in_info = s.fade_info_font.render(f"Night {s.game.data['NIGHT_DATA']}\n0 AM", False, (255,255,255))
        s.fade_in_info_rect = s.fade_in_info.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        #TRANSPARENCY LEVEL - BEGINING WITH NOT TRANSPARENT
        s.transparancy_level = 255

        #TIMERS AND TIMER LOGIC
        s.start_time = pygame.time.get_ticks()  #START TIME FOR EFFECT
        s.delay_duration = 2000     #DELAY BEFORE FADING OUT (2 SEC)
        s.fade_in_duration = 3000   #FADE OUT DURATION (3 SEC)
        s.is_fading = False         #BOOLIAN TO CHECK IF FADING SHOULD START
    

    #METHOD FOR UPDATING FADE IN INFO
    def update_fade_info(s):
        s.fade_in_info = s.fade_info_font.render(f"Night {s.game.data['NIGHT_DATA']}\n0 AM", False, (255,255,255))

    # METHOD TO RESET THE FADE-IN EFFECT
    def reset(s):
        s.start_time = pygame.time.get_ticks()  # Reset start time
        s.transparancy_level = 255  # Reset transparency to fully opaque
        s.is_fading = False  # Reset fading status

    #METHOD FOR UPDATING THE FADE IN
    def update(s):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - s.start_time

        # Start fading only after delay
        if elapsed_time >= s.delay_duration:
            s.is_fading = True

        if s.is_fading:
            fade_elapsed_time = elapsed_time - s.delay_duration

            if fade_elapsed_time < s.fade_in_duration:
                s.transparancy_level = 255 - (255 * fade_elapsed_time / s.fade_in_duration)
            else:
                s.transparancy_level = 0  #FULLY TRANSPARENT

        #ENSIRING TRANSPARENCY IS WITHIN VALID RANGES
        s.transparancy_level = max(0, min(255, s.transparancy_level))

        #APPLYING TRANSPARENCY TO BORDER
        s.fade_in_border.set_alpha(s.transparancy_level)

        #RE-RENDERING FADE IN TEXT EACH FRAME WITH NEW TRANSPARENCY
        fade_text_surface = s.fade_info_font.render(f"Night {s.game.data['NIGHT_DATA']}\n0 AM", True, (255,255,255))
        fade_text_surface.set_alpha(s.transparancy_level)
        s.fade_in_info = fade_text_surface


    #METHOD FOR DRAWING THE FADE IN
    def draw(s):

        #DRAWING THE FADE IN BORDER
        s.game.display.blit(s.fade_in_border, (0,0))
        s.game.display.blit(s.fade_in_info, s.fade_in_info_rect)

#BUTTON CLASS
class Button:
    # BUTTON CLASS CONSTRUCTOR
    def __init__(s, game, level):
        # TURNING GAME INTO ATTRIBUTE
        s.game = game

        # TURNING CURRENT VIEW INTO AN ATTRIBUTE
        s.level = level

        # OFFICE BUTTON ATTRIBUTES
        s.image_up = pygame.image.load(path.join('..', 'assets', 'office_assets', 'camera_button_up.png')).convert_alpha()
        s.image_up = pygame.transform.scale(s.image_up, (400, 40))

        # CAMERAS BUTTON ATTRIBUTES
        s.image_down = pygame.image.load(path.join('..', 'assets', 'office_assets', 'camera_button_down.png')).convert_alpha()
        s.image_down = pygame.transform.scale(s.image_down, (400, 40))

        # SETTING INITIAL BUTTON IMAGE AND RECT
        s.image = s.image_up
        s.rect = s.image.get_rect(bottomright=(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 5))

        # COOLDOWN TIMER TO PREVENT RAPID PRESSING
        s.last_press_time = 0
        s.cooldown_time = 0.15  # 150 ms cooldown

        # TRANSPARENCY LOGIC
        s.transparency_normal = 150
        s.transparency_hover = 200

    # METHOD TO UPDATE THE BUTTON
    def update(s):
        s.input()

    # METHOD FOR DRAWING BUTTON
    def draw(s):
        # CHOOSING THE RIGHT BUTTON IMAGE
        s.image = s.image_up if s.level.current_view == 'office' else s.image_down

        # APPLYING TRANSPARENCY BASED ON HOVER STATE
        mouse_pos = pygame.mouse.get_pos()
        if s.rect.collidepoint(mouse_pos):
            s.image.set_alpha(s.transparency_hover)
        else:
            s.image.set_alpha(s.transparency_normal)

        # DRAWING THE BUTTON
        s.game.display.blit(s.image, s.rect)

    # METHOD FOR GETTING USER INPUT
    def input(s):
        # GETTING THE MOUSE POSITION AND CHECKING FOR CLICKS
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # CHECKING COOLDOWN
        current_time = time.time()
        if current_time - s.last_press_time > s.cooldown_time:
            # IF BUTTON CLICKED, SWITCH VIEW
            if mouse_pressed and s.rect.collidepoint(mouse_pos):
                if s.level.current_view == 'office':
                    s.level.camera_view_on_sound.play()
                else:
                    s.level.camera_view_off_sound.play()
                s.level.current_view = 'cameras' if s.level.current_view == 'office' else 'office'
                s.last_press_time = current_time

            # SPACEBAR HANDLING
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if s.level.current_view == 'office':
                    s.level.camera_view_on_sound.play()
                else:
                    s.level.camera_view_off_sound.play()
                s.level.current_view = 'cameras' if s.level.current_view == 'office' else 'office'
                s.last_press_time = current_time