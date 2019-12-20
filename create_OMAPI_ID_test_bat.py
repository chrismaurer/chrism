__author__ = 'cmaurer'

import random

id_prefix = "TTGBX3"
range_start = 294
range_end = 309
exch_gateway_ip = "10.161.5.117"
exch_gateway_port = "12025"
password = "hkatstest"

range_end += 1

f = open(r'/Users/cmaurer/Desktop/test_hkex_ids.bat', 'w')
for id in range(range_start, range_end):
    random_port = random.randint(12024, 12027)
    f.write("\necho apitstlogin {0} {1} {2} {3} >> hkex_login_test.txt".format("".join([id_prefix, str(id)]), password,
                                                                      exch_gateway_ip, random_port))
    f.write("\napitstlogin {0} {1} {2} {3} >> hkex_login_test.txt".format("".join([id_prefix, str(id)]), password,
                                                                      exch_gateway_ip, random_port))
    f.write("\necho **************************************** >> hkex_login_test.txt")
    f.write("\nsleep 3\n")

f.close()




