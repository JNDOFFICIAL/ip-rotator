#!/usr/bin/python

import logging
import ConfigParser
import sys

l = logging.getLogger()
config = ConfigParser.ConfigParser()
config.read("ip-rotator.cfg")
__version__ = "0.1.0"

class my_params:
	try:
		#Main
		rotate_time = config.getint('main', 'rotate.time')
		ip_list = eval(config.get('main', 'ip.list'))
		switch = eval(config.get('main', 'switch'))
		outgoing_ip = config.get('main', 'outgoing.ip')
		flow_tos_bits = config.getint('main', 'flow.tos_bits')
		flow_priority = config.getint('main', 'flow.priority')
		flow_prefix = config.get('main', 'flow.prefix')
		flow_port=eval(config.get('main', 'flow.port'))
		
		#Opendaylight
		odl_user = config.get('opendaylight', 'user')
		odl_password = config.get('opendaylight', 'password')
		odl_server = config.get('opendaylight', 'server')

		#Logging
		log_level = ['INFO', config.get('main', 'log.level')][config.get('main', 'log.level') != '']
		log_file = ['ip_rotator.log', config.get('main', 'log.file')][config.get('main', 'log.file') != '']
		log_format = '%(asctime)-15s %(levelname)-7s [%(threadName)-10s] (%(module)s::%(funcName)s) [L:%(lineno)d] %(message)s'
		log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
	except ConfigParser.NoOptionError as e:
		print e
		sys.exit(1)
	except Exception as e:
		print e
		sys.exit(1)

params = my_params()

def setup_logging():
	logging.basicConfig(format=params.log_format, filename=params.log_file)
	l.setLevel(logging.__dict__["_levelNames"][params.log_level])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
