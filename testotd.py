__author__ = 'cmaurer'

from optparse import OptionParser
import ast

oc_log = r'/Users/cmaurer/testlog.log'
# oc_log = r'/var/log/debesys/OC_sgx.log'
order_tags = ["account", "order_capacity", "sText2", "sText1", "PARTY_ROLE_CLIENT_ID",
              "PARTY_ROLE_INVESTMENT_DECISION_MAKER", "PARTY_ROLE_EXECUTING_TRADER", "text_tt", "order_origination",
              "order_attribute_type"]


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

    for msg in logmsg:
        # print msg

        if len(msg.split("=")) == 1:
            if msg != '}' and msg != '{':
                print "msg:", msg
                idx = logmsg.index(msg)
                logmsg.pop(idx)

        elif msg == "{":
            bracketed_message = True
            bracketed_message_list = []
            # print "bracketed_message:", bracketed_message

        elif bracketed_message:
            if msg == '}':
                if "PARTY_ROLE_CLEARING_ACCOUNT" not in bracketed_message_list\
                        and "PARTY_ROLE_CUSTOMER_ACCOUNT" not in bracketed_message_list:
                    message_list.append(str(bracketed_message_list))
                bracketed_message = False
            # elif msg == '{':
            #     pass
            else:
                bracketed_message_list.append(msg)
            # print "bracketed_message:", bracketed_message
            # print "bracketed_message_list:", bracketed_message_list

        # elif msg == 'user_id':
        #     security_desc_contains_spaces = False
        #     message_list.append(' '.join(security_desc_list))

        # if msg == '{':
        #     bracketed_message_list = []
        #     bracketed_message = True
        # if msg == '}':
        #     bracketed_message = False
        #     bracketed_message_list.append(msg)
        #     # msg = ' '.join(bracketed_message_list)
        #     msg = bracketed_message_list[-2]
        #
        # if bracketed_message:
        #     bracketed_message_list.append(msg)
        #     if len(bracketed_message_list) in range(1, 5) and len(bracketed_message_list) % 3 == 0:
        #         bracketed_message_list.append(',')

        # elif security_desc_contains_spaces:
        #     security_desc_list.append(msg)

        else:
            message_list.append(msg)

        # if 'security_desc' in msg:
        #     security_desc_list = []
        #     security_desc_contains_spaces = True

    message_list_item = iter(message_list)
    log_message_dict = dict(zip(message_list_item, message_list_item))
    for message_list_item in message_list:
        # print "message_list_item:", message_list_item
        log_message_dict[message_list_item.split("=")[0]] = message_list_item.split("=")[1]
    #
    print "log_message_dict:", log_message_dict
    # return log_message_dict


def verify_otd_data(log_message):
    for element in log_message:
        # print "element:", element
        for order_tag in order_tags:
            if order_tag in element:
                # ast.literal_eval(output)
                print "order_tag in element:", element


def parse_otd_data(order_id):

    print "Searching {} for order_id {}...".format(oc_log, order_id)
    logfile = open(oc_log, 'r')
    for line in logfile.readlines():
        if order_id in line:
            line_list = line.split(" | ")[5:]
            if "order_submitter_inl.h" in line_list[0]:
                line_list.pop(0)
            print "#" * 20
            print line_list[0]
            print "#" * 20
            print "\n\nline:", line, "\n\n"
            if "secondary_cl_ord_id" in line:
                log_message = [line_list[0], line_list[1].lstrip(' ')]
                log_message.append(line_list[2])
                log_message.append(line_list[3])
                log_message.extend(line_list[4].split(" "))
            else:
                log_message = [line_list[0], line_list[1].lstrip(' ')]
                log_message.extend(line_list[2].split(" "))
                # log_message.append(line_list[3])
                # log_message.extend(line_list[4].split(" "))

            for instr_msg in log_message:
                if "security_desc" in instr_msg:
                    message_index = log_message.index(instr_msg)
                    log_message.pop(message_index)
                    break

            # print "log_message[{}]:".format(message_index)
            # print log_message[message_index]
            # print log_message[27]
            log_message.pop(message_index)
            log_message.pop(message_index)
            log_message.pop(message_index)

            # print "log_message:", log_message, "\n\n"
            verification = parse_log_message(log_message)
            # print "verification:", verification
            # verify_otd_data(verification)

# optmenu()
parse_otd_data("65c581a7-96d4-43af-a2a3-dae163a6c56d")