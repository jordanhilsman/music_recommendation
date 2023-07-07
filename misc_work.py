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
album_list = []
full_name_list = []
for i in range(5): # W: Unused variable 'i'
    album = input("Enter album name and year in the format Name - Year:") # E: line too long (81 > 79 characters)
    try:
        name, year = album.split(" - ")
    except ValueError:
        name, year = album.split("-")
    album_dict = {"name": name.strip(), "year": int(year.strip())}
    album_list.append(album_dict)




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
df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x))
sample = df.sample(n=5, random_state=1337)
averages = sample.loc[:, keys_to_extract].mean()
combined_genres = [item for sublist in sample['genres'].tolist() for item in sublist]
average_row = pd.DataFrame([averages])
average_row['genres'] = [combined_genres]
subset_df = df[df['genres'].apply(lambda x: any(item in x for item in combined_genres))]
print(sample)

distances = cdist(average_row[keys_to_extract], subset_df[keys_to_extract], "cosine")

n_songs=5
index = list(np.argsort(distances)[:, :n_songs][0])
recs = subset_df.iloc[index]
recs = recs[['artist','name']]
#print(recs['name'], recs['artist'])
print(recs)

distances_nosubset = cdist(average_row[keys_to_extract], df[keys_to_extract], "cosine")
index2 = list(np.argsort(distances_nosubset)[:, :n_songs][0])
recs_nosubset = df.iloc[index2]
recs_nosubset = recs_nosubset[['artist','name']]

print(recs_nosubset)
