class StochRSIStrategy:
    def __init__(self, stoch_rsi_entry_threshold=0.2, stoch_rsi_exit_threshold=0.8):
        "This is the threshold below which you consider entering a Bull Put Spread position. "
        "The default value is 0.2, which signifies an oversold condition."
        self.stoch_rsi_entry_threshold = stoch_rsi_entry_threshold
        "This is the threshold above which you consider exiting the position. " 
        "The default value is 0.8, which signifies an overbought condition."
        self.stoch_rsi_exit_threshold = stoch_rsi_exit_threshold

    def generate_signals(self, data):
        signals = []

        # Iterate over the data bars and generate signals based on Stochastic RSI
        for _, bar in data.iterrows():
            if bar['stoch_RSI'] < self.stoch_rsi_entry_threshold:
                signals.append({'action': 'enter', 'bar': bar})  # Buy signal (bullish)

            elif bar['stoch_RSI'] > self.stoch_rsi_exit_threshold:
                signals.append({'action': 'exit', 'bar': bar})  # Exit signal (sell or close position)

        return signals
