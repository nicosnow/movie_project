import random
import statistics
import os

class MovieApp:
    """
    Movie application to manage movie data.
    """

    def __init__(self, storage_api, storage_json):
        """
        Initialize with storage API and JSON storage objects.
        """
        self._storage_api = storage_api
        self._storage_json = storage_json

    def _command_list_movies(self):
        """
        Command to list all movies.
        """
        try:
            self._storage_json.list_movies()
        except Exception as e:
            print(f"An error occurred while listing movies: {e}")
        input("Press Enter to continue...")

    def _command_movie_stats(self):
        """
        Command to display movie statistics.
        """
        try:
            movies = self._storage_json.movies
            if not movies:
                print("No movies available.")
            else:
                ratings = [float(movie['rating']) for movie in movies.values()]
                avg_rating = sum(ratings) / len(ratings) if ratings else 0
                median_rating = statistics.median(ratings)
                best_movie = max(movies.items(), key=lambda x: float(x[1]['rating']))
                worst_movie = min(movies.items(), key=lambda x: float(x[1]['rating']))
                print(f"Average rating: {avg_rating:.2f}")
                print(f"Median rating: {median_rating:.2f}")
                print(f"Best movie rating: {best_movie[0]} with rating {best_movie[1]['rating']}")
                print(f"Worst movie rating: {worst_movie[0]} with rating {worst_movie[1]['rating']}")
        except Exception as e:
            print(f"An error occurred while calculating movie statistics: {e}")
        input("Press Enter to continue...")

    def _command_random_movie(self):
        """
        Command to display a random movie and its rating.
        """
        try:
            movies = self._storage_json.movies
            if not movies:
                print("No movies available.")
            else:
                title, details = random.choice(list(movies.items()))
                print(f"Random movie: {title} with rating {details['rating']}")
        except Exception as e:
            print(f"An error occurred while selecting a random movie: {e}")
        input("Press Enter to continue...")

    def _command_search_movie(self):
        """
        Command to search for movies by part of the title.
        """
        try:
            query = input("Enter part of movie name to search: ").lower()
            matched_movies = [
                f"{title}, {details['rating']}"
                for title, details in self._storage_json.movies.items()
                if query in title.lower()
            ]
            if matched_movies:
                print("\n".join(matched_movies))
            else:
                print("No movies matched your query.")
        except Exception as e:
            print(f"An error occurred while searching for movies: {e}")
        input("Press Enter to continue...")

    def _command_movies_sorted_by_rating(self):
        """
        Command to display movies sorted by rating.
        """
        try:
            movies = self._storage_json.movies
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
            for title, details in sorted_movies:
                print(f"{title}: {details['rating']}")
        except Exception as e:
            print(f"An error occurred while sorting movies by rating: {e}")
        input("Press Enter to continue...")

    def _generate_website_file(self):
        """
        Generate the website file (index.html) with the movie data.
        """
        try:
            movies = self._storage_json.movies
            template_path = os.path.join('_static', 'index_template.html')
            if not os.path.exists(template_path):
                print(f"Template file not found: {template_path}")
                return

            with open(template_path, 'r') as file:
                template = file.read()

            movie_items = "\n".join(
                f"""
                <li style="list-style-type: none; margin-bottom: 20px;">
                    <h2 style="text-align: center;">{title}</h2>
                    <div style="display: flex; align-items: center;">
                        <a href="https://www.imdb.com/title/{details['imdb_id']}" target="_blank">
                            <img src="{details['poster']}" alt="{title} poster" style="width: 150px; height: auto; margin-right: 20px;">
                        </a>                        <div>
                            <p><strong>Description:</strong> {details['description']}</p>
                            <p><strong>Year:</strong> {details['year']}</p>
                            <p><strong>Rating:</strong> {details['rating']}</p>
                        </div>
                    </div>
                </li>
                """
                for title, details in movies.items()
            )

            html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movie_items)

            with open('index.html', 'w') as file:
                file.write(html_content)
            print("Website was generated successfully.")
        except Exception as e:
            print(f"An error occurred while generating the website: {e}")
        input("Press Enter to continue...")

    def _generate_website(self):
        """
        Generate the movie database menu and handle user input.
        """
        while True:
            print("\nMovie Database Menu")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie")
            print("5. Stats")
            print("6. Random Movie")
            print("7. Search Movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")
            choice = input("\nEnter choice(0-9): ")

            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                self._command_list_movies()
            elif choice == '2':
                try:
                    title = input("Enter movie title: ")
                    movie_details = self._storage_api._fetch_movie_details(title)
                    if movie_details:
                        self._storage_json.add_movie(
                            title=movie_details['Title'],
                            year=movie_details['Year'],
                            rating=movie_details['imdbRating'],
                            poster=movie_details['Poster']
                        )
                    else:
                        print("Error: Movie not found.")
                except Exception as e:
                    print(f"An error occurred while adding the movie: {e}")
                input("Press Enter to continue...")
            elif choice == '3':
                try:
                    title = input("Enter movie title to delete: ")
                    self._storage_json.delete_movie(title)
                except Exception as e:
                    print(f"An error occurred while deleting the movie: {e}")
                input("Press Enter to continue...")
            elif choice == '4':
                try:
                    title = input("Enter movie title to update: ")
                    rating = input("Enter new movie rating: ")
                    self._storage_json.update_movie(title, rating)
                except Exception as e:
                    print(f"An error occurred while updating the movie: {e}")
                input("Press Enter to continue...")
            elif choice == '5':
                self._command_movie_stats()
            elif choice == '6':
                self._command_random_movie()
            elif choice == '7':
                self._command_search_movie()
            elif choice == '8':
                self._command_movies_sorted_by_rating()
            elif choice == '9':
                self._generate_website_file()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def run(self):
        """
        Run the movie application.
        """
        self._generate_website()