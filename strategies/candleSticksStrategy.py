from strategies.strategy import Strategy
from indicators.Indicators import Indicators

def candlestickStrategy(df, i:int):
    
   if (df["open"][i]-df["low"][i])/(df["close"][i]-df["open"][i])>3 and \
       (df["high"][i]-df["close"][i])<(df["close"][i]-df["open"][i]) :
      return True
   else :
      return False