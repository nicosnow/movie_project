import requests
from istorage import IStorage

class StorageApi(IStorage):
    """
    API storage implementation for movie data.
    """

    def __init__(self, api_url, api_key):
        """
        Initialize with the API URL and API key.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.movies = {}  # Local storage for movies

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
            #print(f"Fetched movie details: {movie_details}")  # Print the fetched movie details
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
        movies = self._fetch_movies()
        print(f"{len(movies)} movies in total:\n")
        for movie in movies:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def add_movie(self, title):
        """
        Add a new movie by fetching details from the OMDb API.
        """
        if title in self.movies:
            print("Movie already exists.")
            return
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
            self.movies[title] = movie
            print("Movie added successfully!")
        else:
            print("Error: Movie not found.")

    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        title_lower = title.lower()
        movies_lower = {k.lower(): k for k in self.movies.keys()}
        if title_lower in movies_lower:
            del self.movies[movies_lower[title_lower]]
            print("Movie deleted successfully!")
        else:
            print("Error: Movie not found.")

    def update_movie(self, title, rating):
        """
        Update the rating of a movie.
        """
        title_lower = title.lower()
        movies_lower = {k.lower(): k for k in self.movies.keys()}
        if title_lower in movies_lower:
            self.movies[movies_lower[title_lower]]['rating'] = rating
            print("Movie rating updated successfully!")
        else:
            print("Error: Movie not found.")