
from abc import ABC, abstractmethod

import pandas as pd


class Indicators(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_dataframe(self,ohlc:pd.DataFrame):
        pass

    @abstractmethod
    def reconfigure(self):
        pass

    # def add_indicator(df, indicator_name, col_name, args):
    #     try:
    #             if indicator_name == "ichimoku": 
    #                 # this is a special case, because it will create more columns in the df
    #                 df = ComputeIchimokuCloud(df)
    #             else:
    #                 # remember here how we used to compute the other indicators inside 
    #                 # TradingModel: self.df['fast_sma'] = sma(self.df['close'].tolist(), 10)
    #                 df[col_name] = Indicators.INDICATORS_DICT[indicator_name](df['close'].tolist(), args)
    #     except Exception as e:
    #             print("\nException raised when trying to compute "+indicator_name)
    #             print(e)