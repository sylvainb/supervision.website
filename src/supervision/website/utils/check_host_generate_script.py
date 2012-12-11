import sys
from supervision.website.config import *

def generate_sh_script():
	# Generate the sh script using our custom configuration

	with open('check_hosts.sh.tmpl', 'r') as f:
		script = f.read()
	
	script = script.replace('TO_BE_REPLACE_TIMEOUT', str(TIMEOUT))
	script = script.replace('TO_BE_REPLACE_HOSTS', '\n'.join((['"%s" \\' % uri for uri in WEBSITE_URIS])))
	script = script.replace('TO_BE_REPLACE_REPORTS_PATH', REPORTS_PATH)

	with open('check_hosts.sh', 'w') as f:
		f.write(script)


if __name__ == '__main__':
	generate_sh_script()