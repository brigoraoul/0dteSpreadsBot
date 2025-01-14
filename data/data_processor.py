import pandas as pd
import ta

class TechnicalAnalysis:
    @staticmethod
    def calculate_rsi(data, period=14):
        df = pd.DataFrame(data)
        df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=period).rsi()
        return df
