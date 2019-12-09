import requests
from bs4 import BeautifulSoup
import logging
import sys
import os

from src.spotify_api import SpotifyApi

LIST_URL = "https://pitchfork.com/features/lists-and-guides/best-songs-2019/"

logger = logging.getLogger(__name__)

DIRTY_CHARS = [
    '“',
    '”'
]

token = os.environ['SPOTIFY_TOKEN']
spotify_api = SpotifyApi(token)


def clean(string):
    for char in DIRTY_CHARS:
        while char in string:
            string = string.replace(char, "")

    if "[" in string:
        string = string[0:string.index("[")]

    return string.strip()

def fetch_tracks():
    response = requests.get(LIST_URL)
    if response.status_code != 200:
        logger.error("Unable to read URL %s response: %d" % (LIST_URL, response.status_code))
        sys.exit(1)

    soup = BeautifulSoup(response.content)
    tracks = soup.find_all("div", "heading-h3", "h2")
    listing = []
    for track in tracks:
        track_details = track.nextSibling.next
        track_split = track_details.split(":")
        artist = clean(track_split[0])
        title = clean(track_split[1])

        listing.append({
            "artist": artist,
            "track": title
        })

    return listing

if __name__ == "__main__":
    tracks = fetch_tracks()
    uris = []
    for track in reversed(tracks):
        search = spotify_api.search(f"artist:{track['artist']} track:{track['track']}", types=['track'])
        if "tracks" in search and "items" in search['tracks'] and len(search['tracks']['items']):
            uri = search['tracks']['items'][0]['uri']
            uris.append(uri)
        else:
            search = spotify_api.search(f"track:{track['track']}", types=['track'])
            if "tracks" in search and "items" in search['tracks'] and len(search['tracks']['items']):
                uri = search['tracks']['items'][0]['uri']
                uris.append(uri)
            else:
                print(f"Couldn't find {track}")

    playlist_id = "65BeGJfIMrZPsZv7Dr1GR9"
    spotify_api.add_tracks_to_playlist(playlist_id, uris)