#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Prints the account blance to standard output.

import krakenex
import numpy as np
import os

k = krakenex.API()
k.load_key('/data/data/com.termux/files/home/.ssh/kraken.key')

bal = k.query_private('Balance')['result']

recent_trades = dict()
value = dict()

for curr in bal:
    print(curr)

    if curr[0] == 'X':
        recent_trades[curr] = k.query_public('Trades', data={'pair': curr+'ZEUR'})['result'][curr+'ZEUR']
        value[curr] = np.mean([float(trade[0]) for trade in recent_trades[curr] if trade[3] == 's'])
    elif curr != 'ZEUR':
        recent_trades[curr] = k.query_public('Trades', data={'pair': curr+'EUR'})['result'][curr+'EUR']
        value[curr] = np.mean([float(trade[0]) for trade in recent_trades[curr] if trade[3] == 's'])


bal_eur = float(bal['ZEUR'])

for key, v in value.items():
    bal_eur += float(bal[key]) * v

print('Balance: {0:.2f}'.format(bal_eur))

prev_bal = 0
try:
    f = open("/data/data/com.termux/files/home/last_shown_balance.txt", "r")
    prev_bal = float(f.readline())
    f.close()
except OSError as e:
    print('going to creat missing file')

if prev_bal == 0 or abs(bal_eur/prev_bal - 1.0) > 0.1 or bal_eur >= 10000:
    cmd = 'termux-notification -c "Balance: ' + '{0:.2f}'.format(bal_eur) + '"'
    os.system(cmd)

    f = open("/data/data/com.termux/files/home/last_shown_balance.txt", "w")
    f.write(str(bal_eur))
    f.close()
