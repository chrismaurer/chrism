#~TestCaseName: logfile_analiser
#~TestCaseSummary: This program reads logfiles from C:\logs and returns any unexpected messages

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import logging
from optparse import OptionParser

log = logging.getLogger(__name__)

class logfile_analiser():

    def __init__(self):
        self.market_ids = { '1' : 'CESC Index Futures / Options',
                            '2' : 'Stock Futures',
                            '3' : 'Three-Year Exchange Fund Note Futures',
                            '8' : 'Gold Futures',
                            '16' : 'Mini Hang Seng Index Futures / Options',
                            '20' : 'Stock Options',
                            '24' : 'HIBOR',
                            '27' : 'HSI Dividend Point Index Futures / HSCEI Dividend Point Index Futures',
                            '34' : 'Hang Seng Index Futures / Options',
                            '35' : 'Flexible Hang Seng Index Options',
                            '37' : 'Flexible H-shares Index Options',
                            '38' : 'H-shares Index Futures / Options',
                            '51' : 'HSI Volatility Index Futures',
                            '70' : 'Renminbi Currency Futures',
                            '93' : 'IBOVESPA Index Futures',
                            '96' : 'S&P BSE SENSEX Index Futures',
                            '99' : 'FTSE/JSE Top 40 Index Futures',
                            '102' : 'MICEX Index Futures',
                            '114' : 'API 8 Thermal Coal Futures',
                            '120' : 'London Alum, Copper, Zinc Mini Futures'}

        self.status_ids = { '1' : 'OPENALLOC',
                            '2' : 'CLOSE',
                            '3' : 'OPEN',
                            '4' : 'PREOPEN',
                            '5' : 'PREOPENALLOC',
                            '6' : 'PAUSE',
                            '7' : 'PRE_MKT_ACT',
                            '8' : 'CL_START',
                            '9' : 'CL_CLOSE',
                            '10' : 'AHT_CLOSE',
                            '11' : 'AHT_CLR_INFO',
                            '12' : 'AHT_INACT_T_ORDER',
                            '13' : 'AHT_NEXT_DAY',
                            '14' : 'AHT_OPEN',
                            '15' : 'AHT_OPEN_PL',
                            '16' : 'AHT_PRE_MKT_ACT',
                            '17' : 'OPEN_PL',
                            '18' : 'CLOSE_TODAY',
                            '19' : 'OPEN_DPL',
                            '20' : 'FAILOVER',
                            '90' : 'COMMODITY SUSPENDED',
                            '91' : 'COMMODITY RESUME TRADING'}

        self.on_mkt_stat = {'1' : 'SecurityTradingStatus_OpeningDelay',
                            '2' : 'SecurityTradingStatus_TradingHalt',
                            '3' : 'SecurityTradingStatus_Resume',
                            '4' : 'SecurityTradingStatus_NoOpenNoResume',
                            '5' : 'SecurityTradingStatus_PriceIndication',
                            '6' : 'SecurityTradingStatus_TradingRangeIndication',
                            '7' : 'SecurityTradingStatus_MarketImbalanceBuy',
                            '8' : 'SecurityTradingStatus_MarketImbalanceSell',
                            '9' : 'SecurityTradingStatus_MarketOnCloseImbalanceBuy',
                            '10' : 'SecurityTradingStatus_MarketOnCloseImbalanceSell',
                            '12' : 'SecurityTradingStatus_NoMarketImbalance',
                            '13' : 'SecurityTradingStatus_NoMarketOnCloseImbalance',
                            '14' : 'SecurityTradingStatus_ITSPreOpening',
                            '15' : 'SecurityTradingStatus_NewPriceIndication',
                            '16' : 'SecurityTradingStatus_TradeDisseminationTime',
                            '17' : 'SecurityTradingStatus_ReadyToTrade',
                            '18' : 'SecurityTradingStatus_NotAvailableForTrading',
                            '19' : 'SecurityTradingStatus_NotTradedOnThisMarket',
                            '20' : 'SecurityTradingStatus_UnknownOrInvalid',
                            '21' : 'SecurityTradingStatus_PreOpen',
                            '22' : 'SecurityTradingStatus_OpeningRotation',
                            '23' : 'SecurityTradingStatus_FastMarket',
                            '24' : 'SecurityTradingStatus_PreCross',
                            '25' : 'SecurityTradingStatus_Cross',
                            '26' : 'SecurityTradingStatus_NoCancel',
                            '27' : 'SecurityTradingStatus_Expired',
                            '96' : 'SecurityTradingStatus_Auction',
                            '97' : 'SecurityTradingStatus_SessionRollover',
                            '98' : 'SecurityTradingStatus_PostTrade',
                            '99' : 'SecurityTradingStatus_PreTrade',
                            '100' : 'SecurityTradingStatus_Deleted'}

    def optmenu(self):
        parser = OptionParser()
        parser.add_option('-f', '--file', dest='filename',
                          help='logfile to be read', metavar='filename')
        optmenu, args = parser.parse_args()
        return optmenu.filename

    def parseline(self, inputline):
        market_id = ''
        status_id = ''
        on_mkt_stat_id = ''
        line_list = inputline.split('[')
        for item in line_list:
            if 'market:' in item:
                market_id_ref_lookup = str(item)
                market_id_ref_lookup = market_id_ref_lookup.replace('market:', '')
                market_id_ref_lookup = market_id_ref_lookup.replace('] ', '')
                try:
                    market_id = self.market_ids[market_id_ref_lookup]
                except KeyError:
                    market_id = 'UNKNOWN (%s)' % market_id_ref_lookup
                    
            if 'exch:' in item:
                status_id_ref_lookup = item
                status_id_ref_lookup = status_id_ref_lookup.replace('exch:', '')
                status_id_ref_lookup = status_id_ref_lookup.replace(']\n', '')
                try:
                    status_id = self.status_ids[status_id_ref_lookup]
                except KeyError:
                    status_id = 'UNKNOWN (%s)' % status_id_ref_lookup

        if 'OnCommodityStatus' in line_list[0]:
            on_mkt_stat_id = line_list[1]
            on_mkt_stat_id = on_mkt_stat_id.lstrip('[')
            on_mkt_stat_id = on_mkt_stat_id.rstrip('] ')
            try:
                on_mkt_stat_id = self.on_mkt_stat[on_mkt_stat_id]
            except KeyError:
                on_mkt_stat_id = 'UNKNOWN (%s)' % on_mkt_stat_id
        else:
            on_mkt_stat_id = line_list[2]
            on_mkt_stat_id = on_mkt_stat_id.lstrip('[')
            on_mkt_stat_id = on_mkt_stat_id.rstrip('] ')
            try:
                on_mkt_stat_id = self.on_mkt_stat[on_mkt_stat_id]
            except KeyError:
                on_mkt_stat_id = 'UNKNOWN (%s)' % on_mkt_stat_id

        outputline = ' | '.join((line_list[0], market_id, on_mkt_stat_id, status_id))
        return outputline

    def parseLogfile(self):

        logfile = self.optmenu()

        inputFile = open(logfile, 'r')
        for line in inputFile.readlines():
            if 'OnCommodityStatus' in line or 'OnMarketStatus' in line:
                print self.parseline(line)

        inputFile.close()


logRead = logfile_analiser()
logRead.optmenu()
logRead.parseLogfile()