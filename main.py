import argparse
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from album_dataset_creation import add_albums
from recommendation import get_recommendations

# Note for your own purposes, you would have to put in your own CLIENT_ID and CLIENT_SECRET.
# TO DO : Make it so that if the album is already present in .csv file, it doesn't have to query spotify or rym.
os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"

#os.environ["SPOTIFY_CLIENT_ID"] = "38aa6dbab43f46898cea5c5a82ba8b24"
#os.environ["SPOTIFY_CLIENT_SECRET"] = "88c7f081441f4e5d90c9df23984469ac"


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    task_choices = ["add_entries", "recommend"]
    parser = argparse.ArgumentParser("Perform tasks for album recommendation.")
    parser.add_argument(
        "--task",
        type=str,
        help="Task you would like to perform",
        choices=task_choices,
        required=True,
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Directory of the dataset of album information for recommendations or additions to be made.",
    )

    parser.add_argument(
        "--from_csv",
        type=str,
        help="Directory of CSV if you're choosing to do that form of upload. Default False, and prompts inputs.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.from_csv is None:
        n = int(input("How many albums are you uploading: "))  # W: Missing module docstring
        album_dict = {}
        album_list = []
        for i in range(n):
            album = input("Enter album name and year in the format Album Name - Arist:")
            try:
                name, artist = album.split(" - ")
            except ValueError:
                name, artist = album.split("-")
            album_dict = {"name": name.strip(), "artist": (artist.strip())}
            album_list.append(album_dict)

    else:
        input_dataset = pd.read_csv(args.from_csv, usecols=["Album", "Last Name"])
        input_dataset.dropna(inplace=True)
        album_dict = {}
        album_list = []
        for index, row in input_dataset.iterrows():
            name = row["Album"]
            artist = row["Last Name"]
            album_dict = {"name": name, "artist": artist}
            album_list.append(album_dict)

    dataset = args.data
    if args.task == "add_entries":
        add_albums(album_list, dataset)
    elif args.task == "recommend":
        new_rows = add_albums(album_list, dataset)
        df = pd.read_csv(dataset)
        df.drop_duplicates(inplace=True, ignore_index=False)
        df.to_csv(dataset, index=False)
        get_recommendations(new_rows, dataset)


if __name__ == "__main__":
    main()
