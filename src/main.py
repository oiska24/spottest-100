# from spotify import authenticate_spotify
# from spotify import combine_data_from_links
# from spotify import create_countdown
# from spotify import save_countdown_to_spotify
import spotify

COUNTDOWN_NUMBER = 50

if __name__ == '__main__':
    token = spotify.get_token()
    link = "https://open.spotify.com/playlist/4msINp4cNYtKuAlLZAQowv?si=535858ec39c141be"
    # response = spotify.get_playlist(rk=link)

    # working code
    # authenticate_spotify()
    # df_comb = combine_data_from_links(save_playlist_csv=True)
    # df_countdown = create_countdown(
    #     df_comb,
    #     COUNTDOWN_NUMBER,
    #     save_playlist_csv=True
    # )

    # save_countdown_to_spotify() ## untested
