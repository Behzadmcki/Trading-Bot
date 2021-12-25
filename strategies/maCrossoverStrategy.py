from indicators.Indicators import Indicators
from strategies.strategy import Strategy


def maCrossoverStrategy(df, i:int):

	''' If price is 10% below the Slow MA, return True'''

	if not df.__contains__('50_ema') and not df.__contains__('200_ema'):
		Indicators.AddIndicator(df, indicator_name="ema", col_name="50_ema", args=50)
		Indicators.AddIndicator(df, indicator_name="ema", col_name="200_ema", args=200)

	if i > 0 and df['50_ema'][i-1] <= df['200_ema'][i-1] and \
		df['50_ema'][i] > df['200_ema'][i]:
		return df['close'][i]

	return False