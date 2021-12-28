from strategies.strategy import Strategy
from indicators.Indicators import Indicators

def testStrategy(df, i:int):

    if not df.__contains__('30_ema') and not df.__contains__('10_ema'):
        Indicators.AddIndicator(df, indicator_name="ema", col_name="30_ema", args=30)
        Indicators.AddIndicator(df, indicator_name="ema", col_name="10_ema", args=10)
    if i >30 :
        if (df["10_ema"][i-3]<df["30_ema"][i-3] and df["10_ema"][i-2]>df["30_ema"][i-2]) or (df["10_ema"][i-2]<df["30_ema"][i-2] and df["10_ema"][i-1]>df["30_ema"][i-1]) :
            if (df["HA_Open"][i]-df["HA_Low"][i])<1 :
                    return df["close"][i]
        else : return False

    
