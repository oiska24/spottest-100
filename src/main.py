from spotify import authenticate_spotify
from spotify import combine_data_from_links
from spotify import create_countdown

COUNTDOWN_NUMBER = 50

if __name__ == "__main__":
    authenticate_spotify()
    df_comb = combine_data_from_links(save_playlist_csv=True)
    df_countdown = create_countdown(
        df_comb,
        COUNTDOWN_NUMBER,
        save_playlist_csv=True
    )
