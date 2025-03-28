import csv
from istorage import IStorage

class StorageCsv(IStorage):
    """
    CSV storage implementation for movie data.
    """

    def __init__(self, file_path):
        """
        Initialize with the path to the CSV file.
        """
        self.file_path = file_path

    def _load_movies(self):
        """
        Load movies from the CSV file.
        """
        movies = {}
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movies[row['title']] = {
                    'year': row['year'],
                    'rating': float(row['rating']),
                    'poster': row['poster']
                }
        return movies

    def _save_movies(self, movies):
        """
        Save movies to the CSV file.
        """
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ['title', 'year', 'rating', 'poster']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    'title': title,
                    'year': details['year'],
                    'rating': details['rating'],
                    'poster': details['poster']
                })

    def list_movies(self):
        """
        List all movies.
        """
        movies = self._load_movies()
        print(f"{len(movies)} movies in total:\n")
        for title, details in movies.items():
            print(f"{title} ({details['year']}): {details['rating']}")

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie.
        """
        movies = self._load_movies()
        movies[title] = {'year': year, 'rating': float(rating), 'poster': poster}
        self._save_movies(movies)
        print("Movie added successfully!")

    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        movies = self._load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print("Movie deleted successfully!")
        else:
            print("Movie not found. Please try again with one of the list")

    def update_movie(self, title, rating):
        """
        Update the rating of a movie.
        """
        movies = self._load_movies()
        if title in movies:
            movies[title]['rating'] = float(rating)
            self._save_movies(movies)
            print("Movie rating updated successfully!")
        else:
            print("Movie not found. Please try again with one of the list")