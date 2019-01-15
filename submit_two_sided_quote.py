# Imports
import uuid
from google.protobuf.text_format import MessageToString
from tt.messaging.order import enums_pb2 as enums
from tt.pyrate.debesys.clients.order_sender import OCOrderSender
from tt.pyrate.debesys.messaging import dict_to_protobuf
from tt.pyrate.debesys.messaging import Header
from tt.pyrate.debesys.messaging import load_lbm_config
from tt.pyrate.debesys.messaging import PYRATE_APPLICATION_ID
from tt.pyrate.debesys.messaging import NewQuote

# Initialization
# NOTE: make sure you add the Pyrate application to your lbm.conf
load_lbm_config("/etc/debesys/lbm.conf")

# Put your info here
account_id = 747
account = "MaurerDC"
connection_id = 16710
user_id = 9587

price = 22
qty = 1

# Construct the message
quote_id = uuid.uuid4()
quote_side_1 = [
    {'qty': 1, 'side': 1, 'price': 22},  # 5100
    {'qty': 1, 'side': 2, 'price': 22}  # 22100
]
attrs = {
    'instrument_id': 14812862346263533632,
    'quote_side': quote_side_1,
    'market_id': enums.TT_MARKET_ID_HKEX,
    'connection_id': connection_id,
    'user_id': user_id,
    'account_id': account_id,
    'account': account,
    'quote_id': quote_id,
    'source': enums.SOURCE_PYRATE,
    'appl_id': PYRATE_APPLICATION_ID,
    'ord_type': enums.ORD_TYPE_LIMIT,
    'time_in_force': enums.TIME_IN_FORCE_DAY,
    'sender_location_id': "HKEX",
}
msg = dict_to_protobuf(attrs, NewQuote)

# Submit a new quote
submitter = OCOrderSender(account_id, connection_id)
submitter.send(msg)
print '\nSent NewQuote\n'
# print '\nSent NewQuote {} on {}\n'.format(quote_id, submitter.send_topic)
print msg

# Wait for a response
try:
    wait_topic = 'OR.OC.{}'.format(connection_id)
    msgs = submitter.wait_for_response(Header.MSG_QUOTE_RESPONSE, wait_topic)
    print '\nQuoteResponse(s) received:\n'
    print MessageToString(submitter.order_responses[quote_id][-1].order_response)

except:
    print 'Did not receive a QuoteResponse from the OC, make sure its up!!'
