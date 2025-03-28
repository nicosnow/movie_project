from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Abstract base class for storage operations.
    """

    @abstractmethod
    def list_movies(self):
        """
        List all movies.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Delete a movie by title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Update the rating of a movie.
        """
        pass