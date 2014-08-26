#!/usr/bin/python

from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets
from boto.route53.zone import Zone
import requests
import time
import logging
import logging.handlers

zone_id = 'Z1E3MC35359WK5'
conn = Route53Connection()
domains = ['couch.moretour.co.uk.','sabnzb.moretour.co.uk.','sick.moretour.co.uk.','www.moretour.co.uk.']

r53_logging = logging.getLogger('Route53Updater')
r53_logging.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler('/dev/log')

r53_logging.addHandler(handler)

def main():

	while True:
		domain_ips = {}
		ip = requests.get('http://ip.42.pl/raw').text
		sets = conn.get_all_rrsets(zone_id)
		for rset in sets:
			domain_ips[rset.name] = rset.resource_records
		for k,v in domain_ips.iteritems():
			if k in domains:
				if v[0] != ip:
					#print k
					changes = ResourceRecordSets(conn, zone_id)
					delete_record = changes.add_change("DELETE", k, "A", 300)
					delete_record.add_value(v[0])
					create_record = changes.add_change("CREATE", k, "A", 300)
					create_record.add_value(ip)
					changes.commit()
					r53_logging.debug('Route53_Updater	Updated IP addresses')
				else:
					#print 'Nothing to update'
					r53_logging.debug('Route53_Updater	Nothing to update')
		time.sleep(600)

if __name__ ==  '__main__':
	main()	
