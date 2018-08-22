#!/usr/bin/python3

import sys
import os.path
import subprocess

if len(sys.argv) < 3:
	print('ERROR: {name} {path} {?domain}\n')
	exit(1)

name = sys.argv[1]
path = sys.argv[2]

path_apache = "/etc/apache2/sites-available/{}.conf".format(name)

if os.path.exists(path_apache):
	print("ERROR: file {} exists\n\n".format(path_apache))
	exit(1)

path_link = "/var/www/{}".format(name);
if os.path.exists(path_link):
	print("ERROR: file {} exists\n\n".format(path_link))
	exit(1)

domain = "{}.{}".format(name, sys.argv[3] if len(sys.argv) > 3 else 'app');

{'domain': domain, 'name': name}

conf = """
<VirtualHost *:80>
	ServerName {domain}
	ServerAlias www.{domain}

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/{name}

	<Directory />
		Options -Indexes +FollowSymLinks +MultiViews +Includes
		AllowOverride AuthConfig
		Order allow,deny
		allow from all
	</Directory>

	<Directory /var/www/{name}>
		Options -Indexes +FollowSymLinks +MultiViews +Includes
		Order allow,deny
		allow from all
		RewriteEngine on
		RewriteBase /
		RewriteCond %{{REQUEST_FILENAME}} !-f
		RewriteCond %{{REQUEST_FILENAME}} !-d
		RewriteRule ^(.*)$ index.php?q=$1 [L,QSA]
		RewriteRule ^ - [E=HTTP_AUTHORIZATION:%{{HTTP:Authorization}}]
	</Directory>


	ErrorLog ${{APACHE_LOG_DIR}}/{name}-error.log
	CustomLog ${{APACHE_LOG_DIR}}/{name}.log combined

</VirtualHost>
""".format(domain=domain, name=name)

with open(path_apache, 'w') as file:
	file.write(conf)

subprocess.check_call(['ln', '-s', path, path_link]);
subprocess.check_call(['a2enmod', 'rewrite']);
subprocess.check_call(['a2ensite', '{}.conf'.format(name)]);
subprocess.check_call(['service', 'apache2', 'restart']);

print("Site configurado...\n\n");
