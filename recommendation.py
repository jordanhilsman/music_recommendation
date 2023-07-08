import argparse  # W: Missing module docstring
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from album_dataset_creation import add_albums
from scipy.spatial.distance import cdist
import ast
import numpy as np
import pandas as pd  # W: Missing module docstring
from numpy.linalg import norm
df = pd.read_csv("spotify_album_data.csv")

os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"


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
n_songs = 5

def get_recommendations(album_list, full_dataframe):
    full_dataframe = pd.read_csv(full_dataframe)
    averages = album_list.loc[:, keys_to_extract].mean()
    average_row = pd.DataFrame([averages])
    distances_nosubset = cdist(
        average_row[keys_to_extract], full_dataframe[keys_to_extract], "cosine"
    )  # E: Undefined variable 'average_row' # E: undefined name 'average_row' # E: line too long (87 > 79 characters)
    
    index2 = list(np.argsort(distances_nosubset)[:, :n_songs][0])
    recs_nosubset = full_dataframe.iloc[index2]
    recs_nosubset = recs_nosubset[["artist", "name"]]  # E: missing whitespace after ','
    print(f"Recommendations based on cosine distance:\n {recs_nosubset}")
    canberra_distances = cdist(average_row[keys_to_extract], full_dataframe[keys_to_extract], "canberra")
    index = list(np.argsort(canberra_distances)[:, :n_songs][0])
    recs = full_dataframe.iloc[index]
    recs = recs[["artist","name"]]
    print(f"Recommendations based on canberra distance:\n {recs}")
