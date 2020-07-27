# Imports
import uuid
import tt.pyrate.util
from google.protobuf.text_format import MessageToString
from tt.messaging.order import enums_pb2 as enums
from tt.pyrate.debesys.clients.order_sender import OCOrderSender
from tt.pyrate.debesys.messaging import dict_to_protobuf
from tt.pyrate.debesys.messaging import Header
from tt.pyrate.debesys.messaging import load_lbm_config
from tt.pyrate.debesys.messaging import PYRATE_APPLICATION_ID
from tt.pyrate.debesys.messaging import NewQuote
from tt.pyrate.debesys.messaging import QuoteCancel
from tt.pyrate.debesys.messaging import QuoteReplace

# Initialization
# NOTE: make sure you add the Pyrate application to your lbm.conf
load_lbm_config("/etc/debesys/lbm.conf", "T_Trader")

responses = []

soid = None

############################
# update values below for your connection/account/user
connection_id = 19080
user_id = 5964
account_id = 99073
account = "cm-int-devp"
############################
wait_topic = 'OR.OC.{}'.format(connection_id)

quote_side_1=[
       {'qty':1,'side':1,'price':21003}, #21000
       {'qty':1,'side':2,'price':21004}  #21006
     ]
attrs = {
        'instrument_id':7560150852431274216, #MCHZ7
        'quote_side':quote_side_1,
        'ord_type':enums.ORD_TYPE_LIMIT,
        'time_in_force':enums.TIME_IN_FORCE_DAY,
        'market_id':enums.TT_MARKET_ID_HKEX,
        'connection_id': connection_id,
        'user_id': user_id,
        'account_id': account_id,
        'account':account,
        'quote_id':None,
        'source':enums.SOURCE_PYRATE,
        'appl_id':PYRATE_APPLICATION_ID,
        'aggressor_indicator':True,
        }

er_format = """quote_id:{quote_id}, cl_ord_id:{cl_ord_id}, acct:{account}, acctid:{account_id}, user:{user_id},
ord_status: {ord_status}, exec_type:{exec_type}, ord_type:{ord_type},
inst_id: {instrument_id}
text:{text}"""

def SetQuoteId(attr, oid):
    attr['quote_id'] = oid

def GetQuoteId(attr):
    return attr['quote_id']

def RunTest():
    submitter = OCOrderSender(attrs['account_id'], attrs['connection_id'])
    while True:
        if GetQuoteId(attrs) == None:
            print "n - new quote"
        else:
            print "x - change quote"
            print "c - cancel quote"
            print "q - quit"
        opt = raw_input("=> ")
        if opt == "c":
            if SendQuoteCancel(submitter, attrs):
                SetQuoteId(attrs, None)
        if opt == "n":
            SendNewQuote(submitter, attrs)
        if opt == "x":
            SendQuoteReplace(submitter, attrs)
        if opt == "q":
            return True
    return False

#########################################################################
def SendNewQuote(submitter, attrs):
    global responses, soid
    quote_id = uuid.uuid4()
    SetQuoteId(attrs, quote_id)
    msg = dict_to_protobuf(attrs, NewQuote)
    print '\nSent QuoteCancel {}\n'.format(quote_id, )  # submitter.send_topic)
    # print '\nSent NewQuote {} on {}\n'.format(quote_id, )  # submitter.send_topic)
    print msg
    submitter.send(msg)

 #Wait for a response
    try:
        msgs = submitter.wait_for_response(Header.MSG_QUOTE_RESPONSE, wait_topic, timeout=60, exists=True)
        print '\nQuoteResponse for new quote received:\n'
        responses = responses + submitter.order_responses[quote_id]
        soid = submitter.order_responses[quote_id][-1].order_response.secondary_order_id
        return True

    except:
        print 'Did not receive a new QuoteResponse from the OC, make sure its up!!'
        return False

#########################################################################
def SendQuoteCancel(submitter, attrs):
    global responses
    quote_id = GetQuoteId(attrs)
    msg = dict_to_protobuf(attrs, QuoteCancel)
    print '\nSent QuoteCancel {}\n'.format(quote_id, )  # submitter.send_topic)
    # print '\nSent QuoteCancel {} on {}\n'.format(quote_id, )  # submitter.send_topic)
    submitter.send(msg)

# Wait for a response
    try:
        msgs = submitter.wait_for_response(Header.MSG_QUOTE_RESPONSE, wait_topic)
        print '\nQuoteResponse for cancel received:\n'
        responses = responses + submitter.order_responses[quote_id]
        return True

    except:
        print 'Did not receive a canceled QuoteResponse from the OC, make sure its up!!'
        return False

#########################################################################
def SendQuoteReplace(submitter, attrs):
    global responses, soid
    quote_id = GetQuoteId(attrs)

    buy_qty = raw_input("Buy Qty=> ")
    sell_qty = raw_input("Sell Qty=> ")
    buy_prc = raw_input("Buy Price=> ")
    sell_prc = raw_input("Sell Price=> ")

    quote_side_1=[
               {'qty':int(buy_qty),'side':1,'price':int(buy_prc)}, #orginal=32860
               {'qty':int(sell_qty),'side':2,'price':int(sell_prc)}  #orginal=32870
                 ]
    attrs = {
                 'instrument_id':18340898110286919161, #MCHZ7
                 'quote_side':quote_side_1,
                 'ord_type':enums.ORD_TYPE_LIMIT,
                 'time_in_force':enums.TIME_IN_FORCE_DAY,
                 'market_id':enums.TT_MARKET_ID_HKEX,
                 'connection_id': connection_id,
                 'user_id': user_id,
                 'account_id': account_id,
                 'account':account,
                 'quote_id':quote_id,
                 'source':enums.SOURCE_PYRATE,
                 'appl_id':PYRATE_APPLICATION_ID,
                 'aggressor_indicator':True,
                 'secondary_order_id': soid
            }
# Submit a replace quote
    msg = dict_to_protobuf(attrs, QuoteReplace)
    print '\nSent QuoteCancel {}\n'.format(quote_id, )  # submitter.send_topic)
#    print '\nSent QuoteReplace {} on {}\n'.format(quote_id, )  # submitter.send_topic)
    print msg
    submitter.send(msg)

# Wait for a response
    try:
        msgs = submitter.wait_for_response(Header.MSG_QUOTE_RESPONSE, wait_topic)
        print '\nQuoteResponse for QuoteReplace received:\n'
        responses = responses + submitter.order_responses[quote_id]

        soid = submitter.order_responses[quote_id][-1].order_response.secondary_order_id
        print MessageToString(submitter.order_responses[quote_id][-1].order_response)
        
        return True

    except:
        print 'Did not receive a QuoteReplace QuoteResponse from the OC, make sure its up!!'
        return False
    
if __name__ == "__main__":
    import sys
    RunTest()



