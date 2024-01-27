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
LINKS_DIR = "data"
RESULTS_DIR = "data/results"
PLAYLISTS_DIR = "data/results/individual_playlists"
COUNTDOWN_NUMBER = 50

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


def df_from_uri(user, save_playlist_csv=False):
    # df_from_uri(links_df.iloc[n])  # to add one playlists as a csv
    # get uri from https link
    playlist_uri = get_playlist_uri_from_link(user["link"])
    # get list of tracks in a given playlist (note: max playlist length 100)
    tracks = session.playlist_tracks(playlist_uri)["items"]
    # create empty dataframe
    df = pd.DataFrame(columns=['track', 'artist', 'weight', user['name']])
    # start weight counter
    j = 0
    # extract name and artist
    for track in tracks:
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )
        # write to df
        df.loc[j] = [name, artists, weights[j], rank[j]]
        # increment weight counter
        j = j + 1
    if save_playlist_csv is True:
        df_to_csv(df=df, OUTPUT_FILE_NAME=f'{user["name"]}' + '.csv', OUTPUT_DIR=PLAYLISTS_DIR)
    globals()[f'df_{user["name"]}'] = df


def create_dfs_from_links(links_df, save_playlist_csv):
    for i in range(0, (links_df.shape[0])):
        df_from_uri(links_df.iloc[i], save_playlist_csv=save_playlist_csv)


def csv_to_df(filename, INPUT_DIR):  
    file_path = "/".join([INPUT_DIR, filename + ".csv"])
    df = pd.read_csv(file_path)
    return df


def df_to_csv(df, OUTPUT_FILE_NAME, OUTPUT_DIR):   
    file_path = "/".join([OUTPUT_DIR, OUTPUT_FILE_NAME])
    df.to_csv(file_path)
    print('\nData saved in', file_path)


def combine_two_dfs(df1, df2):
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
        if match is False:
            new_track = pd.DataFrame([[df2.iloc[j]['track'], df2.iloc[j]['artist'], df2.iloc[j]['weight'], df2.iloc[j][df2.columns[3]]]], columns=['track', 'artist', 'weight', df2.columns[3]])
            df1 = pd.concat([df1, new_track], ignore_index=True)
    return df1


def combine_all_dfs(links_df):
    df_comb = globals()[f'df_{links_df.iloc[0]["name"]}']
    for i in range(1, (links_df.shape[0])):
        print('\nSearching ' + links_df.iloc[i]["name"])
        df_comb = combine_two_dfs(df1=df_comb, df2=globals()[f'df_{links_df.iloc[i]["name"]}'])
    print('\nCombination successful')
    df_comb = df_comb.sort_values(by=['weight'], ascending=False, ignore_index=True)
    print('\nSorted results')
    return df_comb


def countdown(df_comb, COUNTDOWN_NUMBER):
    df_countdown = df_comb.iloc[0:COUNTDOWN_NUMBER]
    df_countdown = df_countdown.sort_values(by=['weight'], ascending=True, ignore_index=True)
    return df_countdown


if __name__ == "__main__":
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET  # authenticate
    )   
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # create spotify session object
    links_df = csv_to_df(filename="links", INPUT_DIR=LINKS_DIR)  # convert links csv to df
    create_dfs_from_links(links_df=links_df, save_playlist_csv=True)  # add all playlists as dataframes
    df_comb = combine_all_dfs(links_df=links_df)  # combine each df into one and sort by weight
    df_to_csv(df=df_comb, OUTPUT_FILE_NAME='results.csv', OUTPUT_DIR=RESULTS_DIR)  # save results to csv
    df_countdown = countdown(df_comb, COUNTDOWN_NUMBER)  # create countdown list of top x songs
    df_to_csv(df=df_countdown, OUTPUT_FILE_NAME='countdown.csv', OUTPUT_DIR=RESULTS_DIR)  # save countdown to csv
