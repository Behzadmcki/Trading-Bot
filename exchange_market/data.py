from abc import ABC, abstractmethod
import requests
import json


class Data(ABC):

    def __init__(self):
        super(Data, self).__init__()
        self.symbol = None

    @abstractmethod
    def get_ohlcv(self):
        pass

    @abstractmethod
    def get_ticks(self):
        pass

    @abstractmethod
    def market_list(self):
        pass

    # def get(self, url, params=None, headers=None) -> dict:
    #     """ Makes a Get Request """
    #     try:
    #         response = requests.get(url, params=params, headers=headers)
    #         data = json.loads(response.text)
    #         data['url'] = url
    #     except Exception as e:
    #         print("Exception occured when trying to access " + url)
    #         print(e)
    #         data = {'code': '-1', 'url': url, 'msg': e}
    #     return data

    # def post(self, url, params=None, headers=None) -> dict:
    #     """ Makes a Post Request """
    #     try:
    #         response = requests.post(url, params=params, headers=headers)
    #         data = json.loads(response.text)
    #         data['url'] = url
    #     except Exception as e:
    #         print("Exception occured when trying to access " + url)
    #         print(e)
    #         data = {'code': '-1', 'url': url, 'msg': e}
    #     return data
