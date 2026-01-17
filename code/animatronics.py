#IMPORTING LIBRARIES
import pygame
from os import path, listdir
from random import randint

#IMPORTING FILES
from settings import *


#ANIMATRONICS CLASS / ANIMATRONICS SUBSYSTEM FOR LEVEL
class Animatronic:

    #ANIMATRONICS CLASS CONSTRUCTOR
    def __init__(s, game, name, start_pos, movement_path):

        #TURNING GAME IN TO ATTRIBUTE
        s.game = game

        #ANIMATRONIC ATTRIBUTES
        s.name = name
        s.position = start_pos
        s.path = movement_path
        s.last_move_time = pygame.time.get_ticks()

        # ADDING ANIMATRONIC JUMPSCARE FRAMES
        s.jumpscare_frames = [
            pygame.transform.scale(
                pygame.image.load(path.join('..', 'assets', 'animatronics', f'{s.name}_jumpscare', f'{i}.png')).convert_alpha(),
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
            for i in range(1, len([file for file in listdir(path.join('..', 'assets', 'animatronics', f'{s.name}_jumpscare')) if file.endswith('.png')]) + 1)
        ]
        

    #METHOD FOR MOVING THE ANIMATIONIC
    def move(s, night, aggression):

        # RANDOMIZING TIME FOR MOVEMENT CHANCE (8-12 SECONDS)
        move_interval = randint(4000, 6000)
        current_time = pygame.time.get_ticks()

        if current_time - s.last_move_time < move_interval:
            return
        
        #UPDATING THE LAST MOVE TIME
        s.last_move_time = current_time

        #CALCULATING MOVEMENT PROBABILITY BASED ON, WHICH NIGHT AND AGGRESSION
        base_chance = aggression + night * (3 + night // 2)
        move_chance = min(base_chance, 100)     #CAPPING CHANCE AT 100%

        if randint(0, 100) < move_chance:
            current_index = s.path.index(s.position)   
            
            #IF NOT AT THE END OF THE PATH
            if current_index + 1 < len(s.path):
                s.position = s.path[current_index + 1]  #MOVE CLOSER TO THE OFFICE
        