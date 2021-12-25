from indicators.indicatorsAbstractClass import Indicators
from finta import TA


class BBands(Indicators):


    def __init__(self,round:int) -> None:
        super().__init__()
        self.round=round

        
    def get_dataframe(self,ohlc):

        bband_dataframe = TA.BBANDS(ohlc).round(decimals=self.round) 

        return bband_dataframe

    def reconfigure(self):
        self.round=round
        