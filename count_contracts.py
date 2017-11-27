from pyrate.manager import Manager
ps = Manager.getPriceSession()
pp = ps.getProducts()
contract_count = 0
for p in pp:
    cc = ps.getContracts(p)
    contract_count += len(cc)

print 'Number of contracts = ' + str(contract_count)
