from indicators.Indicators import Indicators
from strategies.strategy import Strategy


def MACDStrategy(df,i:int):
    
    if  not df.__contains__('macd') and not df.__contains__('signal') :
        print("data frame does not have the macd ")
        Indicators.AddIndicator(df,indicator_name="macd",col_name=None, args=None)
    # print("computing macd strategy")
    # print(df["diffrence"].head())
    if i>20:
        if df["diffrence"][i]>0 and df["diffrence"][i-1]<0  :
            return df["close"][i]