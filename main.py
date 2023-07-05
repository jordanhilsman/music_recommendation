import argparse
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from album_dataset_creation import add_albums

# TO DO: MAKE IT EASIER TO RUN THIS WITHOUT DOING A LIST OF DICTIONARIES IF POSSIBLE? TOO USER UNFRIENDLY + HARD TO RUN WITH ARGPARSER.
# Note for your own purposes, you would have to put in your own CLIENT_ID and CLIENT_SECRET.
# To Do: Look into using global variables or whatever they're called to call these without showing the world
# my client secret/id.
os.environ["SPOTIFY_CLIENT_ID"] = "9236160482de4e9784a90b999ae169b7"
os.environ["SPOTIFY_CLIENT_SECRET"] = "b82e4df8039b466ead3a20765efa1b64"


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
    #    parser.add_argument("--albums", type=str, nargs="+", help="List of albums in the format 'Album Name - Album Year', or a predefined variable name")
    parser.add_argument(
        "--data",
        type=str,
        help="Directory of the dataset of album information for recommendations or additions to be made.",
    )

    parser.add_argument("--from_csv", type=str, help="Directory of CSV if you're choosing to do that form of upload. Default False, and prompts inputs.")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        )
    )
    if args.from_csv is None:
        n = int(input("How many albums are you uploading: "))  # W: Missing module docstring
        album_dict = {}
        album_list = []
        for i in range(n):
            album = input("Enter album name and year in the format Name - Year:")
            try:
                name, year = album.split(" - ")
            except ValueError:
                name, year = album.split("-")
            album_dict = {"name": name.strip(), "year": int(year.strip())}
            album_list.append(album_dict)

    else:
        input_dataset = pd.read_csv(args.from_csv, usecols=["Album", "Year"])
        input_dataset.dropna(inplace=True)
#        input_dataset['Year'] = input_dataset['Date'].str[-4:].astype(int)
        album_dict = {}
        album_list = []
        for index, row in input_dataset.iterrows():
            name = row["Album"]
            year = row["Year"]
            album_dict = {"name": name, "year": year}
            album_list.append(album_dict)

    dataset = args.data
    if args.task == "add_entries":
        add_albums(album_list, dataset)
    elif args.task == "recommend":
        pass


if __name__ == "__main__":
    main()
