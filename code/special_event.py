#IMPORTING LIBRARIES
import pygame

#IMPORTING FILES
from settings import *


#MENU CLASS
class SpecialEvent:

    #MENU CONSTRUCTOR
    def __init__(s, game):  #PASSING IN THE GAME

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #SPECIAL EVENT ATTRIBUTES
        s.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.background.fill('red')


    #METHOD FOR RUNNING THE SPECIAL EVENT
    def run(s):

        s.game.display.blit(s.background, (0,0))