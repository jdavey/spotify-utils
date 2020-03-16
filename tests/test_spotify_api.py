import unittest
from src.bbc_api import parse_program_id, fetch_playlist_from_program
from src.spotify_api import SpotifyApi

token = "BQBZc6lgR7OGjknyeOgVe8TVYEb9NcUhsV0I4Ev1I0P3sRhl0w7jfBVEXR1AW-J7TiQ70AyhuFEL9zId2wOshS0Z0h9TPRmn88mRz5yJJOe8TFGq-_QvDI9vLsOFAqu8V5-sMphN3jTXh42syNh4oaItJkbLfRw28xs_bwvEIM0qalA9xquz0YtcpE8Qjw8SuCKQ6xUEogXZ0aZgfM3PA_T_UA"

class SpotifyApiTest(unittest.TestCase):
    def test_search(self):
        terms = "The 1975 - Sincerity Is Scary"
        api = SpotifyApi(token)
        results = api.search(terms)
        print(results)

    def test_playlists(self):
        api = SpotifyApi(token)
        results = api.get_playlists("joeman5683")
        print(len(results))

if __name__ == "__main__":
    unittest.TestCase()