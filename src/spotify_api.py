import requests
import base64

BASE_URL = "https://api.spotify.com/v1/search"
client_id = ""
client_secret = ""


class SpotifyApi:
    def __init__(self, code):
        token_url = "https://accounts.spotify.com/api/token"

        params = {
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:8080",
            "code": code
        }

        encoded_auth = base64.urlsafe_b64encode(("%s:%s" % (client_id, client_secret)).encode("utf-8"))
        headers = {
            "Authorization": encoded_auth,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.get(token_url, params=params, headers=headers)
        print(response.status_code)


if __name__ == "__main__":
    code = ""
    api = SpotifyApi(code)