# IMPORTING LIBRARIES
import pygame
from random import randint, choice

#IMPORTING FILES
from settings import *


#LIGHTING EFFECT FOR OFFICE
def create_glow_surface(radius, color):

    #CREATING THE LIGHT / GLOW FROM A CIRCLE
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    center = (radius, radius)

    for r in range(radius, 0, -1):
        #ADJUST ALPHA TO FADE SMOOTHLY TO 0 NEAR THE EDGES
        alpha = max(0, int(255 * ((r / radius)**2.5)))  #MAKING THE EFECT SLOWLY FALLOFF
        pygame.draw.circle(surface, (*color[:3], alpha), center, r)
    return surface


#CREATING STATIC NOISE EFFECT
def add_static(image, intensity = 50):
    static_surface = image.copy()

    for _ in range(intensity):      #NUMBER OF NOISE POINTS
        x = randint(0, WINDOW_WIDTH - 1)
        y = randint(0, WINDOW_HEIGHT - 1)

        colour = choice([(255, 255, 255), (0, 0, 0)])  # WHITE OR BLACK
        static_surface.set_at((x, y), colour)
    return static_surface


## FUNCTION FOR FLICKERING BRIGHTNESS
def flicker_brightness(image, intensity=50):
    #CLAMP INTENSITY TO THE RANGE [0, 255]
    intensity = max(0, min(255, intensity))
    
    #CREATE COPY OF THE IMAGE
    flicker_surface = image.copy()
    
    #APPLY BRIGHTNESS FLICKER USING BLEND_RGB_ADD
    flicker_surface.fill((intensity, intensity, intensity), special_flags=pygame.BLEND_RGB_ADD)
    
    return flicker_surface


#FUNCTION TO ADD GLITCH LINES
def add_glitch_lines(image):
    glitch_surfce = image.copy()
    for _ in range(randint(1, 8)):      #RANDOM NUMBER OF LINES
        x_start = randint(0, WINDOW_WIDTH)
        y = randint(0, WINDOW_HEIGHT)
        width = randint(10, 300)
        pygame.draw.rect(glitch_surfce, (randint(50, 255), 0, 0), (x_start, y, width, 2))
    return glitch_surfce


#LAMP CLASS / FOR ATMOSPHERE
class Lamp:

    #LAMP CLASS CONSTRUCTOR
    def __init__(s, game, pos, radius, flicker_intensity = 1.0, colour = (255, 200, 150)):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #LAMP ATTRIBUTES
        s.lamp_glow = create_glow_surface(radius, colour)  #KIND OF A WARM ORANGE GLOW FOR BASE - (255,200,150)
        s.lamp_glow_start_pos = pos  #POSITIONING THE OF THE LIGHT
        s.lamp_glow_alpha = 50  #INITIAL ALPHA FOR FLICKERING
        s.flicker_intensity = flicker_intensity  #FLICKER INTENCITY MULTIPLAYER



    #METHOD FOR UPDATING AND MAKING A FLICKERING EFFECT
    def update(s):

        #SMALL CHANGES FOR SMOOTH FLICKERING
        flicker_change = randint(-100, 100)  * s.flicker_intensity

        #BASE APPHA VALUE WITH SLIGHT RANDOMNESS
        target_alpha = 100 + flicker_change

        #SMOOTH INTERPOLATION
        s.lamp_glow_alpha += (target_alpha - s.lamp_glow_alpha) * 0.15

        #CLAMP TO VALID RANGE
        s.lamp_glow_alpha = max(50, min(200, int(s.lamp_glow_alpha)))

    
    #METHOD FOR DRAWING THE 
    def draw(s, offset=0):

        #CALCULATING THE LAMPS GLOW POSITION RELATIVE TO THE SCREEN
        lamp_glow_pos = (s.lamp_glow_start_pos[0] + offset, s.lamp_glow_start_pos[1])
        lamp_glow = s.lamp_glow.copy()

        #GIVING THE GLOW CIRCLE A SORT OF TRANSPARENCY
        lamp_glow.set_alpha(s.lamp_glow_alpha)

        #DRAWING IT ON TO THE DISPLAY
        s.game.display.blit(lamp_glow, lamp_glow_pos)

    # METHOD TO DRAW LAMP GLOW ON A SPECIFIC SURFACE
    def draw_on_surface(s, surface, offset=0):

        #CALCULATING THE LAMPS GLOW POSITION RELATIVE TO THE SCREEN
        lamp_glow_pos = (s.lamp_glow_start_pos[0] + offset, s.lamp_glow_start_pos[1])
        lamp_glow = s.lamp_glow.copy()

        #GIVING THE GLOW CIRCLE A SORT OF TRANSPARENCY
        lamp_glow.set_alpha(s.lamp_glow_alpha)

        #DRAWING IT ONTO THE GIVEN SURFACE
        surface.blit(lamp_glow, lamp_glow_pos)