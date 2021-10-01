from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import json
from TTypes import TMessage, TSignal
import os

credentials_path = 'binance_credentials.json'

with open(credentials_path) as f:
    credentials = json.load(f)

api_key = credentials['api_key']
api_secret = credentials['api_secret']

client = Client(api_key, api_secret)


print("f")
