#~TestCaseName: logExceptions
#~TestCaseSummary: This is a library module for storing a master list of logfile exceptions

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import re

def logExceptions():
    logExceptions = [
        # Ignore messages from guard server.
        re.compile( r'.*\| guardserv.exe/(SIM|PROD) \|.*', re.I ),
        # Ignore messages from guardian.
        re.compile( r'.*\| guardian.exe/(SIM|PROD) \|.*', re.I ),
        # This message is not an error that should fail this test.
        re.compile( r'.*License not received, trying again.*', re.I ),
        # Ignore Limit Request messages.
        re.compile( r'.* Limit request failed.*', re.I ),
        # This message is caused by a known defect; and should be removed once PCR 97315 is fixed.
        re.compile( r'.*In VIAMessaging ConsumerThread.*Cannot send message.*Session is not active.*', re.I ),
        # Ignore server up/down messages.
        re.compile( r'.* SERVER is .*', re.I ),
        # Ignore client login messages.
        re.compile( r'.* license.*', re.I ),
        # Ignore client accepted login messages.
        re.compile( r'.* accepted my login .*', re.I ),
        # Ignore localStatus messages.
        re.compile( r'.*TT_CLIENT_.*', re.I ),
        # Ignore preferred/active server messages.
        re.compile( r'.*TT_NO_CLIENT.*', re.I ),
        # Ignore client connection messages.
        re.compile( r'.* closed connection.*', re.I ),
        # Ignore risk server messages.
        re.compile( r'.* Risk server ip .*', re.I ),
        # Ignore product table messages.
        re.compile( r'.* product table.*', re.I ),
        # Ignore currency table messages.
        re.compile( r'.* currency table .*', re.I ),
        # Ignore going online messages.
        re.compile( r'.* Going online .*', re.I ),
        # Ignore DH params messages.
        re.compile( r'.* DH params.*', re.I ),
        # Ignore OpenExchangePrices messages.
        re.compile( r'.* OpenExchangePrices.*', re.I ),
        # ignore RequestTimeoutTCB messages
        re.compile( r'.* RequestTimeoutTCB.*', re.I ),
        # Ignore manual server shutdown messages.
        re.compile( r'.* normal termination.*', re.I ),
        # Ignore RQ36: invalid transaction messages.
        re.compile( r'.* RQ36: invalid transaction type .*', re.I ),
        # Ignore [DA120] missing underlyingBasic messages.
        re.compile( r'.* missing underlyingBasic.*', re.I ),
        # Ignore [DA122] missing classBasic messages.
        re.compile( r'.* missing classBasic.*', re.I ),
        # Ignore querying greeks messages.
        re.compile( r'.* Error querying current option greeks .*', re.I ),
        # Ignore Client App Connection ID mismatch messages.
        re.compile( r'.* Connection ID mismatch.*', re.I ),
        # Ignore client status messages.
        re.compile( r'.* consecutive client status messages .*', re.I ),
        # Ignore bad Cabinet Price Data from SGX Exchange
        re.compile( r'.* but not equal its cabinet price.*', re.I ),
        # Ignore Exchange-side disconnects
        re.compile( r'.* logout message received from host.*', re.I )
        ]
    return logExceptions
