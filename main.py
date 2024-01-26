"""Get song titles and artists from Spotify playlist"""

import csv
import logging
import os
import re
import pandas as pd

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OATH_CREATE_PLAYLIST = os.getenv("OATH_CREATE_PLAYLIST", "")
# specify csv files and directory
OUTPUT_DIR = "data"

# create array of weighting
weights = list(range(100,0,-1))
rank = list(range(1,101,1))
# add column for each name in count with the rank value specified
for x in range(0,10):
    weights[x] = weights[x] + 10

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


def get_playlist_uri_from_link(playlist_link: str) -> str:
    """Get Spotify playlist URI from Spotify playlist link

    The URI is the bit after 'playlist' but before the '?'

    Example:
    get_playlist_uri_from_link(
        "https://open.spotify.com/playlist/6jAarBZaMmBLnSIeltPzkz?si=d42be5c6ec194bb9"
    )
    >>> "6jAarBZaMmBLnSIeltPzkz"

    """
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlist_link):
        return match.groups()[0]
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")


def save_csv_from_uri(user):
    # get uri from https link
    playlist_uri = get_playlist_uri_from_link(user["link"])

    # get list of tracks in a given playlist (note: max playlist length 100)
    tracks = session.playlist_tracks(playlist_uri)["items"]

    # create csv file
    file_path = "/".join([OUTPUT_DIR, user["name"] + ".csv"])
    with open(file_path, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["track", "artist", "weight", user["name"]])
        # start weight counter
        j = 0

        # extract name and artist
        for track in tracks:
            name = track["track"]["name"]
            artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )

            # write to csv
            writer.writerow([name, artists, weights[j], rank[j]])
            # increment weight counter
            j = j + 1

    logger.info("Extracted data saved in %s", file_path)


def save_csvs_from_links(df):
    for i in range(0,(links_df.shape[0])):
        save_csv_from_uri(df.iloc[i])


def csv_to_df(filename):   
    file_path = "/".join([OUTPUT_DIR, filename + ".csv"])
    df = pd.read_csv(file_path)
    return df


# def create_dfs_from_links(df):
#     for i in range(0,(links_df.shape[0])):
#         csv_to_df(df.iloc[i]["name"])


def df_to_csv(df, OUTPUT_FILE_NAME):   
    file_path = "/".join([OUTPUT_DIR, OUTPUT_FILE_NAME])
    df.to_csv(file_path)
    print('\nData saved in', file_path)


def combine_df(df1, df2):
    length = df1.shape[0]
    for j in range(0, df2.shape[0]):
        match = False
        for i in range(0, length):
            if df1.iloc[i]['track'] == df2.iloc[j]['track']:
                if df1.iloc[i]['artist'] == df2.iloc[j]['artist']:
                    match = True
                    df1.at[i, 'weight'] = df1.iloc[i]['weight'] + df2.iloc[j]['weight'] + 50
                    df1.at[i, df2.columns[3]] = df2.iloc[j][df2.columns[3]]
                    print([df2.iloc[j]['track'], df2.iloc[j]['artist']])
                    print('match')
                    break
                print('track matched, artist didnt')
                print([df2.iloc[j]['track'], df2.iloc[j]['artist'], df1.iloc[i]['artist']])
        if match == False:
            new_track = pd.DataFrame([[df2.iloc[j]['track'], df2.iloc[j]['artist'], df2.iloc[j]['weight'], df2.iloc[j][df2.columns[3]]]], columns=['track', 'artist', 'weight', df2.columns[3]])
            df1 = pd.concat([df1, new_track], ignore_index=True)
    return df1


if __name__ == "__main__":
    # authenticate
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )

    # create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # user_id = "1236848429"

    links_df = csv_to_df(filename="links")

    save_csvs_from_links(links_df) # to add all playlists as csvs
    save_csv_from_uri(links_df.iloc[16]) # to add one playlists as a csv

    # create_dfs_from_links(links_df)
    df_0  = csv_to_df(links_df.iloc[0]["name"])
    df_1 = csv_to_df(links_df.iloc[1]["name"])
    df_2 = csv_to_df(links_df.iloc[2]["name"])
    df_3 = csv_to_df(links_df.iloc[3]["name"])
    df_4 = csv_to_df(links_df.iloc[4]["name"])
    df_5 = csv_to_df(links_df.iloc[5]["name"])
    df_6 = csv_to_df(links_df.iloc[6]["name"])
    df_7 = csv_to_df(links_df.iloc[7]["name"])
    df_8 = csv_to_df(links_df.iloc[8]["name"])
    df_9 = csv_to_df(links_df.iloc[9]["name"])
    df_10 = csv_to_df(links_df.iloc[10]["name"])
    df_11 = csv_to_df(links_df.iloc[11]["name"])
    df_12 = csv_to_df(links_df.iloc[12]["name"])
    df_13 = csv_to_df(links_df.iloc[13]["name"])
    df_14 = csv_to_df(links_df.iloc[14]["name"])
    df_15 = csv_to_df(links_df.iloc[15]["name"])
    df_16 = csv_to_df(links_df.iloc[16]["name"])

    df_count = df_0
    print('\nSearching 1')
    df_count = combine_df(df1=df_count, df2=df_1)
    print('\nSearching 2')
    df_count = combine_df(df1=df_count, df2=df_2)
    print('\nSearching 3')
    df_count = combine_df(df1=df_count, df2=df_3)
    print('\nSearching 4')
    df_count = combine_df(df1=df_count, df2=df_4)
    print('\nSearching 5')
    df_count = combine_df(df1=df_count, df2=df_5)
    print('\nSearching 6')
    df_count = combine_df(df1=df_count, df2=df_6)
    print('\nSearching 7')
    df_count = combine_df(df1=df_count, df2=df_7)
    print('\nSearching 8')
    df_count = combine_df(df1=df_count, df2=df_8)
    print('\nSearching 9')
    df_count = combine_df(df1=df_count, df2=df_9)
    print('\nSearching 10')
    df_count = combine_df(df1=df_count, df2=df_10)
    print('\nSearching 11')
    df_count = combine_df(df1=df_count, df2=df_11)
    print('\nSearching 12')
    df_count = combine_df(df1=df_count, df2=df_12)
    print('\nSearching 13')
    df_count = combine_df(df1=df_count, df2=df_13)
    print('\nSearching 14')
    df_count = combine_df(df1=df_count, df2=df_14)
    print('\nSearching 15')
    df_count = combine_df(df1=df_count, df2=df_15)
    print('\nSearching 16')
    df_count = combine_df(df1=df_count, df2=df_16)
    print('\nCombination successful')

    df_count = df_count.sort_values(by=['weight'], ascending=False, ignore_index=True)
    df_50 = df_count.iloc[0:50]
    df_50 = df_50.sort_values(by=['weight'], ascending=True, ignore_index=True)
    print('\nSorted results')

    df_to_csv(df=df_50, OUTPUT_FILE_NAME='hot50.csv')
    df_to_csv(df=df_count, OUTPUT_FILE_NAME='countdown.csv')

