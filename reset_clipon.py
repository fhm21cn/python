/bin/env python

import os
import sys
import getopt
#import re
import telnetlib 

def do_telnet(Host, username, password, finish, commands):
    tn = telnetlib.Telnet(Host, port=23, timeout=10)
#	tn.set_debuglevel(2)
     
    tn.read_until('login: ')
    tn.write(username + '\n')
    
    tn.read_until('password: ')
    tn.write(password + '\n')
      
    tn.read_until(finish)
    for command in commands:
        tn.write('%s\n' % command)
    
    tn.read_until(finish)
    tn.close()


def usage():
    	print ('reset_clipon.py <-h> <NE> <shelf> <slot> <type>')

try:
    opts,args = getopt.getopt(sys.argv[1:],"h", ["help"])
    for opt,arg in opts:  
    	if opt in ("-h", "--help"):  
        	usage();  
          	sys.exit(1); 
    
    ne = args[0]
    shelf = int(args[1])
    slot = int(args[2])

    print ne, shelf, slot

    username = 'root'
    password = 'ALu12#'
    finish = ':~$ '
    commands = ['cd /pureNeApp/EC']

    do_telnet(ne, username, password, finish, commands)



except getopt.GetoptError:
	sys.exit()

    

