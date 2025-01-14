from ib_insync import IB

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

# Example usage
if __name__ == "__main__":
    # Connect to IB
    ib_connection = connect_to_ib()

    # Disconnect
    if ib_connection:
        ib_connection.disconnect()
