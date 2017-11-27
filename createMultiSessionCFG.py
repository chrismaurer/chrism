#~Filename: setupGW.py
#~Copies the files needed to run your GW and creates the necessary Trader IDs in User Manager.

import os
import time
import _winreg

def createCFG():
    #2
[session_order1]
trader=trader1
connection=connection2
gateway=gateway_ose
consumer=order
users=trader2
#users=trader1, trader2
primary=False

[session_price1]
trader=trader1
connection=connection2
gateway=gateway_ose
consumer=price
primary=False

[session_fill1]
trader=trader1
connection=connection2
gateway=gateway_ose
consumer=fill
primary=False