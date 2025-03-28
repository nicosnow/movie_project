from movie_app import MovieApp
from storage_api import StorageApi
from storage_json import StorageJson
from dotenv import load_dotenv
import os

def main():
    """
    Main function to run the MovieApp.
    """
    load_dotenv()  # Load environment variables from .env file
    api_url = 'https://www.omdbapi.com/'  # API URL
    api_key = os.getenv('API_KEY')  # Get the API key from environment variables
    storage_api = StorageApi(api_url, api_key)  # Pass the API key to StorageApi
    storage_json = StorageJson('movies.json')  # Path to the JSON file
    movie_app = MovieApp(storage_api, storage_json)
    movie_app.run()

if __name__ == "__main__":
    main()