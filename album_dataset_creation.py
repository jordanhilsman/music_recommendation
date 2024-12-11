import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from collections import defaultdict

spotipy_cid = os.getenv("SPOTIFY_CLIENT_ID")
spotipy_csecret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=spotipy_cid, client_secret=spotipy_csecret
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


def find_album(name, artist):
    album_data = defaultdict()
    results = sp.search(q="album: {} artist: {}".format(name, artist), limit=1)
    results = results["tracks"]["items"][0]
    album_id = results["album"]["id"]
    album_data["name"] = [name]
    album_data["artist"] = [artist]
    album_data["album_id"] = [album_id]
    album_data["year"] = results["album"]["release_date"][0:4]
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
            if weight != 0:
                weighted_sum[key] += value * weight
                total_weight += weight
            else:
                weighted_sum[key] += value
    weighted_average = {}
    for key, value in weighted_sum.items():
        if total_weight != 0:
            weighted_average[key] = value / total_weight
        else:
            weighted_average[key] = value
    return weighted_average


def extract_keys(track_data, keys):
    j = 0
    edited_list = []
    while j < len(track_data):
        res = dict(filter(lambda item: item[0] in keys, track_data[j].items()))
        edited_list.append(res)
        j += 1
    return edited_list


def make_entry(name, artist, keys):
    album_info = find_album(name, artist)
    album_tracks = sp.album_tracks(album_id=album_info["album_id"][0])
    album_track_items = album_tracks["items"]
    track_data, track_popularity = tracks_audio_features(album_track_items)
    edited_list = extract_keys(track_data, keys)
    album_df_existing = pd.DataFrame(weighted_averaging(edited_list, track_popularity), index=[0])
    entry_df_existing = pd.concat([album_info, album_df_existing], axis=1)
    return entry_df_existing


def add_albums(album_list, filename):
    added_rows = pd.DataFrame()
    df_existing = pd.read_csv(filename)
    i = 0
    while i < len(album_list):
        name = album_list[i]["name"]
        artist = album_list[i]["artist"]
        present = df_existing[(df_existing["name"] == name) & (df_existing["artist"] == artist)]
        if not present.empty:
            added_rows = pd.concat([added_rows, present], axis=0)
        else:
            data = make_entry(name, artist, keys_to_extract)
            added_rows = pd.concat([added_rows, data], axis=0)
        i += 1
    df_updated = pd.concat([df_existing, added_rows], ignore_index=True)
    df_updated.drop_duplicates(inplace=True)
    df_updated.to_csv(filename, index=False)
    return added_rows
