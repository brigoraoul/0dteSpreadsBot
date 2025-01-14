from ib_insync import IB, Future, Index, util
from datetime import datetime, timedelta

def connect_to_ib(host='127.0.0.1', port=7497, client_id=1):
    """
    Connects to Interactive Brokers TWS API.
    Returns:
        IB: A connected IB instance.
    """
    ib = IB()
    try:
        ib.connect(host=host, port=port, clientId=client_id)
        print("Connection established to TWS API.")
        return ib
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def print_account_summary(ib):
    """
    Prints the account summary.
    
    Parameters:
        ib (IB): A connected IB instance.
    """
    if not ib:
        print("IB connection is not established. Cannot fetch account summary.")
        return
    
    try:
        account_summary = ib.accountSummary()
        print("Account Summary:")
        for item in account_summary:
            print(item)
    except Exception as e:
        print(f"Failed to retrieve account summary: {e}")

def download_historical_data(ib, duration='30 D', bar_size='5 mins'):
    """
    Downloads historical data for S&P 500 futures and the regular S&P 500 index.

    Parameters:
        ib (IB): A connected IB instance.
        duration (str): Duration of the data to retrieve (e.g., '30 D' for 30 days).
        bar_size (str): Bar size (e.g., '5 mins').

    Saves:
        CSV files for S&P 500 futures and index data.
    """
    if not ib:
        print("IB connection is not established. Cannot download historical data.")
        return

    # Define contracts for S&P 500 futures and regular S&P 500 index
    contracts = {
        "SP500_futures": Future(symbol='ES', exchange='GLOBEX', currency='USD'),
        "SP500_index": Index(symbol='SPX', exchange='CBOE', currency='USD')
    }
    
    end_date = datetime.now()

    for name, contract in contracts.items():
        try:
            ib.qualifyContracts(contract)
            bars = ib.reqHistoricalData(
                contract,
                endDateTime=end_date.strftime('%Y%m%d %H:%M:%S'),
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow='TRADES',
                useRTH=True  # Regular Trading Hours only
            )

            # convert to DataFrame
            df = util.df(bars)

            # save to csv
            filename = f"{name}_5min_last_month.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {name} data to {filename}")
        except Exception as e:
            print(f"Failed to download data for {name}: {e}")


if __name__ == "__main__":

    # connect to IB
    ib_connection = connect_to_ib()

    # download historical data
    download_historical_data(ib_connection)

    if ib_connection:
        ib_connection.disconnect()
