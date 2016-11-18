#!/usr/bin/python

"""
This is the main loop of the system. Will check for a change
of ip address every 30 seconds and update if it has changed.
"""
from time import sleep
from config import *
from datetime import datetime
from log import Log
import sys, os


if __name__ == '__main__':

    # Initialize log

    log = Log()
    log.write('Initializing...')
    first = True

    # Wait for system boot

    sleep(60)

    while(True):
        try:
            current_ip = SIMPLE_DYNDNS_SERVER.get_current_ip()
            last_ip = SIMPLE_DYNDNS_SERVER.get_last_ip()
            if not current_ip or not last_ip:
                print "Error connecting to known server"
                log.write("Error connecting to known server")
            else:
                print "Last IP:    %s" % last_ip
                print "Current IP: %s" % current_ip
                if first:
                    log.write("Last IP:    %s" % last_ip)
                    log.write("Current IP: %s" % current_ip)
                    first = False

                if current_ip != last_ip:

                    # Set new IP address

                    print "Updating Records..."
                    log.write("Updating Records...")

                    for domain in DOMAINS:
                        domain.login()
                        domain.update_all(current_ip)
                        new_ip = SIMPLE_DYNDNS_SERVER.set_new_ip(current_ip)

                    print "New IP:     %s" % new_ip
                    log.write("New IP: %s" % new_ip)

        except KeyboardInterrupt:

            # Debugging

            print "Bye!"
            sys.exit(0)

        except:

            # Catch any exception and get information in the log

            exception = sys.exc_info()[0]
            message = "Exception: %s" % (exception,)
            log.write(message)

            print message

        sleep(SIMPLE_DYNDNS_SERVER.timer)


