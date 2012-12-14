import os
from datetime import datetime, timedelta
from supervision.website.config import *

def read_status(status_type='current'):
	""" Return a dictionary representing the current or previous status.
	    If the status file is not found, return an empty dictionaty.

	    status_type : 'current' or 'previous'
	"""
	status = {
		# Start and end date of the whole process
		'start_process_date': None,
		'end_process_date': None,
		# Status per host
		'hosts': {
			# 'host': {
			#    'website': url checked,
			#    'start_process_date': when the check start
			# 	 'end_process_date': when the check stop
			#    'response_time': timedelta
			#    'http_code': response's HTTP code (200, 404, ...)
			#  },
			#  ...
		}
	}

	file_path = '%s/sitemonitor.%s.status' % (REPORTS_PATH, status_type)
	
	if not os.path.isfile(file_path):
		return {}

	with open(file_path, 'r') as f:
		lines = f.read().split('\n')

		# Read information from the status file
		begin_date, end_date, hosts = None, None, {}

		for line in lines:
			line = line.strip()

			if line.startswith('BEGIN_DATE:'):
				# BEGIN_DATE:1355243029
				timestamp = int(line[len('BEGIN_DATE:'):])
				status['start_process_date'] = datetime.fromtimestamp(timestamp)

			elif line.startswith('END_DATE:'):
				# END_DATE:1355243030
				timestamp = int(line[len('END_DATE:'):])
				status['end_process_date'] = datetime.fromtimestamp(timestamp)

			elif line.startswith('HOST:'):
				# HOST:http://www.asilax.fr;200;1355243029;1355243029
				infos_line = line[len('HOST:'):]
				website, http_code, start_timestamp, end_timestamp = infos_line.split(';')
				start_process_date = datetime.fromtimestamp(int(start_timestamp))
				end_process_date = datetime.fromtimestamp(int(end_timestamp))
				status['hosts'][website] = {
					'website': website,
					'start_process_date': start_process_date,
					'end_process_date': end_process_date,
					'response_time': end_process_date - start_process_date,
					'http_code': http_code
				}



	return status

def process_report(current_status, previous_status):
	""" Process current and previous status, generate TXT/HTML reports and send emails """
	has_change = False # say a there is a change between previous and current status

	start_process_date_str = current_status['start_process_date'].strftime('%Y/%m/%d %H:%M:%S')
	end_process_date_str = current_status['end_process_date'].strftime('%Y/%m/%d %H:%M:%S')
	process_time_str = str(current_status['end_process_date'] - current_status['start_process_date'])

	host_keys = current_status['hosts'].keys()
	host_keys.sort()

	status2hosts = {
		'OK': [],
		'KO': [],
		'SLOW': []
	}

	for key in host_keys:
		host = current_status['hosts'][key]
		
		# Compute status : OK, SLOW or KO, and populate status2hosts dictionary
		status_ok = host['http_code'] in OK_STATUSES
		status_ok_exception = OK_STATUSES_PER_HOST.get(key, [])

		if status_ok or status_ok_exception:
			status = 'OK'

			# Website is slow ?
			if host['response_time'] > timedelta(seconds=SLOW_THRESHOLD):
				status = 'SLOW'

			# OK status exception ?
			if status_ok_exception:
				host['http_code'] += ' (exception)'
			
		else:
			status = 'KO'

		status2hosts[status].append(host)

		# Change from the previous status ?
		# -> if the website is new or if the HTTP code has changed
		previous_host = previous_status['hosts'].get(key, None)
		if previous_host is None or previous_host['http_code'] != host['http_code']:
			has_change = True

	# Generate TEXT report
	with open('%s/report.txt' % REPORTS_PATH, 'w') as f:

		f.write('Start date : %s\n' % start_process_date_str)
		f.write('End date : %s\n' % end_process_date_str)
		f.write('Process time : %s\n' % process_time_str)

		for status in ['KO', 'SLOW', 'OK']:

			if not status2hosts.get(status, []):
				continue

			f.write('\n\nSTATUT : %s\n' % status)
			for host in status2hosts[status]:
				f.write('%s : response time = %s : HTTP code : %s\n' % (
					host['website'],
					host['response_time'],
					host['http_code']
					)
				)

	# Generate HTML report
	with open('%s/report.html' % REPORTS_PATH, 'w') as f:

		f.write('<div><strong>Start date</strong> : %s</div>\n' % start_process_date_str)
		f.write('<div><strong>End date</strong> : %s</div>\n' % end_process_date_str)
		f.write('<div><strong>Process time</strong> : %s</div>\n' % process_time_str)

		f.write('\n\n')
		f.write('<table id="websites">\n')
		f.write('<tr>\n')
		f.write('<th>Status</th><th>Host</th><th>Response time</th><th>HTTP code</th>\n')
		f.write('</tr>\n')

		for status in ['KO', 'SLOW', 'OK']:

			if not status2hosts.get(status, []):
				continue
			
			for host in status2hosts[status]:
				f.write('<tr class="%s">\n' % status)
				f.write('<td>%s</td><td>%s</td><td>%s</td><td>%s</td>\n' % (
					status,
					host['website'],
					host['response_time'],
					host['http_code']
					)
				)
				f.write('</tr>\n')
			
		f.write('</tr>\n')
		f.write('</table> \n')

	# Send email
	"""
	##### Mail configuration #####
	# Do you want reports by email ?
	MAIL_SEND = True
	# Send an email only when something change ?
	MAIL_SEND_ONLY_ON_CHANGE = True
	# Mail settings
	MAIL_SEND_FROM = 'supervisor@website.com'
	MAIL_SEND_TO = 'supervisor@website.com'
	MAIL_SUBJECT = 'Websites supervision report'
	# body format values are 'txt' and 'html'
	MAIL_BODY_FORMAT = 'txt'
	"""

if __name__ == '__main__':
	current_status = read_status(status_type='current')
	previous_status = read_status(status_type='previous')

	import pprint
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(current_status)

	process_report(current_status, previous_status)







