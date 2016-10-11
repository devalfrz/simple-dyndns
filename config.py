# config.py:

from simpledyndns import SimpleDynDnsServer
from simpledyndns import Hostmonster

SIMPLE_DYNDNS_SERVER = SimpleDynDnsServer(
    known_server='http://behuns.com/simple-dyndns-server/',
    known_server_key='dynip',
    server_alias='talullah.behuns.com'
)

DOMAINS = [
    Hostmonster(
        domain='behuns.com',
        username='behunsco',
        password='2+3=4$devHuns%56F8#$%365',
        records=[
            'talullah',
        ]
    ),
]
