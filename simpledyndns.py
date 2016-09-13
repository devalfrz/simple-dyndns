

import mechanize
import urllib
import json
import sys
import pycurl
import time 
from StringIO import StringIO


def __main__(argv):
    while(True):
        current_ip = SIMPLE_DYNDNS_SERVER.get_current_ip()
        last_ip = SIMPLE_DYNDNS_SERVER.get_last_ip()
        print "Last IP:    %s" % last_ip
        print "Current IP: %s" % current_ip
        if current_ip != last_ip:
            for domain in DOMAINS:
                domain.login()
                domain.update_all(current_ip)
                new_ip = SIMPLE_DYNDNS_SERVER.set_new_ip(current_ip)
            print "New IP:     %s" % new_ip
        sleep(SIMPLE_DYNDNS_SERVER.timer)

class SimpleDynDnsServer(): 
    def __init__(self,known_server,known_server_key,server_alias):
        self.known_server=known_server
        self.known_server_key=known_server_key
        self.server_alias=server_alias
        self.br = mechanize.Browser()
        self.timer = 30
                
    def get_current_ip(self):
        print "Getting current ip..."
        try:
            response = self.br.open(self.known_server)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        data = json.loads(response.read())
        return data['current_ip']
        
    def get_last_ip(self):
        data = {
            'key'     : self.known_server_key,
            'server'  : self.server_alias,
            }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.known_server,endata)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        data = json.loads(response.read())
        try:
            return data['ip']
        except KeyError:
            return ''

    def set_new_ip(self,new_ip):
        data = {
            'key'     : self.known_server_key,
            'server'  : self.server_alias,
            'ip'      : new_ip,
            }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.known_server,endata)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        data = json.loads(response.read())
        return data['ip']


class DynDnsHost():
    def __init__(self,domain,username,password,records=[]):
        self.domain = domain
        self.username = username
        self.password = password
        self.records = records
        self.br = mechanize.Browser()
    
    def update_record(self,ip,record_name):
        print "Update %s: %s" % (record_name,ip)

    def update_all(self,ip):
        self.get_old_records()
        for record in self.records:
            self.update_record(ip,record)

    def login(self):
        pass
    
    def get_old_records(self):
        pass

class Hostmonster(DynDnsHost):
    urls = {
        'login':'https://my.hostmonster.com/cgi-bin/cplogin',
        'records':'https://my.hostmonster.com/cgi/dm/zoneedit/ajax',
    }
    def login(self):
        try:
            self.br.open(self.urls['login'])
            self.br.select_form(name="l_login_form")
            self.br['ldomain'] = self.username
            self.br['lpass'] = self.password
            response = self.br.submit()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return response
    
    def get_old_records(self):
        print "Getting old records..."
        data = {
            'op'     : 'getzonerecords',
            'domain' : self.domain
            }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.urls['records'],endata)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        try:
            records = json.loads(response.read())
        except ValueError:
            return False
        self.old_records = records['data']
        return response

    def delete_record(self,record):
        print "Removing record %s..." % record['name']
        data = {
            'op'            : 'deletezonerecord',
            'domain'        : self.domain,
            'name'          : record['name'],
            'orig__name'    : record['name'],
            'address'       : record['address'],
            'orig__adress'  : record['address'],
            'ttl'           : record['ttl'],
            'orig__ttl'     : record['ttl'],
            'Line'          : record['Line'],
            'type'          : record['type']
        }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.urls['records'],endata)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return response

    def create_record(self,ip,record_name):
        print "Creating Record %s..." % record_name
        data = {
            'op'            : 'addzonerecord',
            'domain'        : self.domain,
            'name'          : record_name,
            'address_a'     : ip,
            'ttl'           : '14400',
            'type'          : 'A',
        }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.urls['records'],endata)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False
        return response
    
    def update_record(self,ip,record_name):
        if not hasattr(self, 'old_records'):
            self.get_old_records()    
        old_record = [item for item in self.old_records if (item.get('name') == record_name and item.get('type')=='A' and item.get('class')=='IN')]
        if old_record:
            self.delete_record(old_record[0])
        self.create_record(ip,record_name)


