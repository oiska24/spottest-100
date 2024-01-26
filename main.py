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

# # specify csv files and directory
# OUTPUT_DIR = "data"
# File_Oscar = "oscar.csv"
# File_Cam = "cam.csv"
# File_Gaz = "gaz.csv"
# File_Jo = "jo.csv"
# File_Eve = "eve.csv"
# File_Bee = "bee.csv"
# File_Liana = "liana.csv"
# File_Bryce = "bryce.csv"
# File_Josh = "josh.csv"
# File_Wrethman = "wrethman.csv"
# File_Hannah = "hannah.csv"
# File_Lauren = "lauren.csv"

# # specify playlist links
# Link_Oscar = (
#     "https://open.spotify.com/playlist/4C8jHebuV1zh1iiLTj5347?si=479743a3b65d42ea"
# )
# Link_Cam = (
#     "https://open.spotify.com/playlist/6lJzWmXvTpqptTJQZBGtnC?si=05ae8b72b6ac4b7f"
# )
# Link_Gaz = (
#     "https://open.spotify.com/playlist/3GcRHW3RKGnnhPx4uSr0En?si=1125345ee6a04ff2"
# )
# Link_Jo = (
#     "https://open.spotify.com/playlist/2GXm4VE7aAKeOgM12qdecs?si=Ganfvk5XSN6o8b5UmcOYjw"
# )
# Link_Eve = (
#     "https://open.spotify.com/playlist/2dCHHxWbHkCKRh0tlqgBh5?si=z-2w0vcgQEyynP5e0dGV_g"
# )
# Link_Bee = (
#     "https://open.spotify.com/playlist/1diUHODVxe34w7TnGNZlKt?si=lORnxhOiRE2Ic_hCcM4pqA"
# )
# Link_Liana = (
#     "https://open.spotify.com/playlist/6h8XWgT8f0cVY8BDMJgpu3?si=DDdq4j9OSy-2xMpp4gbmkg"
# )
# Link_Bryce = (
#     "https://open.spotify.com/playlist/7LdMzuc8AtAcaP7W1BxX86?si=ec1c9774ddfc4647"
# )
# Link_Josh = (
#     "https://open.spotify.com/playlist/5DEzT3pOCx3Xy8B5obbSzG?si=c507370067864879"
# )
# Link_Wrethman = (
#     "https://open.spotify.com/playlist/4tc9hUbQ7Ewo3wqG8khWBx?si=hbSvX2wGSXOUawn0neq67A"
# )
# Link_Hannah = (
#     "https://open.spotify.com/playlist/7eqTQqrhlAMSvi3viTcLwR?si=adffe0bc187b4eb0"
# )
# Link_Lauren = (
#     "https://open.spotify.com/playlist/6C2ZK1hIKhRvGR2yIm7cWx?si=decd9ec70da94f4d"
# )

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

    # save_csvs_from_links(links_df) # to add all playlists as csvs
    # save_csv_from_uri(links_df.iloc[19]) # to add one playlists as a csv

    # create_dfs_from_links(links_df)
    df_oscar  = csv_to_df(links_df.iloc[0]["name"])
    df_cam = csv_to_df(links_df.iloc[1]["name"])
    df_gaz = csv_to_df(links_df.iloc[2]["name"])
    df_jo = csv_to_df(links_df.iloc[3]["name"])
    df_eve = csv_to_df(links_df.iloc[4]["name"])
    df_bee = csv_to_df(links_df.iloc[5]["name"])
    df_liana = csv_to_df(links_df.iloc[6]["name"])
    df_bryce = csv_to_df(links_df.iloc[7]["name"])
    df_josh = csv_to_df(links_df.iloc[8]["name"])
    df_wrethman = csv_to_df(links_df.iloc[9]["name"])
    df_hannah = csv_to_df(links_df.iloc[10]["name"])
    df_lauren = csv_to_df(links_df.iloc[11]["name"])
    df_samila = csv_to_df(links_df.iloc[12]["name"])
    df_billy = csv_to_df(links_df.iloc[13]["name"])
    df_ash = csv_to_df(links_df.iloc[14]["name"])
    df_jack = csv_to_df(links_df.iloc[15]["name"])
    df_sam = csv_to_df(links_df.iloc[16]["name"])
    df_jimbo = csv_to_df(links_df.iloc[17]["name"])
    df_eric = csv_to_df(links_df.iloc[18]["name"])
    df_kara = csv_to_df(links_df.iloc[19]["name"])

    df_count = df_gaz
    # print('\nSearching cam')
    # df_count = combine_df(df1=df_count, df2=df_cam)
    # print('\nSearching gaz')
    # df_count = combine_df(df1=df_count, df2=df_gaz)
    # print('\nSearching jo')
    # df_count = combine_df(df1=df_count, df2=df_jo)
    print('\nSearching bee')
    df_count = combine_df(df1=df_count, df2=df_bee)
    # print('\nSearching eve')
    # df_count = combine_df(df1=df_count, df2=df_eve)
    # print('\nSearching liana')
    # df_count = combine_df(df1=df_count, df2=df_liana)
    # print('\nSearching bryce')
    # df_count = combine_df(df1=df_count, df2=df_bryce)
    # print('\nSearching josh')
    # df_count = combine_df(df1=df_count, df2=df_josh)
    # print('\nSearching wrethman')
    # df_count = combine_df(df1=df_count, df2=df_wrethman)
    # print('\nSearching hannah')
    # df_count = combine_df(df1=df_count, df2=df_hannah)
    # print('\nSearching lauren')
    # df_count = combine_df(df1=df_count, df2=df_lauren)
    # print('\nSearching samila')
    # df_count = combine_df(df1=df_count, df2=df_samila)
    # print('\nSearching billy')
    # df_count = combine_df(df1=df_count, df2=df_billy)
    # print('\nSearching ash')
    # df_count = combine_df(df1=df_count, df2=df_ash)
    # print('\nSearching jack')
    # df_count = combine_df(df1=df_count, df2=df_jack)
    # print('\nSearching sam')
    # df_count = combine_df(df1=df_count, df2=df_sam)
    # print('\nSearching jimbo')
    # df_count = combine_df(df1=df_count, df2=df_jimbo)
    # print('\nSearching eric')
    # df_count = combine_df(df1=df_count, df2=df_eric)
    # print('\nSearching kara')
    # df_count = combine_df(df1=df_count, df2=df_kara)
    
    print('\nCombination successful')

    df_count = df_count.sort_values(by=['weight'], ascending=False, ignore_index=True)
    df_50 = df_count.iloc[0:50]
    df_50 = df_50.sort_values(by=['weight'], ascending=True, ignore_index=True)
    print('\nSorted results')

    df_to_csv(df=df_50, OUTPUT_FILE_NAME='hot50.csv')
    df_to_csv(df=df_count, OUTPUT_FILE_NAME='countdown.csv')