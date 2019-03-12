import unittest
from src.bbc_api import parse_program_id, fetch_playlist_from_program
from src.spotify_api import SpotifyApi

token = "BQCJhaGxII2ZeYE0Y28kyhV5U_OVBy4j9HjLkof-cylhNVDs0GL2wSO4kTZWIImusEIzwGnApm52afJ_VRPZZf7ZVH--rGvJjrpjw1vh_PGC8UHFtac6u4cWCEDTnDQ1_zN9hawV_KWZPxVVWdbLsYUfOmUeBhdgtX7RJwGe_rXDg1Uepw"
class SpotifyApiTest(unittest.TestCase):
    def test_search(self):
        terms = "The 1975 - Sincerity Is Scary"
        api = SpotifyApi(token)
        results = api.search(terms)
        print(results)

if __name__ == "__main__":
    unittest.TestCase()