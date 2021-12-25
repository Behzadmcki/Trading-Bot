from indicators.indicatorsAbstractClass import Indicators
from finta import TA
import pandas as pd 

class RSI(Indicators):


    def __init__(self,period:int,column:str) -> None:
        super().__init__()
        self.period=period
        self.column=column
        
    def get_dataframe(self,ohlc:pd.DataFrame):
        
        delta = ohlc[self.column].diff(1)

        ## positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # EMAs of ups and downs
        _gain = up.ewm(alpha=1.0 / self.period).mean()
        _loss = down.abs().ewm(alpha=1.0 / self.period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="{0} period RSI".format(self.period))
        # rsi_series=TA.RSI(ohlc,self.period,self.column)
        # rsi_dataframe=rsi_series.to_frame()

        # return rsi_dataframe

    def reconfigure(self,period:int,column:str):
        self.period=period
        self.column=column