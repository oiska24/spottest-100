# Spottest 100 #
![alt text](images/spottest-100.png)

## About ##
Create a custom Hottest 100 with your friends by combining your Spotify Wrapped (or other) playlists together in a countdown!

### System Design ###

Following a working prototype in python code, system design is now being carried out using the MagicGrid methodology. [View](/system-model/model-overview/README.md) the artifacts created during the process.

## Disclaimer ##
This program is inspired by, but has no association with, the Australian Broadcast Corporation national radio station [Triple J](https://www.abc.net.au/triplej).\
Apologies that you can't use this out of the box, a little bit of setup is involved to get you going. Instructions are based on a Linux machine.

## Pre-requisites ##
1. IDE or development environment with [Python 3.12.1](https://www.python.org/downloads/release/python-3121/) installed\
`sudo apt install python3.12`\
`sudo apt install python3.12-venv`\
`sudo apt install python3.12-dev`
2. Spotify account

## Setup ##


### Spotify developer account ###
1. Follow [these steps](https://developer.spotify.com/documentation/web-api/tutorials/getting-started), up to and including `Request an access token`.
2. Save your Client_ID and Client Secret for next steps.

### Setup code on your machine ###
1. Clone the repository:\
`git clone git@github.com:oiska24/spottest-100.git`
2. Create a new virtual environment:\
`python3.12 -m venv venv`
3. Activate the virtual environment:\
`source venv/bin/activate`
4. Install the project dependencies:\
`pip install -r requirements.txt`
5. Install the stubs:\
`source postactivate`
6. Create a .env with your Spotify developer credentials:\
`CLIENT_ID='...'`\
`CLIENT_SECRET='...'`

### Get playlists from friends ###
Get links from your friends to their playlist, ensure that they have set their playlist to public.

### Setup playlists and customise countdown generation ###
1. Fill out a CSV with the links that matches `data/sample_links.csv` and name it `data/links.csv`
2. Change the variable `COUNTDOWN_NUMBER` in `src/main.py` to match the number of songs you want in your final countdown playlist.
3. If you are not using Wrapped playlists, set the number of tracks in the playlists you are using with the `PLAYLIST_NUMBER_OF_TRACKS` in `src/spotify.py`. The weighting system currently doesn't allow comparing playlists of differing lengths.
4. By default, tracks are weighted so that each person's #1 song gets 100 points, and their #100 song gets 1 point. The Top 10 songs also receive an extra 10 points each in order to bring out songs that people truly like. This is how I found a good balance, but it can be changed to suit you. Edit the `BONUS` variables in `src/spotify.py` file to add extra weighting to people's top tracks. `BONUS_NUMBER_OF_TRACKS` changes the number of top tracks which get extra weighting, and `BONUS_WEIGHT` changes how much extra weighting is added to those tracks.
## Run code ##
1. Run the script `python3.12 src/main.py`
2. Access the results in `data/results/results.csv`, the `data/results/countdown.csv` file is ordered to end with your #1 song.


## Goals for the future ##
!!!\
Save countdown list back into Spotify as a playlist (requires user authentication, not just a dev account)\
!!\
Create an executable with a GUI to remove local setup\
!\
Create a webpage with cloud hosted back-end (one day)