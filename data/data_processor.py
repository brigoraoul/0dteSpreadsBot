import pandas as pd
import ta

class TechnicalAnalysis:
    @staticmethod
    def get_all_indicators(data):
        data = TechnicalAnalysis.calculate_rsi(data)
        data = TechnicalAnalysis.calculate_stochastic_rsi(data)
        return data
    
    @staticmethod
    def calculate_rsi(data, period=14):
        df = pd.DataFrame(data)
        df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=period).rsi()
        return df

    @staticmethod
    def calculate_stochastic_rsi(data, rsi_period=14, stoch_period=14, smooth_period=3):
        df = pd.DataFrame(data)
        rsi = ta.momentum.RSIIndicator(df['close'], window=rsi_period).rsi()
        stoch_rsi = ta.momentum.StochRSIIndicator(rsi, window=stoch_period).stochrsi()
        df['stoch_RSI'] = stoch_rsi
        return df