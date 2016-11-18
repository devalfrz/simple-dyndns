import mechanize
import urllib
import json
import sys
import pycurl
import time 
from StringIO import StringIO
from log import Log


class SimpleDynDnsServer(): 
    def __init__(self,known_server,known_server_key,server_alias):
        self.known_server=known_server
        self.known_server_key=known_server_key
        self.server_alias=server_alias
        self.br = mechanize.Browser()
        self.timer = 30
        self.log = Log()
                
    def get_current_ip(self):
        print "Getting current ip..."
        try:
            response = self.br.open(self.known_server,timeout=30)
            data = json.loads(response.read())
            return data['current_ip']
        except:
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()

        return False
        
    def get_last_ip(self):
        data = {
            'key'     : self.known_server_key,
            'server'  : self.server_alias,
            }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.known_server,endata,timeout=30)
            data = json.loads(response.read())
            return data['ip']
        except:
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()

        return False

    def set_new_ip(self,new_ip):
        data = {
            'key'     : self.known_server_key,
            'server'  : self.server_alias,
            'ip'      : new_ip,
            }
        endata = urllib.urlencode(data)
        try:
            response = self.br.open(self.known_server,endata)
            data = json.loads(response.read())
            return data['ip']
        except:
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()

        return False


class DynDnsHost():
    def __init__(self,domain,username,password,records=[]):
        self.domain = domain
        self.username = username
        self.password = password
        self.records = records
        self.br = mechanize.Browser()
        self.log = Log()
    
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
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()
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
            records = json.loads(response.read())
            self.old_records = records['data']
        except:
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()
            return False

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
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()
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
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)
            self.br = mechanize.Browser()
            return False

        return response
    
    def update_record(self,ip,record_name):
        try:
            if not hasattr(self, 'old_records'):
                self.get_old_records()    
            old_record = [item for item in self.old_records if (item.get('name') == record_name and item.get('type')=='A' and item.get('class')=='IN')]
            if old_record:
                self.delete_record(old_record[0])
            self.create_record(ip,record_name)
        except:
            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            self.log.write(message)

