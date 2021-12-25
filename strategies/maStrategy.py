from indicators.Indicators import Indicators
from strategies.strategy import Strategy




def maStrategy(df, i:int):
	''' If price is 10% below the Slow MA, return True'''

	if not df.__contains__('slow_sma'):
		Indicators.AddIndicator(df, indicator_name="sma", col_name="slow_sma", args=30)

	buy_price = 0.96 * df['slow_sma'][i]
	if buy_price >= df['close'][i]:
		return min(buy_price, df['high'][i])

	return False