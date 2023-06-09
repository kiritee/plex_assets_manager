from imdb import Cinemagoer, IMDbError
import youtube_dl
import os
import re
from plexapi.server import PlexServer

# Create an instance of the IMDb class
ia = Cinemagoer()

def rename_movie_file(movie, movie_folder):
    # Extract movie title and year from the movie object
    movie_title = movie.title
    movie_year = movie.year

    # Extract original title from the movie's original title attribute
    original_title = movie.get('original title')

    # Remove invalid characters from the original title
    original_title = re.sub(r'[\\/:"*?<>|]+', '', original_title)

    # Get the extension of the movie file
    file_extension = os.path.splitext(movie.locations[0])[1]

    # Construct the new file name based on the specified format
    new_file_name = f"{movie_title} ({movie_year}) - ({original_title}).{file_extension}"

    # Rename the movie file
    old_file_path = movie.locations[0]
    new_file_path = os.path.join(movie_folder, new_file_name)
    os.rename(old_file_path, new_file_path)

    print(f"Renamed movie file: {old_file_path} -> {new_file_path}")

def rename_trailer_file(movie, trailer_file):
    # Extract movie title and year from the movie object
    movie_title = movie.title
    movie_year = movie.year

    # Extract original title from the movie's original title attribute
    original_title = movie.get('original title')

    # Remove invalid characters from the original title
    original_title = " (" + re.sub('[\\/?%*|"<>:]+', "-", original_title) + ")"

    # Get the extension of the trailer file
    file_extension = os.path.splitext(trailer_file)[1]

    # Construct the new file name based on the specified format
    new_file_name = f"{movie_title} ({movie_year}){original_title} -trailer.{file_extension}"

    # Rename the trailer file
    old_file_path = os.path.join(movie.locations[0], trailer_file)
    new_file_path = os.path.join(movie.locations[0], new_file_name)
    os.rename(old_file_path, new_file_path)

    print(f"Renamed trailer file: {old_file_path} -> {new_file_path}")

def download_trailer(imdb_id, movie_folder, movie_name):
    try:
        # Retrieve movie information by IMDb ID
        movie = ia.get_movie(imdb_id)
        print("Movie retrieved...")

        # Get the list of trailers for the movie
        trailers = movie.get('trailers')
        print("Trailers found...")

        # Filter the trailers to find the one with the highest quality
        best_trailer = None
        if trailers is not None:
            for trailer in trailers:
                if trailer.get('type') == 'Trailer' and trailer.get('format') == 'Video':
                    if not best_trailer or trailer.get('quality') == 'High':
                        best_trailer = trailer
            print("best trailer found...")
        else: print("No trailers found")
        # Download and rename the trailer if found
        if best_trailer:
            trailer_url = best_trailer.get('url')
            print("Attempting download: "+ trailer_url)
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(movie_folder, f'{movie_name} -trailer.%(ext)s'),
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([trailer_url])

            # Rename the downloaded trailer file
            trailer_file = ydl.prepare_filename(best_trailer)
            rename_trailer_file(movie, os.path.basename(trailer_file))

            print(f"Trailer downloaded successfully for IMDb ID: {imdb_id}")
        

    except IMDbError as e:
        print("IMDb Error:", e)

def find_imdb_id(guids):
    for guid in guids:
        print(guid.id)
        if guid.id.startswith('imdb://'):
            print('imdb id found')
            return guid.id.split('/')[-1][2:]
    return None



def rename_movies_and_download_trailers(plex_url, plex_token):
    # Connect to your Plex server
    plex = PlexServer(plex_url, plex_token)

    # Iterate over each movie in your library
    for movie in plex.library.section('Movies').all():
        # Get the IMDb ID and movie folder path for the movie
        imdb_id = find_imdb_id(movie.guids)
        print('imdb id :'+imdb_id)
        movie_folder = os.path.dirname(movie.locations[0]) if movie.locations else None

        print("\n\n"+movie.title)
        print(imdb_id)

        if imdb_id and movie_folder:
            movie_name = movie.title

            # Rename the movie file
 #           rename_movie_file(movie, movie_folder)

            # Download and rename the trailer
            print("Downloading trailer...")
            download_trailer(imdb_id, movie_folder, movie_name)

# Example usage
plex_url = "http://127.0.0.1:32400"  # URL of your Plex server
plex_token = '1oZHkXsyW9X-vSHtXDsu' # Your Plex token

print("Starting...")

rename_movies_and_download_trailers(plex_url, plex_token)
