from src.spotify_api import SpotifyApi
from src.bbc_api import *
import os

token = os.environ['SPOTIFY_TOKEN']
spotify_api = SpotifyApi(token)

if __name__ == "__main__":
    # playlist_id = "7kYarjUU5jN5hFPMmiCTN2"
    playlist_id = "7kYarjUU5jN5hFPMmiCTN2"

    # playlist_id = "20JGSnhbas26vwufCpq2dj"

    program_names = [fetch_program_names()[0]]

    for program_name in program_names:
        tracks = fetch_playlist_from_program(program_name)
        uris = []
        for track in tracks:
            # print(track)
            result = spotify_api.search(track)
            if not len(result):
                print("Could not find track %s" % track)

                # try without ()
                index_of_param = track.find("(")
                end_index_of_param = track.find(")")
                if index_of_param and end_index_of_param:
                    # strip out ( )
                    track_stripped = track[0:index_of_param]
                    print("Trying %s..." % track_stripped)
                    result = spotify_api.search(track_stripped)

                    if not len(result):
                        print("Still couldn't find it..")
                        continue
                    else:
                        print("Found it!")

            uris.append(result[0]['uri'])

        print("Have %d tracks to add" % len(uris))
        spotify_api.add_tracks_to_playlist(playlist_id, uris)
