# config.py:

from simpledyndns import SimpleDynDnsServer
from simpledyndns import Hostmonster

SIMPLE_DYNDNS_SERVER = SimpleDynDnsServer(
    known_server='http://your-known-server.com/simple-dyndns-server/',#Replace with yor own server
    known_server_key='dyndns',#Replace with your own key
    server_alias='dev.my-domain.com'#Replace with your own unique alias
)

DOMAINS = [
    Hostmonster(
        domain='your-domain.com',#Replace with your own domain
        username='hostmonster-username',#Replace with your own username
        password='hostmonster-password',#Replace with your own password
        records=['@','www','dev','mail',]#Replace with your own records
    ),
]

