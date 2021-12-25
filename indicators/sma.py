from indicators.indicatorsAbstractClass import Indicators
from finta import TA
import pandas as pd 

class SMA(Indicators):


    def __init__(self,period:int,column:str) -> None:
        super().__init__()
        self.period=period
        self.column=column
        
    def get_dataframe(self,ohlc):

        sam_series = TA.SMA(ohlc,self.period,self.column)
        # sma_dataframe=pd.DataFrame()
        sma_dataframe=sam_series.to_frame()

        return sma_dataframe

    def reconfigure(self,period:int,column:str):
        self.period=period
        self.column=column