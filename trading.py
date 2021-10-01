from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import json
from TTypes import TMessage, TSignal
import os
from datetime import datetime
credentials_path = 'binance_credentials.json'

with open(credentials_path) as f:
    credentials = json.load(f)

api_key = credentials['api_key']
api_secret = credentials['api_secret']

client = Client(api_key, api_secret)

active_trades = []


def create_trade(signal: TSignal, total_value):
    os.system('say "trade is coming"')
    if len(active_trades) > 10:
        print(f'skipping call {signal} as there are already too many existing calls')
        os.system(f'say "skipping call for {signal.coin} as there are already too many existing calls"')
        return

    symbol = f'{signal.coin}USDT'
    unit_price = float(client.get_ticker(symbol=symbol)['askPrice'])
    if signal.type == 'LONG' and unit_price > 1.05 * signal.buy_range[0]:
        print(f"Unit price already too high, skipping long trade, unit_p={unit_price}")
        os.system("say 'Unit price already too high, skipping long trade'")
        return
    elif signal.type == 'SHORT' and unit_price < 1.1 * signal.buy_range[0]:
        print(f"Unit price already too low, skipping short trade, unit_p={unit_price}")
        os.system("say 'Unit price already too low, skipping short trade'")
        return

    res = client.futures_create_order(
        symbol=symbol,
        side=Client.SIDE_SELL if (signal.type == 'SHORT') else Client.SIDE_BUY,
        type=Client.FUTURE_ORDER_TYPE_MARKET,
        quantity=int(total_value / unit_price)
    )
    print(f"created trade signal={signal} with res={res}")
    active_trades.append(total_value)

    os.system(f'say "Bought {signal.type} {signal.coin} for {total_value} dollars"')

    with open('trades.log', 'a') as f:
        f.write(f'\n==\nAt {datetime.now()} Bought {signal.type} {signal.coin} for {total_value} dollars, buy_range={signal.buy_range}\n==\n')