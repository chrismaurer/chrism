Market_TT_BUY = {"855": [6, 8, 2, 4, 3, 10, 6], "860": [6, 1, 8, 7, 7, 7, 2], "865": [7, 6, 10, 4, 10], "870": [2, 3, 7, 2, 4], "875": [2, 1, 8, 3, 7, 10, 10], "885": [10, 4, 6, 4, 10, 7, 3], "890": [5, 2, 7, 6, 9, 6], "900": [2, 7, 4, 5, 1, 7, 4], "910": [9, 2, 8, 2, 5, 4, 9, 3], "915": [9, 6, 9, 6, 10, 4, 8, 8, 2], "920": [6, 8, 6, 2, 10, 8, 4, 8, 6], "930": [2, 3, 6, 3, 7, 7, 3], "935": [3, 10, 8, 5, 2, 9, 10, 6], "945": [4, 5, 5, 6, 5, 2, 1, 8, 1], "960": [8, 2, 9, 5, 9, 7, 10, 4], "965": [1, 5, 1, 2, 5, 6, 5], "970": [2, 5, 1, 8, 8], "975": [9, 10, 8, 4, 4, 5], "985": [1, 1, 1, 6, 5, 10, 3, 6, 2, 5], "990": [7, 2, 3, 10, 10, 3, 7, 6, 9]}
Market_TT_SELL = {"1010": [4, 7, 4, 8, 3, 6, 5], "1015": [9, 5, 8, 5, 4, 4, 7, 9, 6], "1025": [3, 1, 8, 10, 7], "1030": [6, 4, 3, 1, 10, 8, 4, 1], "1050": [2, 3, 2, 6, 10, 6], "1055": [3, 10, 3, 5, 9, 7, 4, 10], "1065": [7, 7, 3, 9, 8, 1, 2, 6, 9, 4], "1070": [5, 10, 6, 7, 7, 4, 2, 9, 6], "1075": [8, 5, 10, 2, 9, 7, 9], "1080": [3, 6, 3, 5, 3, 4], "1085": [9, 2, 8, 6, 10], "1095": [7, 10, 5, 4, 4, 4, 5, 8], "1100": [8, 3, 4, 3, 5, 1], "1115": [8, 6, 7, 1, 6, 1, 6], "1120": [5, 6, 7, 9, 8, 3, 10, 7], "1125": [6, 9, 5, 4, 8, 7, 5, 3, 7], "1130": [7, 4, 1, 8, 1, 3, 10, 7, 4, 8], "1135": [4, 7, 2, 7, 7, 5, 7, 10, 1, 6], "1140": [3, 7, 4, 2, 2, 4, 8, 7], "1145": [2, 8, 9, 2, 7, 4, 3, 7, 4, 1]}
Order_Count_TT_BUY = [9, 10, 6, 5, 7, 8, 9, 8, 7, 9, 9, 8, 7, 6, 7, 7, 5, 5, 7, 7]
Order_Count_TT_SELL = [7, 9, 5, 8, 6, 8, 10, 9, 7, 6, 5, 8, 6, 7, 8, 9, 10, 10, 8, 10]

Market_Buy = {"875": [41], "880": [64], "885": [44], "890": [35], "900": [30], "910": [42], "915": [62], "920": [58], "925": [43], "930": [31], "935": [53], "940": [39], "945": [37], "960": [54], "965": [25], "970": [24], "975": [40], "985": [40], "990": [57], "995": [2]}
Market_Sell = {"1015": [5], "1025": [7], "1035": [37], "1055": [36], "1070": [42], "1095": [18], "1100": [24], "1115": [35], "1120": [55], "1125": [54], "1130": [53], "1135": [56], "1140": [37], "1145": [47], "2840": [197], "2845": [199], "2850": [199]}
Order_Count_Buy = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Order_Count_Sell = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# print "Buy Side Price Levels match:", Market_TT_BUY.keys() == Market_TT_BUY.keys()
# print "Sell Side Price Levels match:", Market_TT_SELL.keys() == Market_TT_SELL.keys()

print "-" * 40

print "Buy Price Level counts match:", len(Market_TT_BUY.keys()) == len(Market_Buy.keys())
missing_actual_buy_prices = [item for item in Market_TT_BUY.keys() if item not in Market_Buy.keys()]
if len(missing_actual_buy_prices) > 0:
    print "Expected Buy prices missing from Actual:", missing_actual_buy_prices
missing_expected_buy_prices = [item for item in Market_Buy.keys() if item not in Market_TT_BUY.keys()]
if len(missing_expected_buy_prices) > 0:
    print "Actual Buy prices missing from Expected:", missing_expected_buy_prices

print "Buy Order Counts match:", sum(Order_Count_TT_BUY) == sum(Order_Count_Buy)

exp_buy_order_prices = []
actual_buy_order_prices = []
for exp_buy_order_prc in Market_TT_BUY.values():
    exp_buy_order_prices.append(sum(exp_buy_order_prc))
for actual_buy_order_prc in Market_Buy.values():
    actual_buy_order_prices.append(sum(actual_buy_order_prc))
print "Buy Order Prices match:", sum(exp_buy_order_prices) == sum(actual_buy_order_prices)

print "-" * 40

print "Sell Price Level counts match:", len(Market_TT_SELL.keys()) == len(Market_Sell.keys())
missing_actual_sell_prices = [item for item in Market_TT_SELL.keys() if item not in Market_Sell.keys()]
if len(missing_actual_sell_prices) > 0:
    print "Expected Sell prices missing from Actual:", missing_actual_sell_prices
missing_expected_sell_prices = [item for item in Market_Sell.keys() if item not in Market_TT_SELL.keys()]
if len(missing_expected_sell_prices) > 0:
    print "Actual Sell prices missing from Expected:", missing_expected_sell_prices

print "Sell Order Counts match:", sum(Order_Count_TT_SELL) == sum(Order_Count_Sell)

exp_sell_order_prices = []
actual_sell_order_prices = []
for exp_sell_order_prc in Market_TT_SELL.values():
    exp_sell_order_prices.append(sum(exp_sell_order_prc))
for actual_sell_order_prc in Market_Sell.values():
    actual_sell_order_prices.append(sum(actual_sell_order_prc))
print "Sell Order Prices match:", sum(exp_sell_order_prices) == sum(actual_sell_order_prices)