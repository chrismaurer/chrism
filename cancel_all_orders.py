import sys, requests, json, hashlib
from base64 import b64encode, encodestring
from requests.auth import HTTPBasicAuth

USER_ID = 162
API_KEY = "DM9gHznINtZB3YP/OILPwyznpHo="
API_PASS = "Debesy$12345678"

# USER_ID = 208
# API_KEY = "JBc36LuMgnxTvOqIz1I60SoWE9U="
# API_PASS = "Debesys12345678"

User = str(USER_ID)

username = str(User)
username += '/'
username += (API_KEY)
username += ':' + API_PASS

sign = 'Basic '
username = sign + b64encode(username)

print username

class CoinflexAuth(HTTPBasicAuth):
    def __init__(self, key):
        self.key = key

    def __call__(self, request):

        request.headers.update({
            'Authorization': self.key
        })
        return request


auth = CoinflexAuth(username)

r = requests.delete('https://demowebapi.coinflex.com/orders/', auth=auth)
print "\n Cancel all open orders:"
print r.json()
