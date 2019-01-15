#!/usr/bin/env python

import getopt
import sys
import time
from mymodule.telnetclient import TelnetClient


def usage():
    print('reset_clipon.py [-v] <NE> <shelf> [times]')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
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
    shelf = int(args[1])
    times = int(5)

    if shelf > 8:
        print('invalid sh{}'.format(shelf))
        sys.exit(1)

    if len(args) > 2:
        times = int(args[2])
        if times > 500:
            print('too many times[{}]'.format(times))
            sys.exit(1)

#    print ne, shelf, slot

    reset_cmd = '/pureNeApp/EC/screen -S console -X stuff "clipon agt shelf reset ' + str(shelf) +' appl \n"'
    te = TelnetClient(ne, 23, "root", "ALu12#", verbose)
    for i in range(1, times):
        te.execute_some_command(reset_cmd)
        time.sleep(20)
        i = i + 1

    te.logout()


