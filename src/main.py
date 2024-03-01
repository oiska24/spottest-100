import spotify

COUNTDOWN_NUMBER = 50

if __name__ == '__main__':
    spotify.get_token()
    df_comb = spotify.combine_data_from_links(save_playlist_csv=True)
    df_countdown = spotify.create_countdown(
        combined_df=df_comb,
        countdown_number=COUNTDOWN_NUMBER,
        save_playlist_csv=True
    )
    spotify.save_countdown_to_spotify(
        playlist_name='Spottest 100',
        playlist_description='made via API'
    )
