from communication import Email

Email(subject='results_2010-01-27_163320.txt',\
       sender='pyfmds.utils.communication',\
       recipient='logresults@ttportal.tradingtechnologies.com',\
       attachment=r'C:\workspace\Chris\src\TT\results_2010-01-27_163320.txt',\
       smtp_server='mail.int.tt.local').send()