# from exchange_market import data  
if __name__=="__main__":
    import data
else:
    from exchange_market import data
    
import json
import pandas as pd
import os 
import time
import collections
import hashlib
import requests
import pyti.relative_strength_index as RSI



request_delay = 1000

class CoinExApiError(Exception):
    pass

class Coinex(data.Data):
    _headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        }
    def __init__(self):
        """
        coinex marekt api : https://github.com/coinexcom/coinex_exchange_api/wiki
        we make the request URl by the base + endpoint like below 
        All of these names in self.endpoints are the same as api documentaion 

        """
        super(Coinex, self).__init__()
        """
        you should put your coinex access id and secret key to in .bashrc 
        or .zshrc file and export those as  COINEX_PUB and COINEX_SEC   
        """
        self._access_id=os.environ.get("COINEX_PUB")
        self._secret_key=os.environ.get("COINEX_SEC")
        self.base = "https://api.coinex.com/v1/"
        self.endpoints = {
            "Acquire Currency Rate": 'common/currency/rate',
            "Acquire K-Line Data": "market/kline",
            "Acquire Single Market Information":"market/detail",
            "Acquire Market Statistics":"market/ticker",
            "Acquire Market Depth":"market/depth",
            "inquire_account_info":"balance/info",
            "Acquire Market List":"market/list"
        }

    def _v1(self, path, method='get', auth=False, **params):

        headers = dict(self._headers)

        if auth:
            if not self._access_id or not self._secret_key:
                raise CoinExApiError('API keys not configured')

            params.update(access_id=self._access_id)
            params.update(tonce=int(time.time() * 1000))

        params = collections.OrderedDict(sorted(params.items()))

        if auth:
            headers.update(Authorization=self._sign(params))
        if method == 'post':
            resp = requests.post(self.base + path, json=params, headers=headers)
        else:
            # fn = getattr(requests, method)
            # print(22*"x")
            resp = requests.get(self.base + path, params=params, headers=headers)


        return self._process_response(resp)

    def _process_response(self, resp):
        resp.raise_for_status()

        dictionary = json.loads(resp.text)
        df = pd.DataFrame.from_dict(dictionary)
        if dictionary['code'] != 0:
            raise CoinExApiError(data['message'])

        return dictionary['data']

    def _sign(self, params):
        data = '&'.join([key + '=' + str(params[key]) for key in sorted(params)])
        data = data + '&secret_key=' + self._secret_key
        data = data.encode()
        return hashlib.md5(data).hexdigest().upper()
    

    def get_ohlcv(self, __market: str,__type: str,__limit: int):
        """
        Request description: Acquire k-line data for specified period, including latest 1000 datas

        name 	         type 	        required 	                description
        -------------------------------------------------------------------------------
        market 	         String 	        Yes 	         See<API invocation description·market>
        limit 	         Integer 	    No(default 100) 	    Less than or equal to 1000

        type           	String           	Yes                 1min:1min;
                                                                3min:3min;
                                                                5min:5min;
                                                                15min:15min;
                                                                30min:30min;
                                                                1hour:1hour;
                                                                2hour:2hour;
                                                                4hour:4hour;
                                                                6hour:6hour;
                                                                12hour:12hour;
                                                                1day:1day;
                                                                3day:3day;
                                                                1week:1week;

            # Request
            GET https://api.coinex.com/v1/market/kline?market=bchbtc&type=1min
            # Response
            {
            "code": 0,
            "data": [
                [
                1492358400, # Time
                "10.0",   # Opening
                "10.0",   # Closing
                "10.0",   # Highest
                "10.0",   # Lowest
                "10",     # Volume
                "100",    # amount
                "BCHBTC", # market
                ]
            ],
            "message": "Ok"
            }
            

        """
        print(f"limit = {__limit}")
        data=self._v1(self.endpoints["Acquire K-Line Data"],method="get",auth=False,market=__market,limit=__limit,type=__type)   

        # put in dataframe and clean-up
        lst = []

        for i in range(len(data)):
            lst.append(data[i])
        col_name=["time", "open", "close", "high", "low", "volume","amount"]
        df = pd.DataFrame(lst, columns=col_name)
        for col in col_name:
            df[col] = df[col].astype(float)
        df=df.drop(columns=["amount"])
        # print(json.dumps(data, indent=6, sort_keys=True))
        return df

    def get_ticks(self,__market):

        """
        Request description: Acquire real-time market data

        name 	type 	required 	description
        ----------------------------------------
        market 	String 	Yes 	See<API invocation description·market>

        example:

        # Request
        GET https://api.coinex.com/v1/market/ticker?market=bchbtc
        # Response
        {
        "code": 0,
        "data": {
            "date": 1513865441609,  # server time when returning
            "ticker": {
            "buy": "10.00",           # buy 1
            "buy_amount": "10.00",    # buy 1 amount
            "open": "10",             # highest price
            "high": "10",             # highest price
            "last": "10.00",          # latest price 
            "low": "10",              # lowest price
            "sell": "10.00",          # sell 1
            "sell_amount": "0.78",    # sell 1 amount
            "vol": "110"              # 24H volume
            }
        },
        "message": "Ok"
        }
        """

        # download data

        data=self._v1(self.endpoints["Acquire Market Statistics"],method="get",auth=False,market=__market) 
         # put in dataframe and clean-up
        dictionary=data
        lst = []
        lst.append(dictionary["ticker"])
        print(type(lst))
        df = pd.DataFrame(
            lst, columns=["buy","buy_amount", "open", "high", "high", "last", "low", "sell","sell_amount","vol"]
        )
  
        return df
    

    def single_market_info(self,__market):

        """

        Request description: Acquire single market detail information

        name 	type 	required 	description
        -------------------------------------------------------
        market 	String 	Yes 	See<API invocation description·market>

        # Request
        GET https://api.coinex.com/v1/market/detail?market=BTCUSDT
        # Response
        {
        "code": 0,
        "message": "Ok",
        "data":
            {
            "taker_fee_rate": "0.001",
            "pricing_name": "USDT",
            "trading_name": "BTC",
            "min_amount": "0.001",
            "name": "BTCUSDT",
            "trading_decimal": 8,
            "maker_fee_rate": "0.001",
            "pricing_decimal": 8
            }
        }

        """



        # download data


        data=self._v1(self.endpoints["Acquire Single Market Information"],method="get",auth=False,market=__market) 

        # put in dataframe and clean-up
        lst = []
        lst.append(data)
        df = pd.DataFrame(
            lst, columns=["name","taker_fee_rate", "maker_fee_rate", "min_amount", "trading_name", "trading_decimal", "pricing_name", "pricing_decimal"]
        )
        return df

    def acquire_currency_rate(self):
        """

        Request description: acquire currency rate
        Request parameter: None

        # Request
        GET https://api.coinex.com/v1/common/currency/rate
        # Response
        {
            "code": 0,
            "data": {
                "USDT_to_USD": "1.00003078",
                "USDC_to_USD": "1",
                "TUSD_to_USD": "1",
                "PAX_to_USD": "1",
                "BTC_to_USD": "34934.26524358",
                "BCH_to_USD": "525.72618135",
                "ETH_to_USD": "2128.28550661",
                "CET_to_USD": "0.05444967"
            },
            "message": "Success"
        }

        """
        
        # download data

        data=self._v1(self.endpoints["Acquire Currency Rate"],method="get",auth=False) 

        print(json.dumps(data, indent=6, sort_keys=True))

    def acquire_market_depth(self,__market,__merge,__limit):   
        """
        Request description: Acquire buy/sell statistics，return up to 50

        Request parameter:
        name 	type 	    required 	        description
        ---------------------------------------------------------
        market 	String 	    Yes 	        See<API invocation description·market>
        merge 	String 	    Yes 	        '0', '0.1', '0.01', '0.001', '0.0001', '0.00001', '0.000001', '0.0000001', '0.00000001
        limit 	Interger 	No(Default20)  	Return amount，range: 5/10/20/50

        Return value description:
        name 	    type 	    description
        -------------------------------------------------
        last 	    String 	    Last price
        time 	    Long 	    Updated time of Depth
        asks 	    Array 	    Seller depth
        asks[0][0] 	String 	    Order price
        asks[0][1] 	String 	    Order amount
        bids 	    Array 	    Buyer depth
        bids[0][0] 	String 	    Order price
        bids[0][1] 	String 	    Order amount
        """


        # # download data

        data=self._v1(self.endpoints["Acquire Market Depth"],method="get",auth=False,market=__market,merge=__merge,limit=__limit) 

        return data


    pass

    def inquire_account_info(self):
        """
        Request description: Inquire account asset constructure. When the total assets (available + frozen) of a coin are 0, no coin data return.


        Signature required: Yes

        Request Header:
        authorization:"xxxx"(32-digit capital letters, see generating method in <API invocation instruction>)

        Request Url:https://api.coinex.com/v1/balance/info

        Request parameter:
        name 	    type 	required 	description
        access_id 	String 	    Yes 	access_id
        tonce   	Integer 	Yes 	Tonce is a timestamp with a positive Interger that represents the number of milliseconds from Unix epoch to the current time. Error between tonce and server time can not exceed plus or minus 60s

        Return value description:
        name 	description
        frozen 	frozen amount
        available 	available amount

        """



        return self._v1("balance/info",method="get",auth=True)       
    
    def market_list(self,quoteAssets:list=["BTC"]):
        available_assets=[]
        data=self._v1(self.endpoints["Acquire Market List"],method="get",auth=False)
        for i in range(len(data)):
            for asset in quoteAssets:
                if asset in data[i]:
                    available_assets.append(data[i])
                    

        return available_assets 
    
    def helkin_ashi(self, __market: str,__type: str,__limit: int):

        df = self.get_ohlcv(__market,__type,__limit)
        df_shifted=df.shift(periods=1)
        HelkinAshi_df=pd.DataFrame()
        HelkinAshi_df["close"]=(df["close"]+df["open"]+df["high"]+df["low"])/4
        HelkinAshi_df["open"]=(df_shifted["close"]+df_shifted["open"])/2
        HelkinAshi_df["high"]=df["high"]
        HelkinAshi_df["low"]=df["low"]
        HelkinAshi_df["time"]=df["time"]
        

        return HelkinAshi_df
        
        
       


if __name__ == "__main__":
    market = Coinex()
    df = market.get_ohlcv("btcusdt","5min",500)
    print(df.head(3))
    df["rsi"]=RSI.relative_strength_index(data=df['close'].tolist(),period=14)
    print(df.head(20))
    # available_assets=market.market_list()
    # print("\n",available_assets)

    print("\n")
    # print(data)


