import unittest
import json
import os
from storage.storage_json import StorageJson
from dotenv import load_dotenv

class TestStorageJson(unittest.TestCase):
    def setUp(self):
        load_dotenv()  # Load environment variables from .env file
        self.test_file = 'test_data.json'
        self.storage = StorageJson(api_url='http://www.omdbapi.com/', api_key=os.getenv('API_KEY'), file_path=self.test_file)
        self.data = {
            "title": "Inception",
            "year": "2010",
            "rating": "8.8",
            "poster": "N/A",
            "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
        }
        self.storage.add_movie(**self.data)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_fetch_movie_details(self):
        movie_details = self.storage._fetch_movie_details(self.data['title'])
        self.assertIsNotNone(movie_details)
        self.assertEqual(movie_details['Title'], self.data['title'])

    def test_add_movie(self):
        with open(self.test_file, 'r') as file:
            loaded_data = json.load(file)
        self.assertIn(self.data['title'], loaded_data)
        self.assertEqual(loaded_data[self.data['title']]['title'], self.data['title'])
        self.assertEqual(loaded_data[self.data['title']]['year'], self.data['year'])
        self.assertEqual(loaded_data[self.data['title']]['rating'], float(self.data['rating']))
        self.assertEqual(loaded_data[self.data['title']]['poster'], self.data['poster'])
        self.assertEqual(loaded_data[self.data['title']]['description'], self.data['description'])

    def test_delete_movie(self):
        self.storage.delete_movie(self.data['title'])
        with open(self.test_file, 'r') as file:
            loaded_data = json.load(file)
        self.assertNotIn(self.data['title'], loaded_data)

    def test_update_movie(self):
        new_rating = "9.0"
        self.storage.update_movie(self.data['title'], new_rating)
        with open(self.test_file, 'r') as file:
            loaded_data = json.load(file)
        self.assertEqual(loaded_data[self.data['title']]['rating'], float(new_rating))

    def test_list_movies(self):
        movies = self.storage.list_movies()
        self.assertIn(self.data['title'], [movie['title'] for movie in movies])

    def test_add_existing_movie(self):
        with self.assertRaises(Exception):
            self.storage.add_movie(**self.data)

    def test_delete_nonexistent_movie(self):
        with self.assertRaises(Exception):
            self.storage.delete_movie("Nonexistent Movie")

    def test_update_nonexistent_movie(self):
        with self.assertRaises(Exception):
            self.storage.update_movie("Nonexistent Movie", "9.0")

if __name__ == '__main__':
    unittest.main()