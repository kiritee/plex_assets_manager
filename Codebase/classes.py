from pathlib import Path
import re
import os

class Movie:
    def __init__(self,movie):
        self.title = movie.title
        self.year = movie.year
        self.originalTitle = movie.originalTitle
        path = Path(movie.locations[0])
        self.folder_path = str(path.parent)
        self.filename=str(path.stem)
    
    def getTitleValidChars(self):
        return re.sub('[/?%*|"<>:]+', "-", self.title)

    def getOriginalTitleValidChars(self):
        if self.originalTitle == None or self.originalTitle.strip() == '':
            return ''
        else:
            return " (" + re.sub('[/?%*|"<>:]+', "-", self.originalTitle) + ")"
        
    def is_trailer_present(self):
        for file in os.listdir(self.folder_path):
            file_name, file_ext = os.path.splitext(file)
            if file_name.endswith("-trailer"):
                return True
        return False

    def get_correct_filename(self):
        title_validchars=self.getTitleValidChars()
        year=self.year
        originalTitle_validchars=self.getOriginalTitleValidChars()
        return f"{title_validchars} ({year}){originalTitle_validchars}"
    
