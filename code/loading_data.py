#IMPORTING LIBRARIES
import json
from os import path, makedirs

#IMPORTING FILES
from settings import *



#FUNCTION FOR LOADING THE GAME DATA
def load_data(data_path, default_data):

    #CHECKING IF GAME FILE EXISTS
    if path.exists(data_path):
        with open(data_path, 'r') as file:
            try:
                
                #TRYING TO LOAD IN THE DATA
                return json.load(file)
            except json.JSONDecodeError:
                print("Save file is corrupted. Creating a new one with default data.")
    

    #IF THE FILE DOESN'T EXIST OR IS CORRUPTED, CREATE IT WITH DEFAULT DATA FROM SETTINGS
    save_data(default_data, data_path)
    return default_data



#FUNCTION FOR SAVING THE GAME DATA
def save_data(data, save_path):

    #ENSURING THE DIRECTORY EXISTS BEFORE WRITING
    makedirs(path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as file:
        json.dump(data, file, indent=4)