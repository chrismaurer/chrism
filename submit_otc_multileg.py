# Submit a single-leg ICE OTC block trade:
# based on actual TTUS connection and account configuration; not "offline" tests.

# Imports
import uuid
from google.protobuf.text_format import MessageToString
from tt.messaging.order import enums_pb2 as enums
from tt.pyrate.debesys.clients.order_sender import OCOrderSender
from tt.pyrate.debesys.messaging import dict_to_protobuf
from tt.pyrate.debesys.messaging import Header
from tt.pyrate.debesys.messaging import load_lbm_config
from tt.pyrate.debesys.messaging import PYRATE_APPLICATION_ID
from tt.pyrate.debesys.messaging import TradeCaptureReport
from tt.pyrate.debesys.messaging import NewTradeCapture

# Initialization
# NOTE: make sure you add the Pyrate application to your lbm.conf
load_lbm_config("/etc/debesys/lbm.conf", "T_Trader")

# Put your info here
connection_id = 12062
user_id = 5964
account_id = 32017
account = "cm-int-dev1"
account_id_1 = 32017
account_1 = "cm-int-dev1"


# Construct the message
report_id = uuid.uuid4()
attrs = {
        'instrument_id':9579938746251228935,
        'market_id':enums.TT_MARKET_ID_OSE,
        'connection_id': connection_id,
        'user_id': user_id,
        'account_id': account_id,
        'report_id':report_id,
        'source':enums.SOURCE_PYRATE,
        'appl_id':PYRATE_APPLICATION_ID,
        'trd_type':enums.TRD_TYPE_INTERNAL,
        "report_legs":[
            {
                'leg_instrument_id':9579938746251228935,
                'price':23553,
                "report_sides":[
                    {   'side':enums.SIDE_BUY,
                        'alloc_qty': 500,
                        'account': account,
                        'account_id': account_id,
                        'position_effect':enums.POSITION_EFFECT_OPEN,
                        "parties":[
                            {   'party_id':"LM4",
                                'party_role':enums.PARTY_ROLE_CUSTOMER_INFO
                            },
                            {   'party_id':"C",
                                'party_role':enums.PARTY_ROLE_ACCOUNT_CODE
                            },
                            {   'party_id':"LM3",
                                'party_role':enums.PARTY_ROLE_ORDER_ENTRY_OPERATOR_ID
                            },
                            {   'party_id':"9",
                                'party_role':enums.PARTY_ROLE_CLEARING_INSTRUCTION
                            },
                            {   'party_id':"B45J2",
                                'party_role':enums.PARTY_ROLE_CONTRA_TRADER
                            },
                        ]
                    },
                    {   'side':enums.SIDE_SELL,
                        'alloc_qty': 500,
                        'account': account_1,
                        'account_id': account_id_1,
                        'position_effect':enums.POSITION_EFFECT_OPEN,
                        "parties":[
                            {   'party_id':"ML4",
                                'party_role':enums.PARTY_ROLE_CUSTOMER_INFO
                            },
                            {   'party_id':"C",
                                'party_role':enums.PARTY_ROLE_ACCOUNT_CODE
                            },
                            {   'party_id':"ML3",
                                'party_role':enums.PARTY_ROLE_ORDER_ENTRY_OPERATOR_ID
                            },
                            {   'party_id':"9",
                                'party_role':enums.PARTY_ROLE_CLEARING_INSTRUCTION
                            },
                            {   'party_id':"B45J2",
                                'party_role':enums.PARTY_ROLE_CONTRA_TRADER
                            },
                        ]
                    }
                ]
            },
            {
                'leg_instrument_id':12026807449771530280,
                'price':23557,
                "report_sides":[
                    {   'side':enums.SIDE_BUY,
                        'alloc_qty': 500,
                        'account':account,
                        'account_id': account_id,
                        'position_effect':enums.POSITION_EFFECT_OPEN,
                        "parties":[
                            {   'party_id':"LM4",
                                'party_role':enums.PARTY_ROLE_CUSTOMER_INFO
                            },
                            {   'party_id':"C",
                                'party_role':enums.PARTY_ROLE_ACCOUNT_CODE
                            },
                            {   'party_id':"LM3",
                                'party_role':enums.PARTY_ROLE_ORDER_ENTRY_OPERATOR_ID
                            },
                            {   'party_id':"9",
                                'party_role':enums.PARTY_ROLE_CLEARING_INSTRUCTION
                            },
                            {   'party_id':"B45J2",
                                'party_role':enums.PARTY_ROLE_CONTRA_TRADER
                            },
                        ]
                    },
                    {   'side':enums.SIDE_SELL,
                        'alloc_qty': 500,
                        'account':account_1,
                        'account_id': account_id_1,
                        'position_effect':enums.POSITION_EFFECT_OPEN,
                        "parties":[
                            {   'party_id':"ML4",
                                'party_role':enums.PARTY_ROLE_CUSTOMER_INFO
                            },
                            {   'party_id':"C",
                                'party_role':enums.PARTY_ROLE_ACCOUNT_CODE
                            },
                            {   'party_id':"ML3",
                                'party_role':enums.PARTY_ROLE_ORDER_ENTRY_OPERATOR_ID
                            },
                            {   'party_id':"9",
                                'party_role':enums.PARTY_ROLE_CLEARING_INSTRUCTION
                            },
                            {   'party_id':"B45J2",
                                'party_role':enums.PARTY_ROLE_CONTRA_TRADER
                            },
                        ]
                    }
                ]
            }
        ],
        'trans_booked_time':1438800308000000000
        }
msg = dict_to_protobuf(attrs, NewTradeCapture)

# Submit a new order
submitter = OCOrderSender(account_id, connection_id)
submitter.send(msg)
print '\nSent NewTradeCaptureReport {} on {}\n'.format(report_id, submitter.send_topic)
print msg
