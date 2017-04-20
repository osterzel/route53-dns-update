#!/usr/bin/env python

import os
import r53 
import unittest
import tempfile

class ServerTestCase(unittest.TestCase):

	def test_config_setup(self):
		os.environ["CHECK_INTERVAL"] = "30"
		os.environ["ROOT"] = "testdomain.com"
		os.environ["SUBDOMAINS"] = "subdomain1"

		config = r53.get_conf()
		self.assertEqual(config['root'], "testdomain.com")	
		self.assertEqual(config['subdomains'], ["subdomain1"])	
		self.assertEqual(config['check_interval'], 30)	
		

