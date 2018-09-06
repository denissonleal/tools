#!/usr/bin/env php
<?php

	if ( count($argv) < 3 ) {
		echo "ERROR: {name} {path} {?domain}\n\n";
		exit;
	}
	$name = $argv[1];
	$path = $argv[2];
	$file_apache = "/etc/apache2/sites-available/$name.conf";
	if ( file_exists($file_apache) ) {
		echo "ERROR: file $file_apache exists\n\n";
		exit;
	}
	$link = "/var/www/$name";
	if ( file_exists($link) ) {
		echo "ERROR: file $link exists\n\n";
		exit;
	}

	$domain = "$name." . ( isset($argv[3]) ? $argv[3] : 'app' );

	$conf = "
<VirtualHost *:80>
	ServerName $domain
	ServerAlias www.$domain

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/$name

	<Directory />
		Options -Indexes +FollowSymLinks +MultiViews +Includes
		AllowOverride AuthConfig
		Order allow,deny
		allow from all
	</Directory>

	<Directory /var/www/$name>
		AllowOverride Options
		Options -Indexes +FollowSymLinks +MultiViews +Includes
		Order allow,deny
		allow from all
		RewriteEngine on
		RewriteBase /
		RewriteCond %{REQUEST_FILENAME} !-f
		RewriteCond %{REQUEST_FILENAME} !-d
		RewriteRule ^(.*)$ index.php?q=$1 [L,QSA]
		RewriteRule ^ - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
	</Directory>


	ErrorLog \${APACHE_LOG_DIR}/$name-error.log
	CustomLog \${APACHE_LOG_DIR}/$name.log combined

</VirtualHost>
";


	file_put_contents($file_apache, $conf);

	exec("ln -s $path $link");
	exec("a2enmod rewrite");
	exec("a2ensite $name.conf");
	exec("service apache2 restart");

	echo "Site configurado...\n\n";
