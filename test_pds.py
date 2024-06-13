import ast
import requests

class GetSupportedOrderTypes():

    def __init__(self):

        environment = "int-stage-cert"
        self.market = "KRX"

        pds_url = "".join(["https://pds-", environment, ".trade.tt"])
        self.base_url = pds_url

        self.headers = {'content-type': 'application/json'}
        self.market = "SGX"
        self.auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiIsIng1dCI6Ik1NSVMtN2JHWTFHc2J2bk5adl9hMS1xelpQTSJ9.eyJjbGllbnRfaWQiOiI1NTRkYjQ4MjdmZDc0MDg5ODNkYjVhNmZmOWM0YjQ5MSIsInN1YiI6Ijc3ZTY0OGEyYzJkODQ5MDE4Yjc3MTNmYWZhOTk3YzhjIiwic2NvcGVzIjpbIm5leHRyYWRlciIsImRhcndpbi9yIiwicm9lL2VkIiwicm9lL2V3Iiwicmlza2FwaS9kZXYiLCJudHcvdHQiLCJkaWFnL3giLCJwZHMvZ3VpIiwibW9uaXRvci94Iiwic2NyeS9lZXgiLCJzY29yZS90dCIsInRyaWFnZS9yIiwidHJpYWdlL3giLCJzeXN0ZW0vdiIsInNjb3JlL3YiLCJkaWFnL3YiLCJlY2hvL2FsbCIsInJpc2thcGkvciIsInJpc2thcGkvdyIsIm1lc3NhZ2VjZW50ZXIvciIsImJpbGxpbmcvciIsImxlZGdlci9yIiwiYm9va2llL3IiLCJqdW5vd2ViL3IiLCJlZGdlL3ByIiwiZWRnZS9vciIsIm50dy94IiwicGRzL3IiLCJwZHMvdyIsImFuYWx5dGljcy9yIiwibWVzc2FnZWNlbnRlci93Iiwic2NvcmUvciIsInRyYWRlL3YiLCJhZGwvdiIsImFsZ290ZXN0aW5nL3YiLCJtb25pdG9yL3YiLCJzZXR1cC92IiwiaW5ib3gvdiJdLCJpc3MiOiJodHRwczovL2lkLnR0c3RhZ2UuY29tLyIsImF1ZCI6InR0LWludCIsImV4cCI6MTU5MjkyMzU1MCwibmJmIjoxNTkyODgwMjkwLCJleHBpcmVzIjoxNTkyOTIzNTUwMDAwMDAwMDAwLCJyZWZyZXNoX2F0IjoxNTkyODgzOTUwLCJpZCI6OTU4NywicGVyc29uX2lkIjoyMDUsInRva2VuX2lzc3VlIjoyLCJzZXNzaW9uX2lkIjoiNTI4ODYwNzc4NjY1NjA3MTY4MDVlZjE2NzlhYjQzZTg1LjYwNjA5MDAyIiwidHdvX2ZhY3RvciI6Ik5vbmUiLCJjbGllbnRfaXAiOiIyNy4xMTAuMjguMjA0IiwiY29tcGFueV9pZCI6MjQsImlkcCI6Imh0dHA6Ly90dHN0cy50cmFkaW5ndGVjaG5vbG9naWVzLmNvbS9hZGZzL3NlcnZpY2VzL3RydXN0In0.PIE1hii8rGbn6sCSTLUyC-18D1b6lVQxS0rKTfBTFW2pjAU0adto3XUVsV_feasS9Fz6MrV1ACuP6JzH8xyVsnw2FBCvrG9w53Sa-CARgF9Jx7auC2MJlQUyssJJUTvwHTxpXwPz4yLOqKC8EP2tuJOuCh8ycRHNbGggMrjR6KUBUEmIiyZuDeLKxehKKZP_8TRufI6pRRbhlduLb9hJuinNevLEmQhGWehgs6JJ0E_rexmzos3NJzA4FAKTQGyfo3fGND7637AWFLC9kICkZVKaxEkx18B-KmE9gap6QQV-rxfMfwVJtUAqMpgcIdhvFYmSiOqUwLzrGogaS64PMA'}

        self.ottifmap= {1: 'Market Day',
                        2: 'Limit Day',
                        3: 'StopMarket Day',
                        4: 'StopLimit Day',
                        5: 'Iceberg Day',
                        6: 'Block Day',
                        7: 'Cross Day',
                        8: 'BookOrCancel Day',
                        9: 'OCO Day',
                        10: 'MinVol Day',
                        11: 'MarketOnOpen Day',
                        12: 'LimitIfTouched Day',
                        13: 'StopMarketToLimit Day',
                        19: 'MTL Day',
                        21: 'Basis Day',
                        22: 'GCross Day',
                        25: 'OneSided Day',
                        28: 'Vola Day',
                        29: 'EFP Day',
                        30: 'EFPI Day',
                        31: 'EFPFI Day',
                        32: 'EFS Day',
                        33: 'FlexFut Day',
                        34: 'FlexOpt Day',
                        35: 'Market GTC',
                        36: 'Limit GTC',
                        37: 'StopMarket GTC',
                        38: 'StopLimit GTC',
                        39: 'Iceberg GTC',
                        40: 'MarketOnOpen GTC',
                        41: 'StopMarketToLimit GTC',
                        45: 'MTL GTC',
                        46: 'MTL GTC',
                        47: 'Market IOC',
                        48: 'Limit IOC',
                        49: 'Iceberg IOC',
                        50: 'StopMarketToLimit IOC',
                        51: 'MTL IOC',
                        52: 'Market FOK',
                        53: 'Limit FOK',
                        54: 'Iceberg FOK',
                        55: 'StopMarketToLimit FOK',
                        56: 'MTL FOK',
                        57: 'Market GTDate',
                        58: 'Limit GTDate',
                        59: 'StopMarket GTDate',
                        60: 'StopLimit GTDate',
                        61: 'Iceberg GTDate',
                        62: 'MinVol GTDate',
                        63: 'MarketOnOpen GTDate',
                        64: 'LimitIfTouched GTDate',
                        65: 'MTL GTDate',
                        66: 'Market OnOpen',
                        67: 'Limit OnOpen',
                        68: 'StopMarket OnOpen',
                        69: 'StopLimit OnOpen',
                        70: 'StopMarketToLimit OnOpen',
                        71: 'MarketToLimit OnOpen',
                        72: 'Market OnClose',
                        73: 'Limit OnClose',
                        74: 'StopMarket OnClose',
                        75: 'StopLimit OnClose',
                        76: 'StopMarketToLimit OnClose',
                        77: 'MarketToLimit OnClose',
                        81: 'Market OnAuction',
                        83: 'Market GIS',
                        84: 'Limit GIS',
                        85: 'StopMarket IOC',
                        86: 'StopMarket FOK',
                        87: 'StopLimit IOC',
                        88: 'StopLimit FOK',
                        93: 'StopMarketToLimit GTDate',
                        94: 'LIMIT Day+',
                        95: 'LIMIT GTC+',
                        96: 'LIMIT GTDate+',
                        97: 'MTL Day+',
                        98: 'LIMIT PO GTC',
                        99: 'MinVol GTC',
                        100: 'LimitIfTouched IOC',
                        101: 'LimitIfTouched FOK',
                        102: 'LimitIfTouched GTC',
                        103: 'LimitIfTouched OnOpen',
                        104: 'LimitIfTouched OnClose',
                        105: 'MarketIfTouched IOC',
                        106: 'MarketIfTouched FOK',
                        107: 'MarketIfTouched Day',
                        108: 'MarketIfTouched GTC',
                        109: 'MarketIfTouched OnOpen',
                        110: 'MarketIfTouched OnClose',
                        111: 'MarketIfTouched GTDate',
                        112: 'MarketToLimitIfTouched IOC',
                        113: 'MarketToLimitIfTouched FOK',
                        114: 'MarketToLimitIfTouched Day',
                        115: 'MarketToLimitIfTouched GTC',
                        116: 'MarketToLimitIfTouched OnOpen',
                        117: 'MarketToLimitIfTouched OnClose',
                        118: 'MarketToLimitIfTouched GTDate',
                        119: 'Discretion IOC',
                        121: 'PostOnly Day',
                        146: 'Market GTT',
                        147: 'Limit GTT',
                        148: 'MarketToLimit GTT',
                        149: 'StopLimit GTT',
                        150: 'StopMarket GTT',
                        151: 'MarketIfTouched GTT',
                        152: 'Limit GFA',
                        153: 'MarketIfTouched GFA'}

    def parse_pds_output(self, url):
        if "ottif" in url or "pmerge" in url:
            headers = dict(self.headers, **self.auth)
        else:
            headers = dict(self.headers)
        request = requests.get(url, headers=headers)
        output = request._content
        while ":false" in output:
            output = output.replace(":false", ":\"false\"")
        while ":true" in output:
            output = output.replace(":true", ":\"true\"")
        full_output = ast.literal_eval(output)
        if "instruments" and "globalData" not in str(full_output):
            if "entries" in full_output:
                try:
                    output = full_output["entries"]
                except KeyError:
                    print("PDS Output parsing Error case:\n\n" + str(full_output))
        else:
            try:
                output = full_output["instruments"]
            except:
                try:
                    output = full_output["data"]["globalData"]["markets"]
                except:
                    output = full_output["instrument"]

        return output

    def get_market_id(self, market=None):
        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        if market is None:
            return market_ids
        else:
            for market_id in market_ids:
                if market in str(market_id):
                    return str(market_id["i"])
            else:
                print("Market, \"{0}\" does not seem to exist.".format(market))

    def get_supported_order_types(self, market):

        endpoint = "/api/1/ottif?marketId=" + str(market)
        url = self.base_url + endpoint

        supported_order_types = self.parse_pds_output(url)
        for o in supported_order_types:
            try:
                qqq = o['ottifId']#, o['params'][0]['e']
            except KeyError:
                print("\nKeyError case:\n\n" + str(o))
                supported_order_types = None
            except TypeError:
                print("\nTypeError case:\n\n" + str(supported_order_types))
                supported_order_types = None

        return supported_order_types

    def get_pmerge_data(self, market):

        endpoint = "/api/1/pmerge/market/" + str(market)
        url = self.base_url + endpoint

        pmerge_data = self.parse_pds_output(url)

        return pmerge_data

    def create_order_type_table(self):

        order_type_db = {}
        all_possible_order_types = []
        list_of_all_possible_order_types = []
        truth_table = (r'/Users/cmaurer/truthtable.csv')

        all_markets = self.get_market_id()
        for market in all_markets:
            marketid = market['i']
            marketName = market['n']
            if marketName == "DV" or "_DEV" in marketName:
                pass
            else:
                supported_order_types = self.get_supported_order_types(marketid)

                if supported_order_types is not None:
                    order_types_for_this_market = []
                    for ordtype in supported_order_types:
                        order_types_for_this_market.append(ordtype['ottifId'])
                        if ordtype['ottifId'] not in all_possible_order_types:
                            all_possible_order_types.append(ordtype['ottifId'])
                            if 'n' not in ordtype:
                                ordtype['n'] = "UNKNOWN"
                            ordtype_name = ordtype['n'].replace("-", " ")
                            ordtype_name = ordtype_name.replace("OO", "OnOpen") if "OO" in ordtype_name else ordtype_name
                            list_of_all_possible_order_types.append(": ".join([str(ordtype['ottifId']).zfill(3), ordtype['n'].replace("-", " ")]))
                    order_support_data = {marketName: order_types_for_this_market}
                    order_type_db[marketid] = dict(**order_support_data)

        list_of_all_possible_order_types.sort()
        for ot in list_of_all_possible_order_types:
            print(ot)

        all_possible_order_types.sort()

        table_header = [' ', ]
        for dictitem in order_type_db.itervalues():
            for k, v in dictitem.iteritems():
                if k not in table_header:
                    table_header.append(k)
        table_header.sort()
        table_header.append('\n')
        f = open(truth_table, 'w')
        f.write(",".join(table_header))
        f.close()

        for possible_order_type in all_possible_order_types:
            try:
                table_row = [self.ottifmap[possible_order_type], ]
            except KeyError:
                print("KeyError:", possible_order_type)
            for column in table_header:
                for value in order_type_db.itervalues():
                    for k, v in value.iteritems():
                        if k == column:
                            if possible_order_type in v:
                                table_row.append('Y')
                            else:
                                table_row.append(' ')
            table_row.append('\n')
            f = open(truth_table, 'a')
            f.write(",".join(table_row))
            f.close()


runme = GetSupportedOrderTypes()
#runme.create_order_type_table()
print(runme.get_pmerge_data())