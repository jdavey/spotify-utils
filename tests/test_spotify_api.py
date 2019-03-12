import unittest
from src.bbc_api import parse_program_id, fetch_playlist_from_program
from src.spotify_api import SpotifyApi


class SpotifyApiTest(unittest.TestCase):
    def test_auth(self):
        spotify_api = SpotifyApi()
        spotify_api.auth()

if __name__ == "__main__":
    unittest.TestCase()