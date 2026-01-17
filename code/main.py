#IMPORTING LIBRARIES
import pygame
from sys import exit
from os import path
from random import choices

#IMPORTING FILES
from settings import *
from menu import Menu
from special_event import SpecialEvent
from loading_data import save_data, load_data
from level import Level
from options import Options
from extras import Extras


#GAME CLASS
class Game:

    #GAME INFO
    def __str__(self):
        return '''
        Fan-game made by Dariusz J. Mironczuk.
        Feel free to use, edit, publish or do whatever you want with my code.
        Hope everything is readable. If you would like to hire me, I left my emial below.
        d.mironczuk@ekonom.jgora.pl
        '''
    
    #GAME CONSTRUCTOR
    def __init__(s):

        #INITIALIZING PYGAME WHEN GAME STARTS
        pygame.init()

        #LOADING IN GAME DATA
        s.data = load_data(DATA_PATH, DATA)
        s.aggression_data = load_data(AGGRESSION_DATA_PATH, AGGRESSION_DATA)

        #INITIALIZING WINDOW
        s.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Five nights at python!')

        #LOADING AND SETTING THE ICON
        icon = pygame.image.load(path.join('..', 'assets', 'icon.png'))
        pygame.display.set_icon(icon)

        #INITIALIZNG CLOCK
        s.clock = pygame.time.Clock()

        #INITIALIZING GAME ELEMENTS
        s.menu = Menu(s, s.data)
        s.level = Level(s, s.data)
        s.special_event = SpecialEvent(s)
        s.options = Options(s, s.aggression_data)
        s.extras = Extras(s)

        #GAME STATE     MENU - 100% , SPECIAL EVENT - 0%
        s.game_state = choices(['menu', 'special_event'],
                               weights=[100, 0],     #CHANGE SPECIAL EVENT CHANCE HERE
                               k=1)[0]


    #METHOD FOR RUNNING THE GAME
    def run(s):

        #GAME LOOP
        while True:

            #CLOCK UPDATE
            s.clock.tick(FPS)

            #GAME STATE HANDLER
            if s.game_state == 'menu':
                s.menu.run()
            elif s.game_state == 'special_event':
                s.special_event.run()
            elif s.game_state == 'new_game':
                s.data['NIGHT_DATA'] = 1
                s.level.data['NIGHT_DATA'] = 1
                s.level.fade_in_border.update_fade_info()
                s.level.run()
            elif s.game_state == 'continue_game':
                s.level.run()
            elif s.game_state == 'options':
                s.options.run()
            elif s.game_state == 'extras':
                s.extras.run()
            elif s.game_state == 'exit':
                save_data(s.data, DATA_PATH)
                save_data(s.aggression_data, AGGRESSION_DATA_PATH)
                pygame.quit()
                exit()

            #EVENT HANDLER
            for event in pygame.event.get():

                #CLOSING THE GAME WITH WINDOW BUTTON
                if event.type == pygame.QUIT:
                    save_data(s.data, DATA_PATH)
                    save_data(s.aggression_data, AGGRESSION_DATA_PATH)
                    pygame.quit()
                    exit()

                #CLOSING THE GAME WITH ESCAPE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        save_data(s.data, DATA_PATH)
                        save_data(s.aggression_data, AGGRESSION_DATA_PATH)
                        pygame.quit()
                        exit()
        

            #UPDATING GAME DATA WITH COMPLETION
            if s.data['NIGHT_DATA'] == 5:
                s.data['COMPLETION_STATE'] = True
            if s.data['NIGHT_DATA'] > s.data['NIGHT_ADVANCED_TO']: 
                s.data['NIGHT_ADVANCED_TO'] = s.data['NIGHT_DATA']

            #DISPLAY UPDATE
            pygame.display.update()


#CREATING AN INSTANCE NAD RUNNING THE GAME
if __name__ == '__main__':
    game = Game()
    print(game)
    game.run()

#SHUTTING DOWN THE GAME
pygame.quit()
exit()