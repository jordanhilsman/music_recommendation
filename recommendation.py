import os
import pandas as pd
from scipy.spatial.distance import cdist
import numpy as np

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

n_albums = 5


def get_five_rec(average, full_dataframe, method):
    distance = cdist(average[keys_to_extract], full_dataframe[keys_to_extract], method)
    idx = list(np.argsort(distance)[:, :n_albums][0])
    reccs = full_dataframe.iloc[idx]
    reccs = reccs[["artist", "name"]]
    return reccs


def get_recommendations(album_list, full_dataframe):
    full_dataframe = pd.read_csv(full_dataframe)
    averages = album_list.loc[:, keys_to_extract].mean()
    average_row = pd.DataFrame([averages])
    recs_cos = get_five_rec(average_row, full_dataframe, "cosine")
    print(f"Recommendations based on cosine distance:\n {recs_cos}")
    recs_canb = get_five_rec(average_row, full_dataframe, "canberra")
    print(f"Recommendations based on canberra distance:\n {recs_canb}")
