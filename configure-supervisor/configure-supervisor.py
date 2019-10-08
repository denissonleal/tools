#!/usr/bin/python3

import argparse
import os.path
import subprocess

parser = argparse.ArgumentParser(description='Setup the supervisorctl.')
parser.add_argument('path', help='Variável de ambiente PATH')

args = parser.parse_args()

path = args.path


numprocs = input('What is the number of processes?[1]: ')
if(numprocs == ''):
	numprocs = 1

path_default = path.split('/')
name = input('What is the name of the program?[{}]:'.format(path_default[-1]))
if(name == ''):
	name = path_default[-1]

path_supervisor = "/etc/supervisor/conf.d/{}.conf".format(name)

if os.path.exists(path_supervisor):
	print("ERROR: file {} exists\n\n".format(path_supervisor))
	exit(1)

conf = """
[program:{name}]
process_name=%(program_name)s_%(process_num)02d
command=php {path}/artisan queue:work --sleep=3 --tries=3 --timeout=300
autostart=true
autorestart=true
user=www-data
numprocs={numprocs}
redirect_stderr=true
stdout_logfile=/tmp/{name}.log
""".format(path = path, name = name, numprocs = numprocs)

with open(path_supervisor, 'w') as file:
	file.write(conf)

subprocess.check_call(['supervisorctl', 'update'])

print("Supervisor configurado...\n\n")
