
"""
Created on Wed May  6 00:16:32 2020

@author: konark
"""
test = 0
test_case = 6
log = 1

from conf import *
import os
import sys
import re
from shutil import move, Error
from pathlib import Path
from plexapi.server import PlexServer 

if test == 1:
    movies_path = codebase + "/Test_" + str(test_case)
elif test == 0:
    movies_path = plex_movies_path
else:
    print('Test field not set properly')
    raise

if log == 1:
    log_file = open(codebase+"/log.txt",'w+',encoding="utf-8")
else:
    log_file = sys.stdout


plex = PlexServer(plex_url, token)
movies = plex.library.section('Movies')

for video in movies.search():
    title = video.title       
    year = video.year
    location = video.locations[0]
    
    location_path = Path(location.replace(plex_movies_path, movies_path))
    
    current_folder_path = str(location_path.parent)
    
    title_validchars = re.sub('[/?%*|"<>:]+', "-", title)
    correct_folder_name = "{0} ({1})".format(title_validchars,year)
    correct_folder_path = movies_path  + "/" + correct_folder_name
    
    print("\n\n{2}\nOld location :\n{0}\nNew location :\n{1}".format(current_folder_path,correct_folder_path,correct_folder_name), file=log_file)
    
    if current_folder_path == correct_folder_path:
        print("Already exists in correct folder. Exiting", file=log_file)

    
    elif current_folder_path == movies_path:
        print("files are in base location. moving following files", file=log_file)  
  
        os.makedirs(correct_folder_path,exist_ok=True)
        
        movie_filename = location_path.stem
               
        for file in os.scandir(current_folder_path):
            filePath = Path(file.path)
            filename = (filePath).stem                  
            if file.is_file():
                if filename.find(movie_filename) == 0:
                    print("Object filename is: {0}".format(file.path), file=log_file)
                    try:
                        move(file.path,correct_folder_path)
                        print("Folder moved", file=log_file)
                    except Error:
                        pass


    else:
        try:
            move(current_folder_path,correct_folder_path)
            print("Folder moved", file=log_file)
        except FileNotFoundError:
            pass
        

    


    
