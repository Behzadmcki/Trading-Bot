from indicators.Indicators import Indicators
from strategies.strategy import Strategy


def MACDStrategy(df,i:int):
    
    if  not df.__contains__('macd') and not df.__contains__('signal') :
        print("data frame does not have the macd ")
        Indicators.AddIndicator(df,indicator_name="macd",col_name=None, args=None)
    #     Indicators.AddIndicator(df, indicator_name="ema", col_name="20_ema", args=24)
    #     Indicators.AddIndicator(df, indicator_name="ema", col_name="12_ema", args=12)
    if not df.__contains__('tenkansen') or not df.__contains__('kijunsen') or \
        not df.__contains__('senkou_a') or not df.__contains__('senkou_b'):
            Indicators.AddIndicator(df, indicator_name="ichimoku", col_name=None, args=None)


    
    if i - 1 > 0 and i < len(df):
        if df['senkou_a'][i] is not None and df['senkou_b'][i] is not None:
            if df['tenkansen'][i] is not None and df['tenkansen'][i-1] is not None:
                if df["kijunsen"][i]<df['tenkansen'][i] :
                # base_line should be under the conversion line
                    if (df["close"][i]>df['senkou_a'][i]):
                    # candle close above the cloud
                        if (df["senkou_a"][i]>df['senkou_b'][i]):
                        # the cloud must be green 
                            if  df["senkou_a"][i]<df['chikouspan'][i]:
                            # lagging span must be over the cloud 
                                if df["macd"][i]>df["signal"][i]:
                                    return df["close"][i]
            else : return False    


                            # if i>20:
    #     # if df["diffrence"][i]>0 and df["diffrence"][i-1]<0  :
    #     #     return df["close"][i]
    #     if df["12_ema"][i-1]<df["20_ema"][i-1] and df["12_ema"][i]>df["20_ema"][i]:
    #         return df["close"][i] 

    
    