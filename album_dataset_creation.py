import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from collections import defaultdict

#os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
#os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"

os.environ["SPOTIFY_CLIENT_ID"] = "38aa6dbab43f46898cea5c5a82ba8b24"
os.environ["SPOTIFY_CLIENT_SECRET"] = "88c7f081441f4e5d90c9df23984469ac"


sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]
    )
)
"""
These are functions I've created to interact with the Spotify API to average track data across albums, so that
I can perform ALBUM recommendation, rather than track recommendation. Averaging may not be the best approach, and I may
move in a different direction in the future. I will be creating my own dataset of these metrics via these functions.
"""

keys_to_extract = [
    "danceability",
    "energy",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]


def find_album(name, year):
    album_data = defaultdict()
    results = sp.search(q="album: {} year: {}".format(name, year), limit=1)
    results = results["tracks"]["items"][0]
    album_id = results["album"]["id"]
    album_data["name"] = [name]
    album_data["year"] = [year]
    album_data["album_id"] = [album_id]
    album_data["artist"] = results["artists"][0]["name"]
    print(f"{name} has been found.")
    return pd.DataFrame(album_data)


def tracks_audio_features(thing):
    i = 0
    track_data = []
    popularity = []
    while i < len(thing):
        track = sp.track(thing[i]["id"])
        popularity.append(track["popularity"])
        audio_features = sp.audio_features(thing[i]["id"])[0]
        track_data.append(audio_features)
        i += 1

    return track_data, popularity


def weighted_averaging(dictionary, popularity):
    weighted_sum = {}
    total_weight = 0

    for dictionary, weight in zip(dictionary, popularity):
        for key, value in dictionary.items():
            if key not in weighted_sum:
                weighted_sum[key] = 0
            weighted_sum[key] += value * weight
        total_weight += weight

    weighted_average = {}
    for key, value in weighted_sum.items():
        weighted_average[key] = value / total_weight

    return weighted_average


def extract_keys(track_data, keys):
    j = 0
    edited_list = []
    while j < len(track_data):
        res = dict(filter(lambda item: item[0] in keys, track_data[j].items()))
        edited_list.append(res)
        j += 1
    return edited_list


def make_entry(name, year, keys):
    album_info = find_album(name, year)
    album_tracks = sp.album_tracks(album_id=album_info["album_id"][0])
    album_track_items = album_tracks["items"]
    track_data, track_popularity = tracks_audio_features(album_track_items)
    edited_list = extract_keys(track_data, keys)
    album_df = pd.DataFrame(weighted_averaging(edited_list, track_popularity), index=[0])
    entry_df = pd.concat([album_info, album_df], axis=1)
    return entry_df


def bulk_entry(album_list, keys):
    new_rows = pd.DataFrame()
    i = 0
    while i < len(album_list):
        name = album_list[i]["name"]
        year = album_list[i]["year"]
        data = make_entry(name, year, keys)
        new_rows = pd.concat([new_rows, data], axis=0)
        i += 1
    return new_rows


def add_albums(album_list, filename):
    added_rows = bulk_entry(album_list, keys_to_extract)
    df_existing = pd.read_csv(filename)
    df_updated = pd.concat([df_existing, added_rows], ignore_index=True)
    df_updated.drop_duplicates(
        subset=["album_id"], inplace=True, ignore_index=True
    )  # E: line too long (80 > 79 characters)
    df_updated.reset_index(drop=True, inplace=True)
    df_updated.to_csv(filename, index=False)
