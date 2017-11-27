import os, socket, win32api, _winreg

ip_addr = None

''' get ip address '''
for i in socket.getaddrinfo(socket.gethostname(), None):
    if ':' not in str(i):
        ip_addr = str(i).split('\'')[-2]

''' get currently-logged-in user '''
username = win32api.GetUserName()

''' get gw flavour name '''
try:
    install_root_reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                          r'SOFTWARE\Wow6432Node\Trading Technologies\Installation')
    install_root_reg_value = _winreg.QueryValueEx(install_root_reg_key, 'INSTALLROOT')
except:
    install_root_reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                          r'SOFTWARE\Trading Technologies\Installation')
    install_root_reg_value = _winreg.QueryValueEx(install_root_reg_key, 'INSTALLROOT')

install_path = list(install_root_reg_value)[0]

non_gw_directories = ['auditfiles', 'bin', 'config', 'datfiles', 'docs', 'Guardian', 'logfiles', 'ttchron', 'ttm',
                      'sounds', 'x_study', 'x_trader']
for directory in os.listdir(install_path):
    if not any(directory_name in directory for directory_name in non_gw_directories):
        gw_flavour_name = directory

''' read in pyrate.cfg '''
pyrate_cfg_source_path = r'T:\SQE\Users\Chris_Maurer\pyrate_Configs\sgx'
pyrate_config_source_file_name = 'pyrate.cfg'
pyrate_config_source_file = pyrate_cfg_source_path + '\\' + pyrate_config_source_file_name



print 'your ip address is', ip_addr
print 'you are', username
print 'your gateway is installed in', install_path
print 'your gateway flavour name is', gw_flavour_name
print 'your pyrate.cfg file is', pyrate_config_source_file