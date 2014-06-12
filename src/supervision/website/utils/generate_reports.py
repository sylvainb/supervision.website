#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from supervision.website.config import *

STATUS_OK = 'OK'
STATUS_KO = 'KO'
STATUS_SLOW = 'SLOW'


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
            #    'status': STATUS_OK, STATUS_SLOW, STATUS_KO
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
                status['start_process_date'] = \
                    datetime.fromtimestamp(timestamp)

            elif line.startswith('END_DATE:'):
                # END_DATE:1355243030
                timestamp = int(line[len('END_DATE:'):])
                status['end_process_date'] = datetime.fromtimestamp(timestamp)

            elif line.startswith('HOST:'):
                # HOST:http://www.asilax.fr;200;1355243029;1355243029
                infos_line = line[len('HOST:'):].split(';')
                website = infos_line[0]
                http_code = infos_line[1]
                start_timestamp = infos_line[2]
                end_timestamp = infos_line[3]
                start_process_date = \
                    datetime.fromtimestamp(int(start_timestamp))
                end_process_date = datetime.fromtimestamp(int(end_timestamp))
                response_time = end_process_date - start_process_date

                # Compute status : OK, SLOW or KO,
                # and populate status2hosts dictionary
                status_ok = http_code in OK_STATUSES
                if website in WEBSITE_URLS_DICT:
                    ok_status_exceptions = \
                        WEBSITE_URLS_DICT[website]['ok_status_exceptions']
                    status_ok_exception = http_code in ok_status_exceptions
                else:
                    status_ok_exception = False

                if status_ok or status_ok_exception:
                    check_status = STATUS_OK
                    if website in WEBSITE_URLS_DICT:
                        slow_threshold = \
                            WEBSITE_URLS_DICT[website]['slow_threshold']
                    else:
                        slow_threshold = DEFAUL_SLOW_THRESHOLD
                    # Website is slow ?
                    if response_time > timedelta(seconds=slow_threshold):
                        check_status = STATUS_SLOW
                else:
                    check_status = STATUS_KO

                # OK status exception ?
                if status_ok_exception:
                    # add a message for the report
                    http_code += ' (exception)'

                status['hosts'][website] = {
                    'website': website,
                    'start_process_date': start_process_date,
                    'end_process_date': end_process_date,
                    'response_time': response_time,
                    'http_code': http_code,
                    'status': check_status
                }

    return status


def process_report(current_datas, previous_datas):
    """ Process current and previous status,
        generate TXT/HTML reports and send emails """

    # say a there is a change between previous and current status
    has_change = False

    start_process_date_str = \
        current_datas['start_process_date'].strftime('%Y/%m/%d %H:%M:%S')
    end_process_date_str = \
        current_datas['end_process_date'].strftime('%Y/%m/%d %H:%M:%S')
    process_time_str = str(current_datas['end_process_date']
                           - current_datas['start_process_date'])

    host_keys = current_datas['hosts'].keys()
    host_keys.sort()

    status2hosts = {
        STATUS_OK: [],
        STATUS_KO: [],
        STATUS_SLOW: []
    }

    for key in host_keys:
        host = current_datas['hosts'][key]

        # Keep some information about the previous host
        previous_host = previous_datas['hosts'].get(key, None)
        if previous_host is not None:
            previous_http_code = previous_host['http_code']
            previous_status = previous_host['status']
        else:
            previous_http_code = 'unknown'
            previous_status = 'unknown'
        host['previous_http_code'] = previous_http_code
        host['previous_status'] = previous_status

        status = host['status']
        status2hosts[status].append(host)

        # Change ?
        if has_change:
            # There was a change for a previous host
            pass
        elif status != previous_status \
            and (status == STATUS_KO
                 or previous_status == STATUS_KO):
            # ('OK', 'KO') - now up (was down)
            # ('SLOW', 'KO') - now up (was down)
            # ('KO', 'OK') - now down (was up)
            # ('KO', 'SLOW') - now down (was up)
            has_change = True
        elif status == previous_status == STATUS_SLOW:
            # The website remains slow
            # ('SLOW', 'SLOW')
            has_change = True
        else:
            # ('OK', 'OK')
            # ('KO', 'KO')
            # ('OK', 'SLOW')
            # ('SLOW', 'OK')
            pass

    # Generate TEXT report
    with open('%s/report.txt' % REPORTS_PATH, 'w') as f:

        f.write('Start date : %s\n' % start_process_date_str)
        f.write('End date : %s\n' % end_process_date_str)
        f.write('Process time : %s\n' % process_time_str)

        for status in [STATUS_KO, STATUS_SLOW, STATUS_OK]:

            if not status2hosts.get(status, []):
                continue

            f.write('\n\nSTATUS : %s\n' % status)
            for host in status2hosts[status]:
                line_text = '%s : response time = %s : HTTP code : %s : ' \
                            'Previous status : %s : Previous HTTP code : %s\n'
                f.write(line_text % (
                    host['website'],
                    host['response_time'],
                    host['http_code'],
                    host['previous_status'],
                    host['previous_http_code']
                    )
                )

    # Generate HTML report
    with open('%s/report.html' % REPORTS_PATH, 'w') as f:

        f.write('<div><strong>Start date</strong> : %s</div>\n' % (
            start_process_date_str
        ))
        f.write('<div><strong>End date</strong> : %s</div>\n' % (
            end_process_date_str
        ))
        f.write('<div><strong>Process time</strong> : %s</div>\n' % (
            process_time_str
        ))

        f.write('\n\n')
        f.write('<table id="websites">\n')
        f.write('<tr>\n')
        line_html = '<th>Status</th><th>Host</th><th>Response time</th>' \
                    '<th>HTTP code</th><th>Previous status</th>' \
                    '<th>Previous HTTP code</th>\n'
        f.write(line_html)
        f.write('</tr>\n')

        for status in [STATUS_KO, STATUS_SLOW, STATUS_OK]:

            if not status2hosts.get(status, []):
                continue

            for host in status2hosts[status]:
                f.write('<tr class="%s">\n' % status)
                status2color = {
                    STATUS_KO: 'red',
                    STATUS_SLOW: 'orange',
                    STATUS_OK: 'green'
                }
                status_text = '<span style="color:%s">%s</span>' % (
                    status2color.get(status),
                    status
                )
                previous_status_text = '<span style="color:%s">%s</span>' % (
                    status2color.get(host['previous_status']),
                    host['previous_status']
                )
                line_text = '<td>%s</td><td>%s</td><td>%s</td>' \
                            '<td>%s</td><td>%s</td><td>%s</td>\n'
                f.write(line_text % (
                    status_text,
                    host['website'],
                    host['response_time'],
                    host['http_code'],
                    previous_status_text,
                    host['previous_http_code']
                    )
                )
                f.write('</tr>\n')

        f.write('</tr>\n')
        f.write('</table> \n')

    # Send email
    send_report_by_mail(has_change)


def send_report_by_mail(has_change):
    """ If asked in the configuration, send report by mail.
        has_change : boolean, True if there are some changes, else False
    """

    if not MAIL_SEND:
        # Don't send mail
        return

    if not has_change and MAIL_SEND_ONLY_ON_CHANGE:
        # No changes and send mail only on change
        return

    # Create message container - the correct MIME type is multipart/alternative
    msg = MIMEMultipart('alternative')
    msg['Subject'] = MAIL_SUBJECT
    msg['From'] = MAIL_SEND_FROM
    msg['To'] = MAIL_SEND_TO

    # Create the body of the message (a plain-text and an HTML version).
    # plain-text
    ftext = open('%s/report.txt' % REPORTS_PATH, 'r')
    text = ftext.read()
    ftext.close()
    # html
    fhtml = open('%s/report.html' % REPORTS_PATH, 'r')
    html = """\
    <html>
      <head></head>
      <body>
        %s
      </body>
    </html>
    """ % fhtml.read()
    fhtml.close()

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(SMTP)
    if SMTP_USER != '':
        s.login(SMTP_USER, SMTP_PASSWORD)
    s.sendmail(MAIL_SEND_FROM, MAIL_SEND_TO, msg.as_string())
    s.quit()


if __name__ == '__main__':
    current_status = read_status(status_type='current')
    previous_status = read_status(status_type='previous')

    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(current_status)

    process_report(current_status, previous_status)







