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
        if search_response.status_code != 200:
            raise Exception(f"Bad status code {search_response.status_code}")

        search_payload = search_response.json()
        return search_payload

    def create_playlist(self, name, description, user_name, public=True):
        playlist_url = f"{BASE_URL}/users/{user_name}/playlists"

        payload = {
            "name": name,
            "description": description,
            "public": public
        }

        playlist_create_response = requests.post(playlist_url, json=payload, headers=self._get_headers())
        if playlist_create_response.status_code == 201:
            return playlist_create_response.json().get('id', None)

        raise Exception(f"Bad status code on playlist creation {playlist_create_response.status_code}")

    def get_or_create_playlist(self, name, description, public=True):
        params = {
            "q": name,
            "type": "playlist"
        }
        search_url = "%s/search" % BASE_URL
        search_response = requests.get(search_url, params=params, headers=self._get_headers())
        search_payload = search_response.json()
        playlist_id = None
        if search_payload['playlists']['items']:
            playlists = search_payload['playlists']['items']
            for playlist in playlists:
                if playlist['name'] == name:
                    print("Playlist already exists")
                    playlist_id = playlist["id"]
                    break

        if not playlist_id:
            playlist_url = "%s/playlists" % BASE_URL
            payload = {
                "name": name,
                "description": description,
                "public": public
            }

            playlist_create_response = requests.post(playlist_url, json=payload, headers=self._get_headers())

            # todo - this is giving a 404
            print(playlist_create_response)

        return playlist_id

    def add_tracks_to_playlist(self, playlist_id, uris):
        url = "%s/playlists/%s/tracks" % (BASE_URL, playlist_id)
        payload = {
            "uris": uris
        }

        response = requests.post(url, json=payload, headers=self._get_headers())
        print(response)

    def get_tracks_from_album(self, album_id):
        url = f"{BASE_URL}/albums/{album_id}/tracks"
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def get_playlists(self, user_name):

        more_results = True
        offset = 0
        limit = 25
        all_playlists = []
        while more_results:
            # spotify:user:joeman5683
            url = f"{BASE_URL}/users/{user_name}/playlists"
            params = {
                "limit": limit,
                "offset": offset
            }

            response = requests.get(url, params=params, headers=self._get_headers())
            results = response.json()
            playlists = results.get("items", [])

            if len(playlists):
                more_results = True
                offset = offset + limit
                all_playlists.extend(playlists)
            else:
                more_results = False

        return all_playlists