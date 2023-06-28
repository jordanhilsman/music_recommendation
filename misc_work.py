from album_dataset_creation import *
import pandas as pd

os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"],
                                                           client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))


keys_to_extract = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']



rolling_stones_albums = [
    {'name': 'Landwerk No. 2', 'year':2020},
    {'name': '7G', 'year':2020},
    {'name': 'Heaven or Las Vegas', 'year':2020}]


new_rows = bulk_entry(rolling_stones_albums, keys_to_extract)

filename='spotify_album_data.csv'
df_existing = pd.read_csv(filename)
#df_updated = df_existing.drop_duplicates(subset=['album_id'])
df_updated = df_existing._append(new_rows, ignore_index=True)

df_updated.to_csv(filename, index=False)

