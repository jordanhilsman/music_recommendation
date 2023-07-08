import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist


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
n_songs = 10


def top_5_recs(average_input, full_dataframe, method):
    distances = cdist(average_input[keys_to_extract], full_dataframe[keys_to_extract], method)
    full_index = list(np.argsort(distances)[:, :n_songs][0])
    reccs = full_dataframe.iloc[full_index]
    reccs = reccs[["artist", "name"]]
    return reccs


def get_recommendations(album_list, full_dataframe):
    full_dataframe = pd.read_csv(full_dataframe)
    averages = album_list.loc[:, keys_to_extract].mean()
    average_row = pd.DataFrame([averages])
    cosine_recs = top_5_recs(average_row, full_dataframe, "cosine")
    print(f"Recommendations based on cosine distance:\n {cosine_recs}")
    canberra_recs = top_5_recs(average_row, full_dataframe, "canberra")
    print(f"Recommendations based on canberra distance:\n {canberra_recs}")
