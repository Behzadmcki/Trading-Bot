from StrategyEvaluator import StrategyEvaluator
from strategies.maCrossoverStrategy import *
from strategies.maStrategy import *
from strategies.ichimokuBullish import *
from strategies.bollStrategy import *
from strategies.rsiStrategy import *
from strategies.testStrategy import *
from strategies.MACDStrategy import *
from exchange_market.coinex import Coinex
from TradingModel import TradingModel
import json
from decimal import Decimal, getcontext

strategies_dict = dict(
	ma_crossover = maCrossoverStrategy,
	ma_simple = maStrategy,
	bollinger_simple = bollStrategy,
	ichimoku_bullish = ichimokuBullish,
	rsi_strategy=rsiStrategy,
	test_strategy=testStrategy,
	macd_strategy=MACDStrategy


)

# Now, We will put everything together. Continuing with our command line interface, we will allow ourselves
# to backtest strategies, evaluate them (see what coins have those strategies fulfilled right now), and if
# any coins are eligible, we will plot & backtest that strategy on that particular coin, and if we are 
# happy with the results, we can place an order. 

# We will update this function a little bit, to make it more customizable
def BacktestStrategies(symbols=[], interval='4hour', plot=False, strategy_evaluators=[], 
options = dict(starting_balance=100, initial_profits = 1.03, initial_stop_loss = 0.99, 
incremental_profits = 1.006, incremental_stop_loss = 0.998)):
	coins_tested = 0
	trade_value = options['starting_balance']
	for symbol in symbols:
		print(symbol)
		model = TradingModel(symbol=symbol, timeframe=interval, helkin_ashi=True)
		for evaluator in strategy_evaluators:
			resulting_balance = evaluator.backtest(
				model,
				starting_balance = options['starting_balance'],
				initial_profits = options['initial_profits'],
				initial_stop_loss = options['initial_stop_loss'],
				incremental_profits = options['incremental_profits'],
				incremental_stop_loss = options['incremental_stop_loss'],
			)

			if resulting_balance != trade_value:
				print(evaluator.strategy.__name__ 
				+ ": starting balance: " + str(trade_value)
				+ ": resulting balance: " + str(round(resulting_balance, 2)))

				if plot:
					model.plotData(
						buy_signals = evaluator.results[model.symbol]['buy_times'],
						sell_signals = evaluator.results[model.symbol]['sell_times'],
						plot_title = evaluator.strategy.__name__+" on "+model.symbol)
					
				evaluator.profits_list.append(resulting_balance - trade_value)
				evaluator.updateResult(trade_value, resulting_balance)
			
			coins_tested = coins_tested + 1

	for evaluator in strategy_evaluators:
		print("")
		evaluator.printResults()

# Now, We will write the function that checks the current market conditions 
# & allows us to place orders if the conditions are good

# But First, We need to define the messages that the user will see:
strategy_matched_symbol = "\nStragey Matched Symbol! \
	\nType 'b' then ENTER to backtest the strategy on this symbol & see the plot \
	\nType 'p' then ENTER if you want to Place an Order \
	\nTyping anything else or pressing ENTER directly will skip placing an order this time.\n"

ask_place_order = "\nType 'p' then ENTER if you want to Place an Order \
	\nTyping anything else or pressing ENTER directly will skip placing an order this time.\n"

def EvaluateStrategies(symbols=[], strategy_evaluators=[], interval='1hour', 
options = dict(starting_balance=100, initial_profits = 1.008, initial_stop_loss = 0.996, 
incremental_profits = 1.004, incremental_stop_loss = 0.998)):
	for symbol in symbols:
		print(symbol)
		model = TradingModel(symbol=symbol, timeframe=interval,helkin_ashi=True)
		for evaluator in strategy_evaluators:
			if evaluator.evaluate(model):
				print("\n"+evaluator.strategy.__name__+" matched on "+symbol)
				print(strategy_matched_symbol)
				answer = input()

				if answer == 'b':
					resulting_balance = evaluator.backtest(
						model,
						starting_balance=options['starting_balance'],
						initial_profits = options['initial_profits'],
						initial_stop_loss = options['initial_stop_loss'],
						incremental_profits = options['incremental_profits'],
						incremental_stop_loss = options['incremental_stop_loss'],
					)
					model.plotData(
						buy_signals = evaluator.results[model.symbol]['buy_times'],
						sell_signals = evaluator.results[model.symbol]['sell_times'],
						plot_title=evaluator.strategy.__name__+" matched on "+symbol
					)
					print(evaluator.results[model.symbol])
					print(ask_place_order)
					answer = input()
				if answer == 'p':
					print("\nPlacing Buy Order. ")

					# We need to update the PlaceOrder function - we don't know what symbol we will be buying beforehand,
					# but let's say that we have received a symbol on coin ABCETH, where 1 ABC = 0.0034 ETH. 
					# Binance only allows us to make orders ABOVE 0.01 ETH, so we need to buy at least 3 ABC.
					# However, if we received a symbol on XYZETH, and say 1 XYZ = 3 ETH, maybe we only want to buy 0.05 XYZ.
					# Therfore, we need to specify the amount we need to buy in terms of QUOTE ASSET (ETH), not base asset.
					# # We are changing the PlaceOrder function to reflect that. 
					order_result = model.exchange.PlaceOrder(model.symbol, "BUY", "MARKET", quantity=0.02, test=False)
					if "code" in order_result:
						print("\nERROR.")
						print(order_result)
					else:
						print("\nSUCCESS.")
						print(order_result)

# Now, we're almost ready to start the bot. Let's add our third strategy and some commands.
opening_text = "\nWelcome to Tudor's Crypto Trading Bot. \n \
	Press 'b' (ENTER) to backtest all strategies \n \
	Press 'e' (ENTER) to execute the strategies on all coins \n \
	Press 'q' (ENTER) to quit. "

def Main():

	exchange = Coinex()
	symbols = exchange.market_list(quoteAssets=["BTCUSDT"])

	strategy_evaluators = [
		# StrategyEvaluator(strategy_function=strategies_dict["ma_simple"]),
		# StrategyEvaluator(strategy_function=strategies_dict["bollinger_simple"]),
		# StrategyEvaluator(strategy_function=strategies_dict["ichimoku_bullish"]),
		# StrategyEvaluator(strategy_function=strategies_dict['ma_crossover']),
		# StrategyEvaluator(strategy_function=strategies_dict['rsi_strategy']),
		StrategyEvaluator(strategy_function=strategies_dict['test_strategy']),
		# StrategyEvaluator(strategy_function=strategies_dict['macd_strategy'])
	]

	print(opening_text)
	
	answer = input()
	while answer not in ['b', 'e', 'q']:
		print(opening_text)
		answer = input()

	if answer == 'e':
		EvaluateStrategies(symbols=symbols, interval='1hour', strategy_evaluators=strategy_evaluators)
	if answer == 'b':
		BacktestStrategies(symbols=symbols, interval='30min', plot=True, strategy_evaluators=strategy_evaluators)
	if answer == 'q':
		print("\nBYE!\n")

if __name__ == '__main__':
	Main()
