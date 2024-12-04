# music_recommendation
Where I am working on a program to recommend albums based on Spotify album listening history.

##NOTE:
As of November 27th, 2024 this project has been made obsolete due to changes in the Spotify API that deprecated the endpoint
for retrieving audio features from tracks.

## Setup

```console
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Generating Album Recommendations

Run the following to generate a list of 5 album recommendations based on cosine distance and Canberra distance.
Note: You should be in the directory of the recommendation system.
```console
$ python main.py --task recommend --data spotify_album_data.csv

```
This will prompt you for an amount of albums you would like to be given recommendations from.
Albums should be input in the form:
"ALBUM NAME - ARTIST NAME"
