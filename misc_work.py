import argparse # W: Missing module docstring
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from album_dataset_creation import add_albums
from scipy.spatial.distance import cdist
import ast
import numpy as np
import pandas as pd # W: Missing module docstring
from rymscraper import rymscraper, RymUrl # W: 'rymscraper.RymUrl' imported but unused # W: Unused RymUrl imported from rymscraper
df = pd.read_csv('spotify_album_data.csv')
network = rymscraper.RymNetwork()

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
    combined_genres = [item for sublist in album_list['genres'].tolist() for item in sublist]
    average_row = pd.DataFrame([averages])
    average_row['genres'] = [combined_genres]
    subset_df = full_dataframe[full_dataframe['genres'].apply(lambda x: any(item in x for item in combined_genres))]
    distances = cdist(average_row[keys_to_extract], subset_df[keys_to_extract], "cosine")
    distances_nosubset = cdist(average_row[keys_to_extract], full_dataframe[keys_to_extract], "cosine") # E: Undefined variable 'average_row' # E: undefined name 'average_row' # E: line too long (87 > 79 characters)
    index = list(np.argsort(distances)[:, :n_songs][0])
    recs = subset_df.iloc[index]
    recs = recs[['artist', 'name']]
    print(f"Recommendations based on cosine distance and shared genres:\n {recs}")
    index2 = list(np.argsort(distances_nosubset)[:, :n_songs][0])
    recs_nosubset = df.iloc[index2]
    recs_nosubset = recs_nosubset[['artist','name']] # E: missing whitespace after ','
    print(f"Recommendations based on cosine distance alone:\n {recs_nosubset}")
