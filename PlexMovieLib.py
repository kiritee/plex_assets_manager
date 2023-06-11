import sys
from plexapi.server import PlexServer 
from Movie import Movie
import os
from shutil import move, Error
from pathlib import Path
from utils import *
import random
import time
from conf import MAX_SLEEP_DURATION


class PlexMovieLib:
    def __init__(self, plex_token, plex_url="http://127.0.0.1:32400", movies_library="Movies", log=False, quiet=False):
        self.plex = PlexServer(plex_url, plex_token)
        self.movies = self.plex.library.section(movies_library)
        self.movies_path = self.movies.location[0]
        self.quiet=quiet
        if log:
            self.log_file = open("log.txt",'w+',encoding="utf-8")
        else:
            self.log_file = sys.stdout

    
    def printText(self,text):
        if not self.quiet:
            print(text,file=self.log_file)

    def reorganize_folders(self):
        for movie in self.movies.all():
            m=Movie(movie)    

            title_validchars = m.getTitleValidChars()
            correct_folder_name = f"{title_validchars} ({m.year})"
            correct_folder_path = self.movies_path  + "/" + correct_folder_name
            self.printText(f"\n\n{correct_folder_name}\nOld location :\n{m.folder_path}\nNew location :\n{correct_folder_path}")
            
            if m.folder_path == correct_folder_path:
                self.printText("Already exists in correct folder. Exiting")
        
            elif m.folder_path == self.movies_path:
                self.printText("files are in base location. moving following files") 
                os.makedirs(correct_folder_path,exist_ok=True)
                for file in os.scandir(m.folder_path):
                    filePath = Path(file.path)
                    filename = (filePath).stem                  
                    if file.is_file():
                        if filename.find(m.filename) == 0:
                            self.printText(f"Object filename is: {file.path}")
                            try:
                                move(file.path,correct_folder_path)
                                self.printText("Folder moved")
                            except Error:
                                pass
            else:
                try:
                    move(m.folder_path,correct_folder_path)
                    self.printText("Folder moved")
                except FileNotFoundError:
                    pass
        
    def rename_movie_files(self):
        for movie in self.movies.all():
            m=Movie(movie)    
            correct_movie_filename = m.get_correct_filename()
            self.printText(f"\n\nMovie : {correct_movie_filename}\nCurrent Name : {m.filename}")
            
            for file in os.scandir(m.folder_path):
                filePath = Path(file.path)
                filename = filePath.stem  
                if file.is_file():
                    if filename.find(m.filename) == 0:
                        correct_filename = filename.replace(m.filename,correct_movie_filename)
                        correct_filepath = m.folder_path + "/" + correct_filename + filePath.suffix
                        self.printText(f"\nObject's filename is: {file.path}\nCorrected filepath is: {correct_filepath}")
                        try:
                            os.rename(file.path,correct_filepath)
                        except PermissionError:
                            self.printText('chflags nouchg "{}"'.format(file.path))
                            os.system('chflags nouchg "{}"'.format(file.path))
                            os.rename(file.path,correct_filepath)
                        self.printText("Rename completed")

    def download_trailers(self):
        for movie in self.movies.all():
            m=Movie(movie) 

            if m.is_trailer_present():
                self.printText(f"Trailer already exists")

            else:
                self.printText(f"\n\n{m.title} ({m.year}): ")
                filename = m.get_correct_filename()

                # try searching <title> on youtube for trailers, and download
                search_title = f"{m.title} ({m.year})"
                download_movie_trailers(search_title, filename, m.folder_path)
                if m.is_trailer_present():
                    self.printText(f"Trailer found for {m.title}")
                else:
                    # if <title> doesnt work, try <original title>
                    self.printText(f"Trailer not found for {m.title}")
                    if self.originalTitle != None and self.originalTitle.strip() != '':
                        search_title = f"{m.originalTitle} ({m.year})"
                        download_movie_trailers(search_title, filename, m.folder_path) 
                        if m.is_trailer_present():
                            self.printText(f"Trailer found for {m.originalTitle}")
                        else:
                            self.printText(f"Trailer not found for {m.originalTitle}")
                
                # sleep for a random duration. this is so that youtube doesnt get bombarded with requests
                # Youtube could introduce captcha if this is not done
                time.sleep(random.randint(1,MAX_SLEEP_DURATION))



