
"""
Created on Wed May  6 00:16:32 2020

@author: konark
"""

from conf import *
from utils import Movie
import os
import sys
import re
from shutil import move, Error
from pathlib import Path
from plexapi.server import PlexServer 

if LOG:
    log_file = open(codebase+"/log.txt",'w+',encoding="utf-8")
else:
    log_file = sys.stdout


plex = PlexServer(PLEX_URL, TOKEN)
movies = plex.library.section(MOVIES_LIBRARY)
movies_path = movies.location[0]

for movie in movies.all():
    m=Movie(movie)    

    title_validchars = m.getTitleValidChars()
    correct_folder_name = f"{title_validchars} ({m.year})"
    correct_folder_path = movies_path  + "/" + correct_folder_name
    print(f"\n\n{correct_folder_name}\nOld location :\n{m.folder_path}\nNew location :\n{correct_folder_path}", file=log_file)
    
    if m.folder_path == correct_folder_path:
        print("Already exists in correct folder. Exiting", file=log_file)
  
    elif m.folder_path == movies_path:
        print("files are in base location. moving following files", file=log_file) 
        os.makedirs(correct_folder_path,exist_ok=True)
        for file in os.scandir(m.folder_path):
            filePath = Path(file.path)
            filename = (filePath).stem                  
            if file.is_file():
                if filename.find(m.filename) == 0:
                    print(f"Object filename is: {file.path}", file=log_file)
                    try:
                        move(file.path,correct_folder_path)
                        print("Folder moved", file=log_file)
                    except Error:
                        pass
    else:
        try:
            move(m.folder_path,correct_folder_path)
            print("Folder moved", file=log_file)
        except FileNotFoundError:
            pass
        

    


    
