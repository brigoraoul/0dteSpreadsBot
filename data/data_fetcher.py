from ib_insync import IB, Future, Index, util
from datetime import datetime

class IBClient:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        """
        Initializes the IBClient and connects to Interactive Brokers TWS API.
        """
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connect()

    def connect(self):
        """
        Connects to the TWS API.
        """
        try:
            self.ib.connect(host=self.host, port=self.port, clientId=self.client_id)
            print("Connection established to TWS API.")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.ib = None

    def disconnect(self):
        """
        Disconnects from the TWS API.
        """
        if self.ib:
            self.ib.disconnect()
            print("Disconnected from TWS API.")

    def print_account_summary(self):
        """
        Prints the account summary.
        """
        if not self.ib:
            print("IB connection is not established. Cannot fetch account summary.")
            return

        try:
            account_summary = self.ib.accountSummary()
            print("Account Summary:")
            for item in account_summary:
                print(item)
        except Exception as e:
            print(f"Failed to retrieve account summary: {e}")

    def download_historical_data(self, duration='30 D', bar_size='5 mins'):
        """
        Downloads historical data for S&P 500 futures and the regular S&P 500 index.
        Saves data to CSV files for S&P 500 futures and index data.
        """
        if not self.ib:
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
                self.ib.qualifyContracts(contract)
                bars = self.ib.reqHistoricalData(
                    contract,
                    endDateTime=end_date.strftime('%Y%m%d %H:%M:%S'),
                    durationStr=duration,
                    barSizeSetting=bar_size,
                    whatToShow='TRADES',
                    useRTH=True  # Regular Trading Hours only
                )

                # Convert to DataFrame
                df = util.df(bars)

                # Save to CSV
                filename = f"{name}_5min_last_month.csv"
                df.to_csv(filename, index=False)
                print(f"Saved {name} data to {filename}")
            except Exception as e:
                print(f"Failed to download data for {name}: {e}")