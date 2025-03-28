import json
from istorage import IStorage

class StorageJson(IStorage):
    """
    JSON storage implementation for movie data.
    """

    def __init__(self, file_path):
        """
        Initialize with the path to the JSON file.
        """
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
            return {}

    def _save_movies(self):
        """
        Save movies to the JSON file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.movies, file, indent=4)

    def list_movies(self):
        """
        List all movies.
        """
        print(f"{len(self.movies)} movies in total:\n")
        for title, details in self.movies.items():
            print(f"{title} ({details['year']}): {details['rating']}")

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie.
        """
        self.movies[title] = {'year': year, 'rating': float(rating), 'poster': poster}
        self._save_movies()
        print("Movie added successfully!")

    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        if title in self.movies:
            del self.movies[title]
            self._save_movies()
            print("Movie deleted successfully!")
        else:
            print("Movie not found. Please try again with one of the list")

    def update_movie(self, title, rating):
        """
        Update the rating of a movie.
        """
        if title in self.movies:
            self.movies[title]['rating'] = float(rating)
            self._save_movies()
            print("Movie rating updated successfully!")
        else:
            print("Movie not found. Please try again with one of the list")