# Imports
import uuid
from google.protobuf.text_format import MessageToString
from tt.messaging.order import enums_pb2 as enums
from tt.pyrate.debesys.clients.order_sender import OCOrderSender
from tt.pyrate.debesys.messaging import dict_to_protobuf
from tt.pyrate.debesys.messaging import Header
from tt.pyrate.debesys.messaging import load_lbm_config
from tt.pyrate.debesys.messaging import PYRATE_APPLICATION_ID
from tt.pyrate.debesys.messaging import QuoteRequest

# Initialization
# NOTE: make sure you add the Pyrate application to your lbm.conf
load_lbm_config("/etc/debesys/lbm.conf", "T_Trader")

# Put your info here
account_id = 747
#account_id = 38228
#connection_id = 4088
connection_id = 16738
user_id = 9587

# Construct the message
request_id = uuid.uuid4()
user_parameters = {
    "user_parameter_list":[
        {   'name':"sText1",
            'type':7,
            'v_string':"Py-Text1"
        },
        {   'name':"sText3",
            'type':7,
            'v_string':"Py-Text3"
        }
        ]
    }

attrs = {
        'manual_order_indicator':1,
        'instrument_id':15953546965709579576,
#        'price':10000,
#        'order_qty':1,
        'side':enums.SIDE_BUY,
        'market_id':enums.TT_MARKET_ID_HKEX_DEV,
        'connection_id': connection_id,
        'user_id': user_id,
        'account_id': account_id,
        'request_id':request_id,
        'source':enums.SOURCE_PYRATE,
        'appl_id':PYRATE_APPLICATION_ID,
#        "user_parameters": user_parameters
        }
msg = dict_to_protobuf(attrs, QuoteRequest)

# Submit a new order
submitter = OCOrderSender(account_id, connection_id)
submitter.send(msg)
# print '\nSent QuoteRequest {} on {}\n'.format(request_id, submitter.send_topic)
print msg

# Wait for a response
try:
    wait_topic = 'OR.OC.{}'.format(connection_id)
    msgs = submitter.wait_for_response(Header.MSG_QUOTE_REQUEST_RESPONSE, request_id, wait_topic)
    print '\nQuoteRequestResponse received:\n'
    print MessageToString(submitter.order_responses[request_id][-1].order_response)
except:
    print 'Did not receive a QuoteRequestResponse from the OC, make sure its up!!'

