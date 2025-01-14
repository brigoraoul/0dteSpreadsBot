import os
import pandas as pd
from data.data_fetcher import IBClient

def data_present(file_name):
    folder_path = "data"
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        return False

    return file_name in files

def main():

    # if not historical data file exists, fetch data from tws api using data fetcher
    if not data_present("SP500_index_5min_last_month.csv"):
        ib_client = IBClient()
        ib_client.download_historical_data()
        ib_client.disconnect()
    
    df = pd.read_csv("data/SP500_index_5min_last_month.csv")
    print(df)
    

if __name__ == "__main__":
    main()