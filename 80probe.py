#!/usr/bin/env python

import argparse
import requests
from multiprocessing.pool import ThreadPool


class Probe80(object):

	def __init__(self, subdomain, domain, timeout=1):
		self.subdomain = subdomain
		self.domain = domain
		self.url = 'http://%s.%s' % (subdomain, domain)
		self.content = None
		self.timeout = timeout

	def __call__(self):
		try:
			r = requests.get(self.url, timeout=self.timeout)
		except Exception as e:
			return

		self.content = r.text


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain',
						help='Domain name to brute force (do not include any subdomains).',
						type=str,
						required=True)
	parser.add_argument('-w', '--wordlist',
					 	help='Path to subdomain wordlist.',
					 	type=str,
					 	required=True)
	parser.add_argument('-f', '--filter',
						help='Removes subdomains that contain filter text in the HTTP response.',
						type=str)
	parser.add_argument('-s', '--showBody',
						help='Prints the HTTP body from each request to stdout.',
						default=False,
						action='store_true')
	parser.add_argument('-t', '--timeout',
						help="Number of seconds to wait before HTTP request times out",
						type=int)
	args = parser.parse_args()

	# Open subdomain wordlist into list
	with open(args.wordlist) as f:
		lines = f.readlines()

	pool = ThreadPool(10)
	probes = [ Probe80(subdomain.strip(), args.domain, args.timeout) for subdomain in lines ]
	pool.map(lambda probe: probe(), probes)

	pool.close()
	pool.join()
	
	results = []

	# Loop through each probe discarding any problems that:
	#   1. probe.content is not set
	#   2. probe.content contains filter text
	for probe in probes:

		# If probe contains no content, move on ...
		if not probe.content:
			continue

		# If --filter is provided filter out any results that contain the
		# filtered word in the HTTP body. We don't care for failed responses
		if args.filter:
			if args.filter not in probe.content:
				results.append(probe)
		else:
			results.append(probe)				

	for probe in results:
		if args.showBody:
			print('[%s] ------------------------------------------- ' % probe.url)
			print(probe.content)
			print('\n')
		else:
			print(probe.url)
