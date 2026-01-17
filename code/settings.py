#IMPORTING LIBRARIES
from os import path

#WINDOW SETTINGS
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

#FPS / CLOCK SETTINGS
FPS = 60

#DEFAULT GAME DATA FILE
DATA_PATH = path.join('..', 'data', 'data.json')
DATA = {'NIGHT_DATA' : 1,
        'COMPLETION_STATE' : False,
        'NIGHT_ADVANCED_TO' : 1
}

#DEFAULT ANIMATRONIC AGGRESSION DATA FILE
AGGRESSION_DATA_PATH = path.join('..', 'data', 'aggression.json')
AGGRESSION_DATA = {
    'Chicka' : 1,
    'Freddy' : 1,
    'Bonnie' : 20,
    'Foxy' : 1
}
