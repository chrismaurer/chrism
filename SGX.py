###############################################################################
#
#                    Unpublished Work Copyright (c) 2019
#                  Trading Technologies International, Inc.
#                       All Rights Reserved Worldwide
#
#          # # #   S T R I C T L Y   P R O P R I E T A R Y   # # #
#
# WARNING:  This program (or document) is unpublished, proprietary property
# of Trading Technologies International, Inc. and is to be maintained in
# strict confidence. Unauthorized reproduction, distribution or disclosure
# of this program (or document), or any program (or document) derived from
# it is prohibited by State and Federal law, and by local law outside of
# the U.S.
#
###############################################################################

import os

from tt.messaging.order import enums_pb2 as enums
from tt.orders.test.suites.test_gtc_backward_compatibility import \
    BaseTestGTCBackwardCompatibilitySendOrder, \
    BaseTestGTCBackwardCompatibilityReplaceFillCancelOrder
from tt.sgx.test.lib.utils import useful_symbols

class TestGTCBackwardCompatibilitySendOrder(BaseTestGTCBackwardCompatibilitySendOrder):

    def __init__(self):
        super(TestGTCBackwardCompatibilitySendOrder, self).__init__( \
                                           'gtc_backward_compatibility_send_order')
        self.oc_name = 'sgx'
        self.pause_after_starts = 0
        self.market_finder_sets = [
            {'market_id':enums.TT_MARKET_ID_SGX,
             'sec_type_id':'FUT', 'symbols':useful_symbols}]

        # simple market finder configuration parameters
        self.symbol = 'NK'
        self.security_type = enums.SECURITY_TYPE_FUTURE
        self.prefer_front_month = False
        self.prefer_back_month = True
        self.order_price = 50
        self.use_market_finder = False


class TestGTCBackwardCompatibilityReplaceFillCancelOrder(BaseTestGTCBackwardCompatibilityReplaceFillCancelOrder):

    def __init__(self):
        super(TestGTCBackwardCompatibilityReplaceFillCancelOrder, self).__init__( \
                                           'gtc_backward_compatibility_replace_fill_cancel_order')
        self.oc_name = 'sgx'
        self.pause_after_starts = 0
        self.market_finder_sets = [
            {'market_id':enums.TT_MARKET_ID_SGX,
             'sec_type_id':'FUT', 'symbols':useful_symbols}]

        # simple market finder configuration parameters
        self.symbol = 'NK'
        self.security_type = enums.SECURITY_TYPE_FUTURE
        self.prefer_front_month = False
        self.prefer_back_month = True
        self.order_price = 50
        self.use_market_finder = False
