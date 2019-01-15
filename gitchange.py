#!/usr/bin/env python

import os
import sys
import time
import getopt
import re
import commands
import subprocess


def usage():
		print ("Usage:")
		print ("gitchange.py <add/del> 'CODE' <file> [commitid]\n")
		print ("Example: gitchange.py del ' PTP_CLK_STATE_PHASETRACKING' Ptp1588Clk.cc ")
		print ("         gitchange.py del ' PTP_CLK_STATE_PHASETRACKING' Ptp1588Clk.cc 17f09bc")
		print ("         search from latest or commitid[17f09bc]")
		sys.exit(1)

def get_changeid(code, file):
#	git log --oneline Ptp1588Log.cc |awk '{print $1}'

	command = "git log --oneline " + file + "|awk '{print $1}' "
  	output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(out, err) = output.communicate()
	return out

def git_show(commitid, file):

	command = "git show " + commitid + " " + file
#	print ("git_show cmd {}".format(command))
  	output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(out, err) = output.communicate()
	return out
	

if __name__ == '__main__':
	if len(sys.argv) < 4: usage()

	method= str(sys.argv[1])
	code = str(sys.argv[2])
	file = str(sys.argv[3])
	startid=""

	if len(sys.argv) > 4: 
		startid = str(sys.argv[4])

	if method != 'add' and method != 'del':
		usage(); 

	commitids =get_changeid(code,file).split()
#	print commitids

	latestid=''
	find = False
	flag = False

	for commitid in commitids:

		if len(startid) == 0 or startid == latestid :	
			flag = True
		
		if not flag:
			latestid = commitid
			continue
#		command = git diff d998a2d 5befda8 Ptp1588Extif.cc 
		command = "git diff " + commitid + " " + latestid + " " + file 
#		print("command is: {}".format(command))
#		lastid = commitid
  		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		while True:  
			linebuf = p.stdout.readline()  
#			print linebuf
			if linebuf == '' and p.poll() != None:  
				break
			elif  linebuf.find(code) > 0 and linebuf[0:1]:
				if (method == 'add' and linebuf[0:1] == '+') \
				or (method == 'del' and linebuf[0:1] == '-'):
					find=True
					break

		if (find):
			break

		latestid = commitid

	if (find):
		print('code changed from commitid {} '.format(latestid))
		print('get more infomation use:')
		print('git show {} {}'.format(latestid,file))
#		print(git_show(latestid, file))

	else:
		print ("not found {} code[{}] in {}".format(method, code, file))



