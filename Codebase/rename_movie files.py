from conf import *
from utils import *
import os
import sys
import re
from shutil import move
from pathlib import Path
from plexapi.server import PlexServer 


if LOG:
    log_file = open(codebase+"/log.txt",'w',encoding="utf-8")
else:
    log_file = sys.stdout


plex = PlexServer(PLEX_URL, TOKEN)
movies = plex.library.section(MOVIES_LIBRARY)
movies_path = movies.location[0]

for movie in movies.all():
    m=Movie(movie)    
    correct_movie_filename = m.get_correct_filename()
    print(f"\n\nMovie : {correct_movie_filename}\nCurrent Name : {m.filename}", file=log_file)
    
    for file in os.scandir(m.folder_path):
        filePath = Path(file.path)
        filename = filePath.stem  
        if file.is_file():
            if filename.find(m.filename) == 0:
                correct_filename = filename.replace(m.filename,correct_movie_filename)
                correct_filepath = m.folder_path + "/" + correct_filename + filePath.suffix
                print(f"\nObject's filename is: {file.path}\nCorrected filepath is: {correct_filepath}", file=log_file)
                try:
                    os.rename(file.path,correct_filepath)
                except PermissionError:
                    print('chflags nouchg "{}"'.format(file.path))
                    os.system('chflags nouchg "{}"'.format(file.path))
                    os.rename(file.path,correct_filepath)
                print("Rename completed", file=log_file)
                
  