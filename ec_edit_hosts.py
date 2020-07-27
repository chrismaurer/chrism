'''Edit Hosts file on Remote PC'''
hosts_file = r'c:\WINDOWS\system32\drivers\etc\hosts'
f = open(hosts_file, 'a')
f.write('\n172.17.250.110\tchifs02.int.tt.local')
f.write('\n172.17.250.114\tchimks01.int.tt.local')
f.write('\n172.17.250.117\tchiec01')
f.close()