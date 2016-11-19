#!/usr/bin/env

"""
Creates log file
"""
from datetime import datetime
import sys, os

class Log:
    def __init__(self,log_file='/var/log/simpledyndns/simpledyndns.log'):
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



