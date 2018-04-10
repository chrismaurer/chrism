# Imports
import time
import uuid
from google.protobuf.text_format import MessageToString
from tt.messaging.order import enums_pb2 as enums
from tt.pyrate.debesys.clients.order_sender import OCOrderSender
from tt.pyrate.debesys.messaging import dict_to_protobuf
from tt.pyrate.debesys.messaging import Header
from tt.pyrate.debesys.messaging import load_lbm_config
from tt.pyrate.debesys.messaging import PYRATE_APPLICATION_ID
from tt.pyrate.debesys.messaging import NewOrderCross

# Initialization
# NOTE: make sure you add the Pyrate application to your lbm.conf
load_lbm_config("/etc/debesys/lbm.conf", "T_Trader")

# Put your info here
account_id = 32017
account = "cm-int-dev1"
connection_id = 12029
user_id = 5964


# Submit a new order
order1id = uuid.uuid4()
order2id = uuid.uuid4()
cross_id = uuid.uuid4()
# Construct the message
attrs = {
    'cross_id':cross_id,
    'cross_type': enums.CROSS_TYPE_CROSS_IOC,
    "cross_sides":[
        {   'order_id': order1id,
            'instrument_id': 4947896210186472147,
            'price':489,
            'side':enums.SIDE_BUY,
            'ord_type':enums.ORD_TYPE_LIMIT,
            'order_qty':500,
            'time_in_force':enums.TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
            'market_id':enums.TT_MARKET_ID_ICE,
            'connection_id': connection_id,
            'user_id': user_id,
            'account_id': account_id,
            'account':account,
            'source':enums.SOURCE_PYRATE,
            'appl_id':PYRATE_APPLICATION_ID,
        },
        {   'order_id': order2id,
            'instrument_id': 4947896210186472147,
            'price':489,
            'side':enums.SIDE_SELL,
            'ord_type':enums.ORD_TYPE_LIMIT,
            'order_qty':500,
            'time_in_force':enums.TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
            'market_id':enums.TT_MARKET_ID_ICE,
            'connection_id': connection_id,
            'user_id': user_id,
            'account_id': account_id,
            'account':account,
            'source':enums.SOURCE_PYRATE,
            'appl_id':PYRATE_APPLICATION_ID,
        }
        ],
    }
msg = dict_to_protobuf(attrs, NewOrderCross)

# Submit a new order
submitter = OCOrderSender(account_id, connection_id)
submitter.send(msg)
print '\nSent NewOrderCross {} on {}\n'.format(cross_id, submitter.send_topic)
print msg


# Wait for a response
try:
    wait_topic = 'OC.{}'.format(connection_id)
    msgs = submitter.wait_for_response(Header.MSG_EXECUTION_REPORT, [wait_topic])
    print '\nExecutionReport received:\n'
    print MessageToString(submitter.order_responses[order_id][-1].order_response)
except:
    print 'Did not receive a ExecutionReport from the OC, make sure its up!!'



