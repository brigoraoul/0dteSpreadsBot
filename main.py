import os
import json
import pandas as pd
from data.data_fetcher import IBClient
from data.data_processor import TechnicalAnalysis
from strategies.stoch_rsi_strategy import StochRSIStrategy

def data_present(file_name):
    folder_path = "data"
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        return False

    return file_name in files

def load_config(path):
        """
        Loads the configuration file.
        """
        try:
            with open(path, 'r') as file:
                config = json.load(file)
            print("Configuration loaded successfully.")
            return config
        except Exception as e:
            print(f"Failed to load configuration: {e}")
            return None

def main():

    config = load_config('config/config.json')

    # if not historical data file exists, fetch data from tws api using data fetcher
    if not data_present("SP500_index_5min_last_month.csv"):
        ib_client = IBClient(config)
        ib_client.download_historical_data()
        ib_client.disconnect()
    
    # read data from csv to pandas dataframe
    df = pd.read_csv("data/SP500_index_5min_last_month.csv")
    print(df)

    df_with_indicators = TechnicalAnalysis.get_all_indicators(df)
    print(df)   

    strategy = StochRSIStrategy()
    signals = strategy.generate_signals(df_with_indicators)
    print(signals)

if __name__ == "__main__":
    main()