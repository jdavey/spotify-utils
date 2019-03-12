import unittest
from src.bbc_api import parse_program_id, fetch_playlist_from_program


class BbcApiTest(unittest.TestCase):
    def test_parse_program_id(self):
        link = "https://www.bbc.co.uk/programmes/m000320s"
        program_name_expected = "m000320s"
        self.assertEquals(program_name_expected, parse_program_id(link), msg="program name parsed correctly")

    def test_fetch_playlist_from_program(self):
        playlist = fetch_playlist_from_program('m000320s')
        print(playlist)


if __name__ == "__main__":
    unittest.TestCase()