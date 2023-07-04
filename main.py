import argparse
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from album_dataset_creation import add_albums

album_input = [
    {"name": "Patsy Hangdog", "year": 2020},
    {"name": "Myth", "year": 2023},
    {"name": "All Bitches Die", "year": 2018},
    {"name": "A flame my love, a frequency", "year": 2017},
    {"name": "Sunbather", "year": 2013},
]


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        )
    )

    #    album_list = args.albums
    dataset = args.data
    if args.task == "add_entries":
        add_albums(album_input, dataset)
    elif args.task == "recommend":
        pass


if __name__ == "__main__":
    main()
