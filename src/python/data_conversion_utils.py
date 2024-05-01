import pandas as pd


def csv_to_df(filename, INPUT_DIR):  # Remove trailing whitespace
    file_path = "/".join([INPUT_DIR, filename + ".csv"])
    df = pd.read_csv(file_path)
    return df


def df_to_csv(df, OUTPUT_FILE_NAME, OUTPUT_DIR):
    file_path = "/".join([OUTPUT_DIR, OUTPUT_FILE_NAME])
    df.to_csv(file_path)
    print('\nData saved in', file_path)
