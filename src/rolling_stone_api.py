from bs4 import BeautifulSoup
import requests
import logging
import sys
import os

from src.spotify_api import SpotifyApi

logger = logging.getLogger(__name__)
token = os.environ['SPOTIFY_TOKEN']
spotify_api = SpotifyApi(token)

URLs = [
    "https://www.rollingstone.com/music/music-lists/best-albums-2010s-ranked-913997",
    "https://www.rollingstone.com/music/music-lists/best-albums-2010s-ranked-913997/?list_page=2"
]

if __name__ == "__main__":
    albums = []
    playlist_id = "1Arhb22zt6EhV7xXGhqeLy"
    for url in URLs:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Unable to read URL %s response: %d" % (URL, response.status_code))
            sys.exit(1)

        soup = BeautifulSoup(response.content)

        articles = soup.find_all("article", "c-list__item")
        for article in articles:
            attrs = article.attrs
            num = attrs.get('data-list-item')
            list_title = attrs.get('data-list-title')

            if not num or not list_title:
                continue

            title_split = list_title.split(",")
            artist = title_split[0]
            title = "".join(title_split[1:]).replace("‘", "").replace("’", "").replace("'", "")

            albums.append(
                {
                    "title": title,
                    "artist": artist,
                    "rank": num
                }
            )

    ranked_albums = reversed(albums)
    for i, album in enumerate(ranked_albums, 1):
        artist = album['artist']
        album = album['title']

        print(f"{i}: {artist} - {album} ")
        search = spotify_api.search(f"artist:{artist} album:{album}", types=['album'])

        if 'albums' not in search or not len(search['albums']['items']):
            print(f"Could not find album {artist} {album} trying just album")
            continue

        search = spotify_api.search(f"album:{album}", types=['album'])

        if 'albums' not in search or not len(search['albums']['items']):
            print(f"Could not find album {artist} {album} for real")
            continue

        album_id = search['albums']['items'][0]['id']
        tracks = spotify_api.get_tracks_from_album(album_id)

        if 'items' not in tracks:
            print(f"No tracks for {artist} {album}")
            continue

        track_uris = list(map(lambda t: t['uri'], tracks['items']))
        print(f"Have {len(track_uris)} to add")

        spotify_api.add_tracks_to_playlist(playlist_id, track_uris)



