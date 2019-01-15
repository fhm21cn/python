#!/usr/bin/env python

import getopt
import sys
import time
from mymodule.telnetclient import TelnetClient


def usage():
    print('reset_lc.py [-v] <NE> <slot> <warm/cold>')
    sys.exit(1)


def do_reset(te, slot, type):

    cmd = '/pureNeApp/EC/ShellCmd'
    te.execute_command(cmd)

    te.tn.read_until(b'.#')

    cmd = '.bm.test 1'
    te.execute_command(cmd)
    te.read_until(b'.#')

    cmd = '.bm.reset ' +str(slot) + ' ' + type
    te.execute_command(cmd)
    te.read_until(b'.#')

    cmd = 'exit'
    te.execute_command(cmd)
    te.read_until(b':~# ')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "v", ["verbose"])
    except getopt.GetoptError:
        sys.exit()

    verbose = False
    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            verbose = True

    ne = args[0]
    slot = int(args[1])
    times = int(5)
    type = args[2]

    if slot > 100:
        print('invalid sh{}'.format(slot))
        sys.exit(1)
    if type != 'warm' and type != 'cold':
        print('invalid type {}'.format(type))
        sys.exit(1)

#    print ne, shelf, slot
    te = TelnetClient(ne, 23, "root", "ALu12#", verbose)
    do_reset(te, slot, type)
    te.logout()


