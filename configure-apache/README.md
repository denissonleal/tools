# configure-apache

Script for apache2 configuration

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

## Exemple

```sh
sudo ./configure-apache exemplo /home/denissonleal/exemplo leal.app
```

# configure-supervison

Script for Supervisor configuration

## Download


```sh
wget https://raw.githubusercontent.com/denissonleal/tools/master/configure-supervison/configure-supervison.py -O configure-supervison
```

## Configuration

```sh
sudo chmod +x configure-supervison
```

## Using

```sh
sudo ./configure-supervison {path}
```

## Exemple

```sh
sudo ./configure-supervison exemplo /home/denissonleal/exemplo leal.app
```
