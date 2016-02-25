#!/usr/bin/python

"""



"""
from time import sleep
from config import *

if __name__ == '__main__':
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

