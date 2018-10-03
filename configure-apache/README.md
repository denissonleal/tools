# configure-apache

Automated scripts for apache2 quick configuration

## Download

```sh
wget https://raw.githubusercontent.com/denissonleal/tools/master/configure-apache/configure-apache.php -O configure-apache
```

or with python

```sh
wget https://raw.githubusercontent.com/denissonleal/tools/master/configure-apache/configure-apache.py -O configure-apache
```

## Configuration

```sh
sudo chmod +x configure-apache
```

## Using

```sh
sudo ./configure-apache {name} {path} {?domain}
```

NOTE: `path` must be an absolute path

## Example

```sh
sudo ./configure-apache exemplo /home/denissonleal/exemplo leal.app
```

