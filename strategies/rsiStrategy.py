from strategies.strategy import Strategy
from indicators.Indicators import Indicators

def rsiStrategy(df ,i:int):
    if not df.__contains__('rsi'):
        Indicators.AddIndicator(df, indicator_name="rsi", col_name="rsi", args=14)
        Indicators.AddIndicator(df, indicator_name="ema", col_name="20_ema", args=24)
    
    buy_price = 0.975 * df['low_boll'][i]
    if buy_price >= df['close'][i]:
        if df["rsi"][i]<30:
            return min(buy_price, df['high'][i])
    else:
        return False        
