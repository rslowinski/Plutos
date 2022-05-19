#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from TelegramCallsHandler import TelegramCallsHandler
from TTypes import RawTMessage, TMessage, TSignal

# trades\nPat:\n@everyone HIGH RISK QTUM short 10.64 sl 11.2 @everyone TODO: it doesnt detect SHORT type

def test_parser_simple_ex():
    # GIVEN:
    handler = TelegramCallsHandler()
    now = datetime.now()
    msg = RawTMessage("🚀trades\nAstekz:\nDOT short 15.34", now)

    # WHEN:
    handler.add_msgs([msg])

    # THEN:
    assert handler.parsed_msgs[0].author == 'Astekz'
    assert handler.parsed_msgs[0].signal.coin == 'DOT'
    assert handler.parsed_msgs[0].signal.buy_range == (15.34, 15.34)
    assert handler.parsed_msgs[0].signal.type == 'SHORT'

def test_parser_simple_ex2():
    # GIVEN:
    handler = TelegramCallsHandler()
    now = datetime.now()
    msg = RawTMessage("🚀trades\nAstekz:\nDOT LONG 15.34", now)

    # WHEN:
    handler.add_msgs([msg])

    # THEN:
    assert handler.parsed_msgs[0].author == 'Astekz'
    assert handler.parsed_msgs[0].signal.coin == 'DOT'
    assert handler.parsed_msgs[0].signal.buy_range == (15.34, 15.34)
    assert handler.parsed_msgs[0].signal.type == 'LONG'

def test_parser():
    # GIVEN:
    handler = TelegramCallsHandler()
    now = datetime.now()
    msg = RawTMessage("🚀trades\nCryptoGodJohn:\nRSR $.0373 SL $.0366 tp $.0381 $.0388 $.03945 $.0402 @everyone", now)

    # WHEN:
    handler.add_msgs([msg])

    # THEN:
    assert handler.parsed_msgs[0].author == 'CryptoGodJohn'
    assert handler.parsed_msgs[0].signal.coin == 'RSR'
    assert handler.parsed_msgs[0].signal.buy_range == (0.0373, 0.0373)
    assert handler.parsed_msgs[0].signal.type == 'LONG'


def test_multi_part_msgs():
    # GIVEN:
    handler = TelegramCallsHandler()
    now = datetime.now()

    msg1 = RawTMessage("🚀trades\nCryptoGodJohn:\n@everyone", now)
    msg2 = RawTMessage("🚀trades\nCryptoGodJohn:\nBTC $41,400 - $ 40,800 LIMIT ORDER", now)
    msg3 = RawTMessage("🚀trades\nCryptoGodJohn:\nSL 39,600", now)
    msg4 = RawTMessage("🚀trades\nCryptoGodJohn:\n @everyone", now)
    msg5 = RawTMessage("🚀trades\nCryptoGodJohn:\n$42,400 $44,322 $46,601 $48,020 $50,030", now)
    msgs = [msg1, msg2, msg3, msg4, msg5]

    # WHEN:
    handler.add_msgs(msgs)

    # THEN:
    assert handler.parsed_msgs[0].author == 'CryptoGodJohn'
    assert handler.parsed_msgs[0].signal.coin == 'BTC'
    assert handler.parsed_msgs[0].signal.buy_range[0] in [41.4, 40.8]
    # assert handler.parsed_msgs[0].signal.type == 'LONG'



def test_multi_part_msgs_with_different_authors():
    # GIVEN:
    handler = TelegramCallsHandler()
    msg1 = RawTMessage("🚀trades\nCryptoGodJohn:\n@everyone",
                       datetime(2021, 5, 17, hour=12, minute=30))
    msg2 = RawTMessage("🚀trades\nCryptoGodJohn:\nBTC $41,400 - $ 40,800 LIMIT ORDER",
                       datetime(2021, 5, 17, hour=12, minute=30))
    msg3 = RawTMessage("🚀trades\nAstekz:\nSRM LONG\n3.885\nSTOP 3.685",
                       datetime(2021, 5, 17, hour=12, minute=30))
    msg4 = RawTMessage("🚀trades\nCryptoGodJohn:\nSL 39,600",
                       datetime(2021, 5, 17, hour=12, minute=30))
    msg5 = RawTMessage("🚀trades\nCryptoGodJohn:\n @everyone",
                       datetime(2021, 5, 17, hour=12, minute=30))
    msg6 = RawTMessage("🚀trades\nCryptoGodJohn:\n$`42,400 $44,322 $46,601 $48,020 $50,030`",
                       datetime(2021, 5, 17, hour=12, minute=33))
    msgs = [msg1, msg2, msg3, msg4, msg5, msg6]

    # WHEN:
    handler.add_msgs(msgs)

    # THEN:
    assert handler.parsed_msgs[0].author == 'CryptoGodJohn'
    assert handler.parsed_msgs[0].signal.coin == 'BTC'
    assert handler.parsed_msgs[0].signal.buy_range[0] in [41.4, 40.8]
    # assert handler.parsed_msgs[0].signal.type == 'LONG'

    assert handler.parsed_msgs[1].author == 'Astekz'
    assert handler.parsed_msgs[1].signal.coin == 'SRM'
    assert handler.parsed_msgs[1].signal.buy_range[0] in [3.885]
    assert handler.parsed_msgs[1].signal.type == 'LONG'
