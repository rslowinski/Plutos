#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) IHS Markit. All Rights Reserved.
NOTICE: All information contained herein is, and remains the property of IHS Markit and its suppliers,
if any. The intellectual and technical concepts contained herein are proprietary to IHS Markit and its suppliers and
may be covered by U.S. and Foreign Patents, patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly forbidden unless prior written
permission is obtained from IHS Markit.
"""
from collections import namedtuple

RawTMessage = namedtuple('RawTMessage', ['msg', 'datetime'])
TMessage = namedtuple('TMessage', ['author', 'signal', 'connected_raw_messages'])
TSignal = namedtuple('TSignal', ['coin', 'buy_range', 'type', 'date'])