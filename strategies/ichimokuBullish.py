from strategies.strategy import Strategy
from indicators.Indicators import Indicators

def ichimokuBullish(df, i:int):
	
	''' If price is above the Cloud formed by the Senkou Span A and B, 
	and it moves above Tenkansen (from below), that is a buy signal.'''

	if not df.__contains__('tenkansen') or not df.__contains__('kijunsen') or \
		not df.__contains__('senkou_a') or not df.__contains__('senkou_b'):
		Indicators.AddIndicator(df, indicator_name="ichimoku", col_name=None, args=None)

	if i - 1 > 0 and i < len(df):
		if df['senkou_a'][i] is not None and df['senkou_b'][i] is not None:
			if df['tenkansen'][i] is not None and df['tenkansen'][i-1] is not None:
				if df['close'][i-1] < df['tenkansen'][i-1] and \
					df['close'][i] > df['tenkansen'][i] and \
					df['close'][i] > df['senkou_a'][i] and \
					df['close'][i] > df['senkou_b'][i]:
						return df['close'][i]
	
	return False