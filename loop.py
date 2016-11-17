#!/usr/bin/python

"""
This is the main loop of the system. Will check for a change
of ip address every 60 seconds and update if it has changed.
"""
from time import sleep
from config import *
from datetime import datetime
import sys, os


class Log:
    def __init__(self,log_file='/var/log/simpledyndns/error.log'):
        self.log_file = log_file

    def write(self,message):
            """
            Write in log file
            """

            # Get time string
            now = datetime.now().strftime("%a %b %d %H:%M:%S.%f")

            try:
                # Create a log directory
                os.makedirs(os.path.dirname(self.log_file))
            except OSError:
                pass

            # Append to log

            f = open(self.log_file,'a')
            f.write("[%s] %s\n" % (now,message))
            f.close()


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
                print "Error connecting to server"
                log.write("Error connecting to server")
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

            sleep(SIMPLE_DYNDNS_SERVER.timer)

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
