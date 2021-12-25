from abc import ABC, abstractmethod
from re import template
from time import sleep
# from data import data
# from strategy import strategy
# from positionManger import positionManager
from finta import TA
from pandas.core import series
import plotly.graph_objs as go
import pandas as pd 
from plotly.offline import plot
#import pandas_ta as ta
from indicators.sma import SMA
from indicators.rsi import RSI

from plotly.subplots import make_subplots

from exchange_market import data
from exchange_market import coinex
import os


class Strategy(ABC):

    def __init__(self):
        self.__symbol = None  # data
        self.__strategy = None # strategy
        self.__position = None  # positionManager
        self.__moneyManager = None  # money_manager ???

    @abstractmethod
    def on_ohlc(self):
        pass

    @abstractmethod
    def on_ohlc_manage_opened_pos(self):
        pass

    @abstractmethod
    def on_tick(self):
        pass

    @abstractmethod
    def on_tick_manage_opened_pos(self):
        pass

class First(Strategy):

    def __init__(self):
        super().__init__()
        self.market1=coinex.Coinex()

        
    
    def on_ohlc(self):
        ohlc=self.market1.get_ohlcv("btcusdt",1000,"5min")
        
        return ohlc

    def on_tick(self):
        return super().on_tick()
    def on_ohlc_manage_opened_pos(self):
        return super().on_ohlc_manage_opened_pos()   
    def on_tick_manage_opened_pos(self):
        return super().on_tick_manage_opened_pos() 






if __name__ == "__main__":


    testStrategy=First()     
    ohlc=testStrategy.on_ohlc()
    # I dont know what the fuck is going on but these lines are needed ........
    ohlc.to_json("data.json")
    rootdir=os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(rootdir, 'data.json')
    ohlc_for_rsi = pd.read_json(data_file, orient=["time"]).set_index("time").tail(500)

    sma_10=SMA(10,"close")
    sma_20=SMA(20,"close")
    sma_50=SMA(50,"close")
    rsi=RSI(14,"close")

    sma_10_df=sma_10.get_dataframe(ohlc)
    sma_20_df=sma_20.get_dataframe(ohlc)
    sma_50_df=sma_50.get_dataframe(ohlc)
    # print("\n")
    # print(type(rsi_df))
    kir = TA.RSI(ohlc_for_rsi, 14).to_frame()
    print("\n")
    print(kir.columns)

    



    
    fig = make_subplots(rows=2, cols=1)
    fig.append_trace(go.Candlestick(
        x = ohlc['time'],
        open = ohlc['open'],
        close = ohlc['close'],
        high = ohlc['high'],
        low = ohlc['low'],
        name = "Candlesticks"),row=1,col=1)
    fig.append_trace(go.Scatter(
        x = ohlc['time'],
        y = sma_10_df['10 period SMA'],
        name = "Fast SMA",
        line = dict(color = ('rgba(250,0,0, 50)'))),row=1,col=1)
    fig.append_trace(go.Scatter(
        x = ohlc['time'],
        y = sma_20_df['20 period SMA'],
        name = "normal SMA",
        line = dict(color = ('rgba(102, 100, 150, 50)'))),row=1,col=1)
    fig.append_trace(go.Scatter(
        x = ohlc['time'],
        y = sma_50_df['50 period SMA'],
        name = "slow SMA",
        line = dict(color = ('rgba(102, 207, 255, 50)'))),row=1,col=1) 
    fig.append_trace(go.Scatter(
        x = ohlc["time"],
        y = kir["14 period RSI"],
        name = "RSI",
        line = dict(color = ('#FFFF00'))),row=2,col=1)   

    fig.add_hline(y=30,line_dash="dash",line_color="white",row=2,col=1)
    fig.add_hline(y=70,line_dash="dash",line_color="white",row=2,col=1)



    fig.update_layout(xaxis_rangeslider_visible=False,template="plotly_dark")
    plot(fig, filename='./'+"hey"+'.html')