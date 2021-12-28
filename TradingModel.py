import pandas as pd
import requests
import json

import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

from exchange_market.coinex import Coinex 

import datetime
import time



class TradingModel:
	
	# We can now remove the code where we're computing the indicators from this class,
	# As we will be computing them in the Strategies class (on a per-need basis)

	def __init__(self, symbol, timeframe:str='4hour',helkin_ashi=False):
		self.symbol = symbol
		self.timeframe = timeframe
		self.exchange = Coinex()
		self.helkinAshi_chart=helkin_ashi
		if helkin_ashi==True:
			self.df=self.exchange.helkin_ashi(symbol, timeframe, 500)
		else:
			self.df = self.exchange.get_ohlcv(symbol,timeframe,500)
			
		self.last_price = self.df['close'][len(self.df['close'])-1]


	# We'll look directly in the dataframe to see what indicators we're plotting

	def plotData(self, buy_signals = False, sell_signals = False, plot_title:str="",
	indicators=[
		dict(col_name="fast_ema", color="indianred", name="FAST EMA"), 
		dict(col_name="50_ema", color="indianred", name="50 EMA"), 
		dict(col_name="200_ema", color="indianred", name="200 EMA")]):
		df = self.df
		df["actual_time"] = pd.to_datetime(df['time'],unit="s")


		# plot candlestick chart
		fig = make_subplots(rows=2, cols=1)
		
		fig.append_trace(go.Candlestick(
        x = df["actual_time"],
        open = df['open'],
        close = df['close'],
        high = df['high'],
        low = df['low'],
        name = "Candlesticks"),row=1,col=1)


		

		if df.__contains__('fast_sma'):
			
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['fast_sma'],
				name = "Fast SMA",
				line = dict(color = ('rgba(102, 207, 255, 50)'))),row=1,col=1)


		if df.__contains__('slow_sma'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['slow_sma'],
				name = "Slow SMA",
				line = dict(color = ('rgba(255, 207, 102, 50)'))),row=1,col=1)


		if df.__contains__('20_ema'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['20_ema'],
				name = "20_ema",
				line = dict(color = ('rgba(255, 207, 102, 50)'))),row=1,col=1)	
		if df.__contains__('30_ema'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['30_ema'],
				name = "30_ema",
				line = dict(color = ('rgba(255, 0, 102, 50)'))),row=1,col=1)
		if df.__contains__('10_ema'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['10_ema'],
				name = "10_ema",
				line = dict(color = ('rgba(255, 207, 0, 50)'))),row=1,col=1)								

		if df.__contains__('12_ema'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['12_ema'],
				name = "12_ema",
				line = dict(color = ('#5F9EA0'))),row=1,col=1)		


		if df.__contains__('low_boll'):
			 fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['low_boll'],
				name = "Lower Bollinger Band",
				line = dict(color = ('rgba(255, 102, 207, 50)'))),row=1,col=1)


		# Now, Let's also plot the Ichimoku Indicators

		if df.__contains__('tenkansen'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['tenkansen'],
				name = "Tenkansen",
				line = dict(color = ('rgba(40, 40, 141, 100)'))),row=1,col=1)
	
		
		if df.__contains__('kijunsen'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['kijunsen'],
				name = "Kijunsen",
				line = dict(color = ('rgba(140, 40, 40, 100)'))),row=1,col=1)


		if df.__contains__('senkou_a'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['senkou_a'],
				name = "Senkou A",
				line = dict(color = ('rgba(160, 240, 160, 100)'))),row=1,col=1)

	
		# As you saw in the chart earlier, the portion between Senkou A and B
		# is filled, either with red or with green. Here, We'll only be using red
		# I haven't found a proper way to change the colors of the fill based on
		# who is on top (Senkou A or B). If you have a way, please put it into the
		# comments, or bettew yet, write it in the code on github (make a pull request)!!

		if df.__contains__('senkou_b'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['senkou_b'],
				name = "Senkou B",
				fill = "tonexty",
				line = dict(color = ('rgba(240, 160, 160, 50)'))),row=1,col=1)
				
		if df.__contains__('chikouspan'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['chikouspan'],
				name = "Chikouspan",
				line = dict(color = ('#00FFFF'))),row=1,col=1)

		
		if df.__contains__('rsi'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['rsi'],
				name = "rsi",
				line = dict(color = ('rgba(240, 160, 160, 50)'))),row=2,col=1)
		
		if df.__contains__('macd'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['macd'],
				name = "macd",
				line = dict(color = ('rgba(240, 0, 160, 50)'))),row=2,col=1)
		if df.__contains__('signal'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['signal'],
				name = "signal",
				line = dict(color = ('rgba(240, 160, 0, 50)'))),row=2,col=1)
		if df.__contains__('diffrence'):
			fig.append_trace(go.Scatter(
				x = df["actual_time"],
				y = df['diffrence'],
				name = "diffrence",
				line = dict(color = ('rgba(0, 160, 160, 50)'))),row=2,col=1)


		if buy_signals:
			fig.append_trace(go.Scatter(
					x = [item[0] for item in buy_signals],
					y = [item[1] for item in buy_signals],
					name = "Buy Signals",
					mode = "markers",
					marker_size = 10,fillcolor='#008000'
				),row=1,col=1)

		if sell_signals:
			fig.append_trace(go.Scatter(
				x = [item[0] for item in sell_signals],
				y = [item[1] for item in sell_signals],
				name = "Sell Signals",
				mode = "markers",
				marker_size = 10,fillcolor='#FF7F50'
			),row=1,col=1)
		if df.__contains__('rsi'):
			fig.add_hline(y=30,line_dash="dash",line_color="white",row=2,col=1)
			fig.add_hline(y=70,line_dash="dash",line_color="white",row=2,col=1)	
		elif df.__contains__('macd'):
			fig.add_hline(y=10,line_dash="dash",line_color="white",row=2,col=1)
			fig.add_hline(y=-10,line_dash="dash",line_color="white",row=2,col=1)		


		if self.helkinAshi_chart==True: 
			fig2 = make_subplots(rows=1, cols=1)
			fig2.append_trace(go.Candlestick(
				x =self.df['actual_time'],
				open = self.df['HA_Open'],
				close = self.df['HA_Close'],
				high = self.df['HA_High'],
				low = self.df['HA_Low'],
				name = "Candlesticks"),row=1,col=1)

			if buy_signals:
				fig2.append_trace(go.Scatter(
					x = [item[0] for item in buy_signals],
					y = [item[1] for item in buy_signals],
					name = "Buy Signals",
					mode = "markers",
					marker_size = 10,fillcolor='#008000'
				),row=1,col=1)

			if sell_signals:
				fig2.append_trace(go.Scatter(
					x = [item[0] for item in sell_signals],
					y = [item[1] for item in sell_signals],
					name = "Sell Signals",
					mode = "markers",
					marker_size = 10,fillcolor='#FF7F50'
				),row=1,col=1)
			if df.__contains__('30_ema'):
				fig2.append_trace(go.Scatter(
					x = df["actual_time"],
					y = df['30_ema'],
					name = "30_ema",
					line = dict(color = ('rgba(255, 0, 102, 50)'))),row=1,col=1)
			if df.__contains__('10_ema'):
				fig2.append_trace(go.Scatter(
					x = df["actual_time"],
					y = df['10_ema'],
					name = "10_ema",
					line = dict(color = ('rgba(255, 207, 0, 50)'))),row=1,col=1)		
			fig2.update_layout(xaxis_rangeslider_visible=False,template="plotly_dark")
			plot(fig2, filename='./'+"helkin_ashi"+'.html')
		# style and display
		# let's customize our layout a little bit:
		fig.update_layout(xaxis_rangeslider_visible=False,template="plotly_dark")
		
		plot(fig, filename='./'+"hey"+'.html')
