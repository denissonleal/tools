#!/usr/bin/python3

import argparse
import os.path
import subprocess

parser = argparse.ArgumentParser(description='Configura o servidor Apache.')
parser.add_argument('name', help='Diretório do projeto')
parser.add_argument('path', help='Variável de ambiente PATH')
parser.add_argument('-d', '--domain', help='Domínio HTTP da aplicação')

args = parser.parse_args()

name = args.name
path = args.path

path_apache = "/etc/apache2/sites-available/{}.conf".format(name)

if os.path.exists(path_apache):
	print("ERROR: file {} exists\n\n".format(path_apache))
	exit(1)

path_link = "/var/www/{}".format(name);
if os.path.exists(path_link):
	print("ERROR: file {} exists\n\n".format(path_link))
	exit(1)

domain = "{}.{}".format(name, args['domain'] if len(args.domain) > 3 else 'app')

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
		AllowOverride Options
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

subprocess.check_call(['ln', '-s', path, path_link])
subprocess.check_call(['a2enmod', 'rewrite'])
subprocess.check_call(['a2ensite', '{}.conf'.format(name)])
subprocess.check_call(['service', 'apache2', 'restart'])

print("Site configurado...\n\n")
