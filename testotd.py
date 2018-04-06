__author__ = 'cmaurer'

from optparse import OptionParser
import ast

oc_log = r'/Users/cmaurer/testlog.log'
# oc_log = r'/var/log/debesys/OC_hkex.log'

order_tags={"account_code": "PARTY_ROLE_ACCOUNT_CODE",
            "clearing_account": "PARTY_ROLE_CLEARING_ACCOUNT",
            "clearing_firm_id": "PARTY_ROLE_CLEARING_FIRM",
            "client": "Routing Member ID",
            "client_id": "PARTY_ROLE_CLIENT_ID",
            "commodity_derivative_indicator": "ORDER_ATTRIBUTE_TYPE_RISK_REDUCTION_ORDER",
            "cti": "CTI Code",
            "desk": "Authorized Group ID",
            "direct_electronic_access": "order_origination",
            "exchange_account": "Exchange Account",
            "execution_decision": "PARTY_ROLE_EXECUTING_TRADER",
            "investment_decision": "PARTY_ROLE_INVESTMENT_DECISION_MAKER",
            "liquidity_provision": "ORDER_ATTRIBUTE_TYPE_LIQUIDITY_PROVISION_ACTIVITY_ORDER",
            "mifid_id": "PARTY_ROLE_COMPOSITE_MIFID_ID",
            "nybot_house": "NYBOT House #",
            "sAuthorizedTrader": "sAuthorizedTrader",
            "sMemo": "sMemo",
            "sText1": "sText1",
            "sText2": "sText2",
            "sTextTT": "text_tt",
            "trading_capacity": "order_capacity",
            "wce_house": "wce_house"}

def optmenu():
    parser = OptionParser()
    parser.add_option('-o', '--order', dest='order_id',
                      help='order_id you want to evaluate', metavar='order_id')
    optmenu, args = parser.parse_args()
    parse_otd_data(optmenu.order_id)


def parse_log_message(log_data):

    log_message_dict = {}
    log_msg_type = log_data[0]
    logmsg = log_data[1:]
    message_list = []
    bracketed_message_list = []
    bracketed_message = False

    concatenating = False
    for msg in logmsg:

        # handle values containing spaces
        if '="' in msg:
            concatenate_string = [msg]
            concatenating = True
        elif concatenating and msg == '':
            concatenate_string.append(msg)
        elif concatenating and '"' in msg:
            concatenate_string.append(msg)
            concatenating = False
            msg = ' '.join(concatenate_string)

        msg = msg.rstrip() if "}" in msg else msg

        if "=" not in msg:
            if msg == "{":
                bracketed_message = True
                bracketed_message_list = []
            elif bracketed_message and msg == '}':
                if any(msg_type not in msg for msg_type in
                       ["PARTY_ROLE_CLEARING_ACCOUNT", "PARTY_ROLE_CUSTOMER_ACCOUNT", "PARTY_ROLE_CLEARING_FIRM"]):
                    message_list.append("|".join(bracketed_message_list))
                bracketed_message = False
            else:
                pass

        elif bracketed_message:
            bracketed_message_list.append(msg)

        else:
            message_list.append(msg)


    for message_list_item in message_list:
        message_list_item = message_list_item.replace('\"', '')
        message_list_item = message_list_item.replace('order_attribute_type=', '')
        message_list_item = message_list_item.replace('order_attribute_value=1', 'Yes')
        message_list_item = message_list_item.replace('order_attribute_value=0', 'No')
        # print message_list_item
        if "|" in message_list_item and "party" in message_list_item and "Company" not in message_list_item:
            dict_update = message_list_item.split("|")
            for item in dict_update:
                if "party_role=" in item:
                    k = item.replace('party_role=', '')
                if "party_id" in item:
                    v = item.replace('party_id=', '')
            log_message_dict[k] = v
        elif "|" in message_list_item and "party" not in message_list_item and "Company" not in message_list_item:
            if "v_string" in message_list_item:
                dict_update = message_list_item.split("|")
                for item in dict_update:
                    if "name" in item:
                        k = item.replace('name=', '')
                    if "v_string" in item:
                        v = item.replace('v_string=', '')
                log_message_dict[k] = v
            else:
                log_message_dict[message_list_item.split("|")[0].replace('\"', '')] = message_list_item.split("|")[1].replace('\"', '')
        else:
            log_message_dict[message_list_item.split("=")[0].replace('\"', '')] = message_list_item.split("=")[1].replace('\"', '')

    return [log_msg_type, log_message_dict]


def parse_otd_data(order_id):

    verification_dict = {}
    verify_data_list = []
    er_counter = 0
    cr_counter = 0
    logfile = open(oc_log, 'r')
    for line in logfile.readlines():
        verification_list = []
        if order_id in line:
            line_list = line.split(" | ")[5:]
            if "order_submitter_inl.h" in line_list[0]:
                line_list.pop(0)
            if "secondary_cl_ord_id" in line:
                log_message = [line_list[0], line_list[1].lstrip(' ')]
                log_message.append(line_list[2])
                log_message.append(line_list[3])
                log_message.extend(line_list[4].split(" "))
            elif "TradeCaptureReport" in line:
                log_message = [line_list[0], line_list[1].lstrip(' ')]
                log_message.append(line_list[2])
                log_message.extend(line_list[3].split(" "))
            else:
                log_message = [line_list[0], line_list[1].lstrip(' ')]
                log_message.extend(line_list[2].split(" "))

            # for instr_msg in log_message:
            #     if "security_desc" in instr_msg:
            #         message_index = log_message.index(instr_msg)
            #         log_message.pop(message_index)
            #         if "ice" in str(logfile):
            #             log_message.pop(message_index)
            #             log_message.pop(message_index)
            #             log_message.pop(message_index)
            #         break

            verification = parse_log_message(log_message)

            # Verify log message
            log_message_type = verification[0]
            if verification[0] == "ExecutionReport":
                er_counter += 1
                log_message_type = '-'.join([verification[0], str(er_counter)])
            elif verification[0] == "OrderCancelReplaceRequest":
                cr_counter += 1
                log_message_type = '-'.join([verification[0], str(cr_counter)])
            else:
                log_message_type = verification[0]
            print "\n" + "#" * 20
            print log_message_type
            print "#" * 20 + "\n"
            for element in verification[1].iteritems():
                for k, v in order_tags.iteritems():
                    if k in str(element) or v in str(element):
                        print element
                        verification_list.append(element)
            verification_list.sort()
            verification_dict[log_message_type] = verification_list
            verify_data_list.append(log_message_type)

    for i in range(0, len(verify_data_list)-1):
        print "\n{0} and {1} match: {2}".format(verify_data_list[i], verify_data_list[i+1], verification_dict[verify_data_list[i]] == verification_dict[verify_data_list[i+1]])
        if not verification_dict[verify_data_list[i]] == verification_dict[verify_data_list[i+1]]:
            for item in verification_dict[verify_data_list[i+1]]:
                if item not in verification_dict[verify_data_list[i]]:
                    print "{0} contains: {1}".format(verify_data_list[i+1], item)

# optmenu()
parse_otd_data("65c581a7-96d4-43af-a2a3-dae163a6c56d")