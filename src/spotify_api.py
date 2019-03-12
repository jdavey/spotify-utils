import requests

BASE_URL = "https://api.spotify.com/v1"
client_id = ""
client_secret = ""


class SpotifyApi:
    def __init__(self, token):
        self.token = token

    def _get_headers(self):
        return {
            "Authorization": "Bearer %s" % self.token
        }

    def search(self,
               terms,
               types=["track"]
               ):
        params = {
            "q": terms,
            "type": ",".join(types)
        }

        search_url = "%s/search" % BASE_URL
        search_response = requests.get(search_url, params=params, headers=self._get_headers())
        search_payload = search_response.json()
        return search_payload



if __name__ == "__main__":
    code = ""
    api = SpotifyApi(code)