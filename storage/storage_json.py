import json
import requests
from storage.istorage import IStorage

class StorageJson(IStorage):
    """
    Combined API and JSON storage implementation for movie data.
    """

    def __init__(self, api_url, api_key, file_path):
        """
        Initialize with the API URL, API key, and path to the JSON file.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.file_path = file_path
        self.movies = self._load_movies()

    def _load_movies(self):
        """
        Load movies from the JSON file.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.file_path}. Starting with an empty movie list.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.file_path}. Starting with an empty movie list.")
            return {}

    def _save_movies(self):
        """
        Save movies to the JSON file.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.movies, file, indent=4)
        except IOError as e:
            print(f"Error saving movies to file: {self.file_path}. {e}")

    def _fetch_movie_details(self, title):
        """
        Fetch movie details from the OMDb API.
        """
        params = {
            't': title,
            'apikey': self.api_key
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            movie_details = response.json()
            if movie_details.get('Response') == 'False':
                print(f"Error: {movie_details.get('Error')}")
                return None
            return movie_details
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to fetch movie details. {e}")
            return None

    def _fetch_movies(self):
        """
        Fetch all movies from the local storage.
        """
        return list(self.movies.values())

    def list_movies(self):
        """
        List all movies.
        """
        try:
            movies = self._fetch_movies()
            if not movies:
                print("No movies available.")
                return []
            print(f"{len(movies)} movies in total:\n")
            for movie in movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
            return movies
        except Exception as e:
            print(f"Error listing movies: {e}")
            return []

    def add_movie(self, title, year=None, rating=None, poster=None, description=None):
        if title.lower() in (movie.lower() for movie in self.movies):
            raise Exception("Movie already exists.")
        if not year or not rating or not poster or not description:
            movie_details = self._fetch_movie_details(title)
            if movie_details:
                movie = {
                    "title": movie_details['Title'],
                    "year": movie_details['Year'],
                    "rating": movie_details['imdbRating'],
                    "poster": movie_details['Poster'],
                    "imdb_id": movie_details['imdbID'],
                    "description": movie_details.get('Plot', 'No description available')
                }
            else:
                raise Exception("Error: Movie not found.")
        else:
            movie = {
                'title': title,
                'year': year,
                'rating': float(rating),
                'poster': poster,
                'description': description
            }
        self.movies[title] = movie
        self._save_movies()
        print("Movie added successfully!")

    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        title_lower = title.lower()
        movies_lower = {k.lower(): k for k in self.movies.keys()}
        if title_lower in movies_lower:
            del self.movies[movies_lower[title_lower]]
            self._save_movies()
            print("Movie deleted successfully!")
        else:
            raise Exception("Error: Movie not found.")

    def update_movie(self, title, rating):
        """
        Update the rating of a movie.
        """
        title_lower = title.lower()
        movies_lower = {k.lower(): k for k in self.movies.keys()}
        if title_lower in movies_lower:
            self.movies[movies_lower[title_lower]]['rating'] = float(rating)
            self._save_movies()
            print("Movie rating updated successfully!")
        else:
            raise Exception("Error: Movie not found.")