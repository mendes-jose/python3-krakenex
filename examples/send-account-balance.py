#!/usr/bin/env python3

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See `examples/LICENSE.txt`.

# Prints the account blance to standard output.

import krakenex
import numpy as np
import os

k = krakenex.API()
k.load_key('~/.ssh/kraken.key')

bal = k.query_private('Balance')['result']
recent_trades = dict()
recent_trades['XXBTZEUR'] = k.query_public('Trades', data={'pair': 'XXBTZEUR'})['result']['XXBTZEUR']
recent_trades['DOTEUR'] = k.query_public('Trades', data={'pair': 'DOTEUR'})['result']['DOTEUR']

btc_value = np.mean([float(trade[0]) for trade in recent_trades['XXBTZEUR'] if trade[3] == 's'])
dot_value = np.mean([float(trade[0]) for trade in recent_trades['DOTEUR'] if trade[3] == 's'])

bal_eur = float(bal['ZEUR']) + float(bal['XXBT']) * btc_value + float(bal['DOT']) * dot_value
print('Balance: {0:.2f}'.format(bal_eur))
if bal_eur >= 550:
    cmd = 'signal-cli -u SENDER_NB send -m "Balance: ' + '{0:.2f}'.format(bal_eur) + '" RECEIVER_NB'
    os.system(cmd)
