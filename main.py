from movie_app import MovieApp
from storage.storage_json import StorageJson
from dotenv import load_dotenv
import os


def main():
    """
    Main function to run the MovieApp.
    """
    try:
        load_dotenv()  # Load environment variables from .env file
        api_url = 'https://www.omdbapi.com/'  # API URL
        api_key = os.getenv('API_KEY')  # Get the API key from environment variables
        if not api_key:
            raise ValueError("API_KEY not found in environment variables.")

        file_path = 'data/movies.json'  # Path to the JSON file
        storage_api_json = StorageJson(api_url, api_key, file_path)  # Combined storage class
        movie_app = MovieApp(storage_api_json, storage_api_json)  # Use the same instance for both parameters
        movie_app.run()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()