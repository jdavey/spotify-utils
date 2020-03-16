from src.spotify_api import SpotifyApi
from src.bbc_api import *
import os

token = os.environ['SPOTIFY_TOKEN']
spotify_api = SpotifyApi(token)
USER = "joeman5683"

if __name__ == "__main__":
    # playlist_id = "7kYarjUU5jN5hFPMmiCTN2"
    add_to_master = False
    add_to_ep = True

    master_playlist_id = "7kYarjUU5jN5hFPMmiCTN2"
    existing_playlists = spotify_api.get_playlists("joeman5683")
    program_names = [fetch_program_names()[4]]

    for program_name in program_names:
        playlist_name, tracks = fetch_playlist_from_program(program_name)

        uris = []
        for track in tracks:
            # print(track)
            result = spotify_api.search(track)["tracks"]["items"]
            if not len(result):
                print("Could not find track %s" % track)

                # try without ()
                index_of_param = track.find("(")
                end_index_of_param = track.find(")")
                if index_of_param and end_index_of_param:
                    # strip out ( )
                    track_stripped = track[0:index_of_param]
                    print("Trying %s..." % track_stripped)
                    result = spotify_api.search(track_stripped)["tracks"]["items"]

                    if not len(result):
                        print("Still couldn't find it..")
                        continue
                    else:
                        print("Found it!")

            uris.append(result[0]['uri'])

        print("Have %d tracks to add" % len(uris))

        if add_to_ep:
            existing_playlist = list(filter(lambda p: p['name'] == playlist_name, existing_playlists))
            bbc_link = get_program_player_url(program_name)

            playlist_id = None
            if len(existing_playlist):
                playlist_id = existing_playlist[0]['id']
            else:
                playlist_id = spotify_api.create_playlist(playlist_name, bbc_link, USER)

            spotify_api.add_tracks_to_playlist(playlist_id, uris)

        if add_to_master:
            spotify_api.add_tracks_to_playlist(master_playlist_id, uris)
