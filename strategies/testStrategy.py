from strategies.strategy import Strategy
from indicators.Indicators import Indicators

def testStrategy(df, i:int):
    Bullish_num=0
    Bearish_num=0
    range_num=0
    confermation=0
    if not df.__contains__('20_ema') :
            Indicators.AddIndicator(df, indicator_name="ema", col_name="20_ema", args=20)
    if not df.__contains__('rsi'):
            Indicators.AddIndicator(df, indicator_name="rsi", col_name="rsi", args=14)
    if not df.__contains__('low_boll'):        
            Indicators.AddIndicator(df, indicator_name="lbb", col_name="low_boll", args=14)
    if not df.__contains__('tenkansen') or not df.__contains__('kijunsen') or \
        not df.__contains__('senkou_a') or not df.__contains__('senkou_b'):
		    Indicators.AddIndicator(df, indicator_name="ichimoku", col_name=None, args=None)
    if not df.__contains__('50_ema') and not df.__contains__('200_ema'):
	    Indicators.AddIndicator(df, indicator_name="ema", col_name="50_ema", args=50)
	    Indicators.AddIndicator(df, indicator_name="ema", col_name="200_ema", args=200)        
    if i > 20:
        for j in range(20):
            if  df["20_ema"][i-j]>df["close"][i-j] and df["20_ema"][i-j]>df["open"][i-j]:
                Bullish_num=Bullish_num+1
            elif df["20_ema"][i-j]<=df["close"][i-j] and df["20_ema"][i-j]<=df["open"][i-j]:
                Bearish_num= Bearish_num+1
            else:
                range_num=range_num+1
        if Bearish_num >15 :
            trend="bearish_trend"
        elif Bullish_num>15:
            trend="bullish_trend"
        else : trend="None"    
        
        if trend == "bullish_trend":
            if df["20_ema"][i]*0.98<df["close"][i]or df["20_ema"][i]*1.02>df["close"][i]:
                confermation=confermation+1

        elif trend == "None":
            if df["20_ema"][i]<df["close"][i] and df["20_ema"][i]>df["open"][i]:
                 confermation=confermation+1
    buy_price = 0.975 * df['low_boll'][i]
    if buy_price >= df['close'][i]:
        if df["rsi"][i]<30:
            confermation=confermation+1
    if i - 1 > 0 and i < len(df):
	    if df['senkou_a'][i] is not None and df['senkou_b'][i] is not None:
			    if df['tenkansen'][i] is not None and df['tenkansen'][i-1] is not None:
				    if df['close'][i-1] < df['tenkansen'][i-1] and \
					df['close'][i] > df['tenkansen'][i] and \
					df['close'][i] > df['senkou_a'][i] and \
					df['close'][i] > df['senkou_b'][i]:
					    confermation=confermation+1	   
    if i > 0 and df['50_ema'][i-1] <= df['200_ema'][i-1] and \
    	df['50_ema'][i] > df['200_ema'][i]:
            confermation=confermation+1	   

    if confermation>=2 :
        return df["close"][i]
    else :
        return False                
        
    
