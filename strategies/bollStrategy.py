from indicators.Indicators import Indicators
from strategies.strategy import Strategy

def bollStrategy(df, i:int):
	''' If price is 2.5% below the Lower Bollinger Band, return True'''

	if not df.__contains__('low_boll'):
		Indicators.AddIndicator(df, indicator_name="lbb", col_name="low_boll", args=14)

	buy_price = 0.975 * df['low_boll'][i]
	if buy_price >= df['close'][i]:
		return min(buy_price, df['high'][i])

	return False