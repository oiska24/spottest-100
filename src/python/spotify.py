from dotenv import load_dotenv
import os
import re
import requests
import pandas as pd
from data_conversion_utils import csv_to_df, df_to_csv
from config import PLAYLISTS_DIR, RESULTS_DIR, LINKS_DIR

PLAYLIST_NUMBER_OF_TRACKS = 100
BONUS_NUMBER_OF_TRACKS = 10
BONUS_WEIGHT = 10

# load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
BASE_URL = "https://api.spotify.com/v1"

# create array of weighting
WEIGHTS = list(range(PLAYLIST_NUMBER_OF_TRACKS, 0, -1))
RANK = list(range(1, PLAYLIST_NUMBER_OF_TRACKS + 1, 1))
# add column for each name in count with the rank value specified
for x in range(0, BONUS_NUMBER_OF_TRACKS):
    WEIGHTS[x] = WEIGHTS[x] + BONUS_WEIGHT


def get_token():
    global TOKEN
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url=url, data=data, headers=headers)
    print(response.status_code)  # TODO turn to logs
    TOKEN = response.json()['access_token']
    return None


def get_playlist(link):
    plid = get_playlist_uri_from_link(link)
    url = BASE_URL + "/playlists/%s/tracks" % (plid)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    response = requests.get(url=url, headers=headers)
    print(response.status_code)  # TODO turn to logs
    return response


def get_playlist_uri_from_link(playlist_link: str) -> str:
    """Get Spotify playlist URI from Spotify playlist link

    The URI is the bit after 'playlist' but before the '?'

    Example:
    get_playlist_uri_from_link(
        "https://open.spotify.com/playlist/6jAarBZaMmBLnSIeltPzkz?si=d42be5c6ec194bb9"
    )
    >>> "6jAarBZaMmBLnSIeltPzkz"

    """
    if (
        match := re.match(
            r"https://open.spotify.com/playlist/(.*)\?",
            playlist_link
        )
    ):
        return match.groups()[0]
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")


def df_from_uri(user, save_playlist_csv=False):
    # df_from_uri(links_df.iloc[n])  # to add one playlists as a csv
    # get list of tracks in a given playlist (note: max playlist length 100)
    link = user['link']
    # API call to get playlist info
    response = get_playlist(link=link)
    tracks = response.json()["items"]
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
        df.loc[j] = [name, artists, WEIGHTS[j], RANK[j]]
        # increment weight counter
        j = j + 1
    if save_playlist_csv is True:
        df_to_csv(
            df=df,
            OUTPUT_FILE_NAME=f'{user["name"]}' + '.csv',
            OUTPUT_DIR=PLAYLISTS_DIR
            )
    globals()[f'df_{user["name"]}'] = df


def save_countdown_to_spotify(playlist_name, playlist_description):
    url = BASE_URL + "/users/%s/playlists" % (CLIENT_ID)
    headers = {
        "Authorization": "Bearer " + TOKEN
    }
    data = {
        'name': playlist_name,
        'public': False,
        'collaborative': False,
        'description': playlist_description
    }
    response = requests.post(url=url, data=data, headers=headers)
    print(response.status_code)  # TODO turn to logs
    print(response.json())
    return None


def combine_data_from_links(save_playlist_csv=False):
    links_df = csv_to_df(filename="links", INPUT_DIR=LINKS_DIR)
    for i in range(0, (links_df.shape[0])):
        df_from_uri(
            user=links_df.iloc[i],
            save_playlist_csv=save_playlist_csv
        )
    combined_df = combine_all_dfs(links_df=links_df)
    df_to_csv(
        df=combined_df,
        OUTPUT_FILE_NAME='results.csv',
        OUTPUT_DIR=RESULTS_DIR
        )
    return combined_df


def combine_two_dfs(df1, df2):
    length = df1.shape[0]
    for j in range(0, df2.shape[0]):
        match = False
        for i in range(0, length):
            if df1.iloc[i]['track'] == df2.iloc[j]['track']:
                if df1.iloc[i]['artist'] == df2.iloc[j]['artist']:
                    match = True
                    df1.at[i, 'weight'] = [
                        df1.iloc[i]['weight'] + df2.iloc[j]['weight'] + 50
                    ]
                    df1.at[i, df2.columns[3]] = df2.iloc[j][df2.columns[3]]
                    print([df2.iloc[j]['track'], df2.iloc[j]['artist']])
                    print('match')
                    break
                print('track matched, artist didnt')
                print(
                    [
                        df2.iloc[j]['track'],
                        df2.iloc[j]['artist'],
                        df1.iloc[i]['artist']
                    ]
                )
        if match is False:
            new_track = pd.DataFrame(
                    [
                        [
                            df2.iloc[j]['track'],
                            df2.iloc[j]['artist'],
                            df2.iloc[j]['weight'],
                            df2.iloc[j][df2.columns[3]]
                        ]
                    ],
                    columns=['track', 'artist', 'weight', df2.columns[3]]
                )
            df1 = pd.concat([df1, new_track], ignore_index=True)
    return df1


def combine_all_dfs(links_df):
    combined_df = globals()[f'df_{links_df.iloc[0]["name"]}']
    for i in range(1, (links_df.shape[0])):
        print('\nSearching ' + links_df.iloc[i]["name"])
        combined_df = combine_two_dfs(
            df1=combined_df,
            df2=globals()[f'df_{links_df.iloc[i]["name"]}']
            )
    print('\nCombination successful')
    combined_df = combined_df.sort_values(
        by=['weight'],
        ascending=False,
        ignore_index=True
    )
    print('\nSorted results')
    return combined_df


def create_countdown(combined_df, countdown_number, save_playlist_csv=True):
    df_countdown = combined_df.iloc[0:countdown_number]
    df_countdown = df_countdown.sort_values(
        by=['weight'],
        ascending=True,
        ignore_index=True
    )
    if save_playlist_csv is True:
        df_to_csv(
            df=df_countdown,
            OUTPUT_FILE_NAME='countdown.csv',
            OUTPUT_DIR=RESULTS_DIR
        )
    return df_countdown
