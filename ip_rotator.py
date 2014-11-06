#!/usr/bin/python

from utils import l, params, setup_logging, __version__
from odl import opendaylight
import sys
import time
import re

ips = ( str(x) for x in params.ip_list )

def ip():
	global ips
	
	try:
		return ips.next()
	except StopIteration:
		ips = ( str(x) for x in params.ip_list )
		return ips.next()

def main():
	l.info("Starting IP Rotator version %s" % (__version__))

	odl = opendaylight()

	while True:
		ip_address = ip()		

		for switch in params.switch:
			flow = {
				'name_in': '%s_in_%s' % (params.flow_prefix, ip_address.replace('.','_')),
				'name_out': '%s_out_%s' % (params.flow_prefix, ip_address.replace('.','_')),
				'priority': params.flow_priority
			}
			current_flows = odl.get_flow(node={'id': switch})
			
			#Check priority of current flows
			for name, value in current_flows.items():
				if re.search(params.flow_prefix, name):
					if flow['priority'] == value['priority']:
						flow['priority'] = str(int(value['priority'])+1)

			#Add new flows
			try:
				for port in params.flow_port:
					odl.add_flow(name=flow['name_in']+'_'+port,
						installInHw='true',
						node={"id":switch, "type": "OF"},
						priority=flow['priority'],
						etherType='0x800',
						protocol='tcp',
						nwDst=ip_address,
						tpSrc=port,
						actions=['SET_NW_DST='+params.outgoing_ip, 'HW_PATH']
					)

					odl.add_flow(name=flow['name_out']+'_'+port,
						installInHw='true',
						node={"id":switch, "type": "OF"},
						priority=flow['priority'],
						etherType='0x800',
						protocol='tcp',
						tpDst=port,
						tosBits=params.flow_tos_bits,
						actions=['SET_NW_SRC='+ip_address, 'HW_PATH']
					)
			finally:
				l.info("I've set IP %s" % (ip_address))
				for name, value in current_flows.items():
					odl.delete_flow(node={"id":switch}, name=name)
			
		time.sleep(params.rotate_time)

# setup logging
try:
    setup_logging()
except Exception, e:
    print "Error starting logger: %s" % str(e)

if __name__ == "__main__":
	main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
