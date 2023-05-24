import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from collections import defaultdict

os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"],
                                                           client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))
"""
These are functions I've created to interact with the Spotify API to average track data across albums, so that
I can perform ALBUM recommendation, rather than track recommendation. Averaging may not be the best approach, and I may
move in a different direction in the future. I will be creating my own dataset of these metrics via these functions.
"""


def find_album(name, year):
    album_data = defaultdict()
    results = sp.search(q= 'album: {} year: {}'.format(name,year), limit=1)
    results = results['tracks']['items'][0]
    album_id = results['album']['id']
    album_data['name'] = [name]
    album_data['year'] = [year]
    album_data['popularity'] = [results['popularity']]
    album_data['album_id'] = [album_id]
    album_data['artist'] = results['artists'][0]['name']
    return pd.DataFrame(album_data)


# album_tracks = sp.album_tracks(album_id=album_info['album_id'][0])
# album_track_items = album_tracks['items']
# track_data = tracks_audio_features(album_track_items)

def tracks_audio_features(thing):

    i = 0
    track_data = []
    while i < len(thing):
        audio_features = sp.audio_features(thing[i]['id'])[0]
        track_data.append(audio_features)
        i+=1
    return track_data

def album_data_mean(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

def extract_keys(track_data, keys_to_extract):
    j = 0
    edited_list = []
    while j < len(track_data):
        res = dict(filter(lambda item: item[0] in keys_to_extract, track_data[j].items()))
        edited_list.append(res)
        j += 1
    return edited_list

def make_entry(name, year, keys):
    album_info = find_album(name, year)
    album_tracks = sp.album_tracks(album_id = album_info['album_id'][0])
    album_track_items = album_tracks['items']
    track_data = tracks_audio_features(album_track_items)
    edited_list = extract_keys(track_data, keys)
    album_df = pd.DataFrame(album_data_mean(edited_list), index=[0])
    entry_df = pd.concat([album_info, album_df], axis=1)
    return entry_df