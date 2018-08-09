all = []
dup = []
secid = "55=222455"
logfile = r"/var/log/debesys/OC_ice.log"

oc_log = open(logfile, 'r')
for line in oc_log.readlines():
    # if secid in line and "Send: 8=FIX.4.2" in line:
    if "Send: 8=FIX.4.2" in line:
        log_message = line.encode("ascii").split("\x01")
        for tag in log_message:
            if tag.startswith("11="):
                clordid = tag.split("=")[1]
                if clordid in all:
                    dup.append(clordid)
                all.append(clordid)
                print clordid
                # pprint(line.encode("ascii").replace("\x01", ";"))

if len(dup) > 0:
    print "\n\nDuplicates:\n", dup


