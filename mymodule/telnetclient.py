#!/usr/bin/env python

import os
import sys
import logging
import time
import getopt
import telnetlib

#logging.basicConfig(level=logging.NOTSET)

__all__ = ["TelnetClient"]


class TelnetClient:
    def __init__(self, host, port=23, user='root', password='ALu12#', ver=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.verbose = ver
        self.tn = None
        self.login()

    def __del__(self):
        self.logout()

    def logout(self):
        self.tn.write(b"exit\n")

    def login(self):
        self.tn = telnetlib.Telnet(self.host, self.port, 5)
        if self.verbose:
            self.tn.set_debuglevel(1)

        self.tn.read_until(b'login: ')
        self.tn.write(self.user.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ")
        self.tn.write((self.password + "\n").encode('utf-8'))
        self.tn.read_until(":~# ".encode('utf-8'))

        cmdres = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in cmdres:
            logging.debug('%s login successfully' % self.host)
            return True
        else:
            logging.debug('%s login failed' % self.host)
            return False

    def read_until(self, command):
        self.tn.read_until(command)

    def execute_command(self, command):

        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)

#        command_result = self.tn.read_very_eager().decode('ascii')
#        logging.debug('command result:\n%s' % command_result)


def usage(command):
    print('{} [-v] <NE> '.format(command))
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        usage(os.path.basename(sys.argv[0]))

    try:
        opts, args = getopt.getopt(sys.argv[1:], "v", ["verbose"])
    except getopt.GetoptError:

        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            verbose = True

    ne = args[0]

    te = TelnetClient(ne, 23, "root", "ALu12#", verbose)
    te.execute_some_command('ls -l')
    te.logout()

