#!/usr/bin/python3

import sys
import os.path
import subprocess

numprocs = input('What is the number of processes?[1]: ')
if(numprocs == ''):
	numprocs = 1

path_default = sys.argv[1].split('/')
# print('The program name by default is',path_default[-1])
name = input('What is the name of the program?[{}]:'.format(path_default[-1]) )
if(name == ''):
	name = path_default[-1]

if len(sys.argv) < 1:
	print('ERROR: {name} {path} {?domain}\n')
	exit(1)

path = sys.argv[1]

path_supervisor = "/etc/supervisor/conf.d/{}.conf".format(name)

# if os.path.exists(path_supervisor):
# 	print("ERROR: file {} exists\n\n".format(path_supervisor))
# 	exit(1)

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

print(conf)


# with open(path_supervisor, 'w') as file:
# 	file.write(conf)

# subprocess.check_call(['supervisorctl', 'update'])

print("Site configurado...\n\n")
