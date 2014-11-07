#!/usr/bin/python

import json
import urllib2
from utils import params, l

class opendaylight:
	def __auth(self, api_url):
		"""Auth to Opendaylight API"""
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(realm='opendaylight', uri=api_url,
			user=params.odl_user, passwd=params.odl_password)
	
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
	
		l.debug("Authorize to OpenDayLight Controller, url: %s" % api_url)


	def get_switch(self):
		"""Gets list of all switches"""
		result=[]
		api_url = "%s/controller/nb/v2/switchmanager/default/nodes" % (params.odl_server)

		self.__auth(api_url)

		req=urllib2.Request(url=api_url)
		f = urllib2.urlopen(req)
	
		for node in json.loads(f.read())['nodeProperties']:
			result.append(node['node']['id'])
	
			l.debug("Added node: %s" % node['node']['id'])
	
		return result

	def add_flow(self, **kwargs):
		api_url=("%s/controller/nb/v2/flowprogrammer/default/node/OF/%s/staticFlow/%s" %
			(params.odl_server, kwargs['node']['id'], kwargs['name']))

		self.__auth(api_url)

		request = urllib2.Request(api_url,data=json.dumps(kwargs))
		request.add_header('Content-Type', 'application/json')
		request.get_method = lambda: 'PUT'
		connection = urllib2.urlopen(request)
		
		l.debug("Flow:")
		for k,v in kwargs.items():
			l.debug("%s: %s" %(k,v))

		if connection.code != 200 and connection.code != 201:
			l.error("Error during adding flow, HTTP response: %s" % connection.code)
			raise Exception("Error during adding flow, HTTP response: %s" % connection.code)			

		return connection.code

	def delete_flow(self,**kwargs):
		api_url=("%s/controller/nb/v2/flowprogrammer/default/node/OF/%s/staticFlow/%s" %
			(params.odl_server, kwargs['node']['id'], kwargs['name']))

		self.__auth(api_url)

		request = urllib2.Request(api_url)
		request.get_method = lambda: 'DELETE'
		connection = urllib2.urlopen(request)

		if connection.code == 204:
			l.info("Flow has been deleted, name: %s" % kwargs['name'])
		else:
			l.error("Error during deleting flow entry, name: %s, http error: %s" % (kwargs['name'], connection.code))

	def get_flow(self, **kwargs):
		result={}

		api_url="%s/controller/nb/v2/flowprogrammer/default/node/OF/%s" % (params.odl_server, kwargs['node']['id'])

		self.__auth(api_url)

		request = urllib2.Request(api_url)
		request.add_header('Content-Type', 'application/json')
		connection = urllib2.urlopen(request)

		for k in json.loads(connection.read())['flowConfig']:
			result[k['name']]=k

		#Debug
		l.debug("Flows list:")
		for k,v in result.items():
			l.debug("Flow %s" % k)
			for flow_key,flow_value in v.items():
				l.debug("%s: %s" % (flow_key,flow_value))
			l.debug("")

		return result


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
