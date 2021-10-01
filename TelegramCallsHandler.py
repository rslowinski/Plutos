import logging
from typing import List

from TTypes import RawTMessage, TMessage, TSignal
from symbols import coin_symbols
from trading import create_trade


def prep_for_float_conv(txt):
    return txt.replace('$', '').replace(',', '.')


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


class TelegramCallsHandler:

    def __init__(self):
        self.raw_msgs: List[RawTMessage] = []
        self.parsed_msgs: List[TMessage] = []

    def add_msgs(self, msgs: List[RawTMessage]):
        self.raw_msgs.extend(msgs)
        self.parse_msgs()

    def _extract_token_from_text(self, txt):
        for chunk in txt.split():
            if chunk.upper() in coin_symbols:
                return chunk.upper()
        return None

    def _extract_position_type_from_text(self, txt):
        if 'LONG' in txt:
            return 'LONG'
        elif 'SHORT' in txt:
            return 'SHORT'
        else:
            return None

    def _extract_entry_price(self, txt):
        for chunk in txt.split():
            c = chunk.replace('$', '').replace(',', '.')
            try:
                return float(c)
            except ValueError:
                continue

    def _extract_sl_price(self, txt):
        splited = txt.split()

        for idx, chunk in enumerate(splited):
            if 'SL' == chunk and len(splited) > idx + 1:
                c = splited[idx + 1].replace('$', '').replace(',', '.')
                try:
                    return float(c)
                except ValueError:
                    continue

    def _extract_tp_prices(self, txt):
        splited = txt.split()

        tps = []
        for idx, chunk in enumerate(splited):
            if 'TP' == chunk and len(splited) > idx:
                c = splited[idx + 1].replace('$', '').replace(',', '.')
                if is_float(c):
                    tps.append(float(c))
            elif len(splited) > idx + 2 and is_float(prep_for_float_conv(chunk)) and is_float(
                    prep_for_float_conv(splited[idx + 1])) and is_float(prep_for_float_conv(splited[idx + 2])):
                tps.append(float(prep_for_float_conv(splited[idx])))
                tps.append(float(prep_for_float_conv(splited[idx + 1])))
                tps.append(float(prep_for_float_conv(splited[idx + 2])))
                return tps
        return tps

    def parse_msgs(self):
        # add changel specific parsing
        parsed = []
        if len(self.raw_msgs) > 1 and self.raw_msgs[-1].msg == self.raw_msgs[-2].msg:
            print('duplicate - skip')
            return

        for raw_msg in [self.raw_msgs[-1]]:
            try:
                splited = raw_msg.msg.split('\n')
                channel = splited[0]
                author = splited[1].replace(':', '')
                coin = self._extract_token_from_text(raw_msg.msg)
                position_type = self._extract_position_type_from_text(raw_msg.msg)
                entry = self._extract_entry_price(raw_msg.msg)
                sl = self._extract_sl_price(raw_msg.msg)
                tps = self._extract_tp_prices(raw_msg.msg)
                if not position_type and len(tps) > 1:
                    if tps[0] < tps[1]:
                        position_type = 'LONG'
                    else:
                        position_type = 'SHORT'

                assert coin is not None
                signal = TSignal(coin, (entry, entry), position_type, raw_msg.datetime)
                parsed_msg = TMessage(author, signal, [raw_msg])
                parsed.append(parsed_msg)
                print(f"Going to create call for messgae={parsed}")

                total_value = 300 if parsed_msg.author in ['CryptoGodJohn', 'Astekz'] else 100
                create_trade(parsed_msg.signal, total_value)

            except Exception:
                logging.getLogger().exception("couldn't parse")
                print(f"Couldn't parse msg={raw_msg}")
        self.parsed_msgs = parsed
