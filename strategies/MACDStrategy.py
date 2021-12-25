from indicators.Indicators import Indicators
from strategies.strategy import Strategy


def MACDStrategy(df,i:int):
    
    if  not df.__contains__('MACD') and not df.__contains__('signal_line') :
        
        Indicators.AddIndicator(df,indicator_name=MACDStrategy(df,"macd", "MACD", 12,26)
    pass