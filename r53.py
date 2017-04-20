#!/usr/bin/python
import os
import sys
import time
import boto
import requests
import datetime
import logging

logger = logging.getLogger('DNS update')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_conf():
    config = {}
    config['check_interval'] = int(os.getenv("CHECK_INTERVAL", 60))
    config['root'] = os.getenv("ROOT", "root")     
    config['subdomains'] = os.getenv("SUBDOMAINS", "").split(",")

    return config

def fetch_old_ip(zone, root):
	try:
        	a_record = zone.get_a(root)
        	return a_record.resource_records[0]
	except:
		return None

def fetch_ip():
	headers = { "User-Agent": "curl/7.21.2 (i386-pc-win32) libcurl/7.21.2 OpenSSL/0.9.8o zlib/1.2.5" }
        r = requests.get("http://icanhazip.com", headers=headers)
        return r.text.strip()

def process():
	config = get_conf() 
	conn = boto.connect_route53()
	root = config["root"]
	subdomains = config["subdomains"]
	zone = conn.get_zone(root)
	ipaddr = fetch_ip()
	for subdomain in subdomains:
		name = '.'.join([subdomain,root])
		oldip = fetch_old_ip(zone, name)
		if oldip != ipaddr:
			if oldip == None:
    				try:
					logger.info("Creating A Record for: " + name + " with IP: " + str(ipaddr))
					zone.add_a(name, ipaddr, ttl=60)
				except Exception as e:
					logger.error(e)
			else:
				try:
					logger.info("Updating IP Address, old: " + str(oldip) + " new: " + str(ipaddr))
					zone.update_a(name, ipaddr)
				except Exception as e:
					logger.error(e)
		else:
	        	continue	


if __name__ == "__main__":
  config = get_conf() 

  logger.info("Processing records in root domain: " + config['root'])
  logger.info("Maintaining IP's for subdomains: " + str(config['subdomains']))
  logger.info("Check Interval: " + str(config['check_interval']))

  while True:
	process()
	time.sleep(config['check_interval'])
