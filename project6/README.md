# Configuring a Linux server

By Basma Ashour, in fulfillment of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

## About
This project is a baseline installation of a Linux server and prepare it to host my web applications. secured my server from a number of attack vectors, installed and configure a database server, and deployed one of my existing web applications onto it.

# Server details
IP address: `52.56.148.216`

SSH port: `2200`

URL:  [http://52.56.148.216](http://52.56.148.216)


# Configuration changes
## Add user
Add user `grader` with command: `sudo adduser grader`

## Add user grader to sudo group
Assuming your Linux distro has a `sudo` group (like Ubuntu 16.04), simply add the user to
this admin group:
```
sudo usermod -a -G sudo grader
```

## Update all currently installed packages

- Update the package indexes `apt-get update` 

- To actually upgrade the installed packages `apt-get upgrade` 


## Set-up SSH keys for user grader
As root user do:
```
mkdir /home/grader/.ssh
chmod 700 /home/grader/.ssh
chmod 644 /home/grader/.ssh/authorized_keys
```

Can now login as the `grader` user using the command:
`ssh grader@52.56.148.216 -p 22 -i ~/.ssh/linuxp6`


## Disable root login
Change the PasswordAuthentication line to no instead of yes in the file `/etc/ssh/sshd_config`:

- So it reads:
```
PasswordAuthentication no
```
Do ` sudo service ssh restart` for the changes to take effect.


## Change timezone to UTC
Check the timezone with the `date` command. This will display the current timezone after the time.
If it's not UTC change it like this:

`sudo timedatectl set-timezone UTC`

## Change SSH port from 22 to 2200

- Reconfigure the port for the ssh server:
`sudo nano /etc/ssh/sshd_config`
and change:
`port 22`
- to:
`Port 2200`

- Then reload the configuration:
`sudo service ssh force-reload`

- and connect via:

`ssh grader@52.56.148.216 -p 2200 -i ~/.ssh/linuxp6`


## Configuration Uncomplicated Firewall (UFW)
By default, block all incoming connections on all ports:

`sudo ufw default deny incoming`

- Allow outgoing connection on all ports:

`sudo ufw default allow outgoing`

- Allow incoming connection for SSH on port 2200:

`sudo ufw allow 2200/tcp`

- Allow incoming connections for HTTP on port 80:

`sudo ufw allow www`

- Allow incoming connection for NTP on port 123:

`sudo ufw allow ntp`

- To check the rules that have been added before enabling the firewall use:

`sudo ufw show added`

- To enable the firewall, use:

`sudo ufw enable`

- To check the status of the firewall, use:

`sudo ufw status`

## Install Apache to serve a Python mod_wsgi application
- Install Apache:

`sudo apt-get install apache2`

- Install the `libapache2-mod-wsgi` package:

`sudo apt-get install libapache2-mod-wsgi`

## Install and configure the PostgreSQL database system
 ```
 sudo apt-get install PostgreSQL
 # check that remote connections are not allowed in PostgreSQL config file
 sudo nano /etc/postgresql/9.3/main/pg_hba.config
 ```
 
## create a PostgreSQL role named catalog and a database named catalog
```
sudo -u postgres -i
postgres:~$ creatuser catalog
postgres:~$ createdb catalog
postgres:~$ psql
postgres=# ALTER DATABASE catalog OWNER TO catalog;
postgres=# ALTER USER catalog WITH PASSWORD 'catalog'
postgres=# \q
postgres:~$ exit

```

## Install Flask, SQLAlchemy, etc
- Issue the following commands:
```
sudo apt-get install python-psycopg2 python-flask
sudo apt-get install python-sqlalchemy python-pip
sudo pip install oauth2client
sudo pip install requests
sudo pip install httplib2
sudo pip install flask-seasurf
```

- An alternative to installing system-wide python modules is to create a virtual 
environment for each application using the [virualenv][4] package.

## Install Git version control software
`sudo apt-get install git`

## Clone the repository that contains Project 4 Catalog app

```
cd /var/www
sudo mkdir project4
sudo chown -R grader:grader project4
cd project4
sudo git clone https://github.com/basmaashouur/project4.git project4
```

## Configure the web application to connect to the PostgreSQL database instead of a SQLite database
 ```
 sudo nano /var/www/project4/app.py
 # change the DATABASE_URI setting in the file from 'sqlite:///catalog.db' to 'postgresql://catalog:db_password@localhost/catalog)', and save
 
 ```
 
 ## Create schema and populate the catalog database with sample data
 ```
 python /var/www/project4/fill.py
 
 ```
 ## Configure Apache to serve the web application using WSGI
- Create the web application WSGI file.
 ```
sudo nano /var/www/project4/app.wsgi
```
Add the following lines to the file, and save the file.
```
#!/usr/bin/python
import sys 
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/project4/")
from project4 import app as application
application.secret_key = 'super_secret_key'

```
- Update the Apache configuration file to serve the web application with WSGI.
```
sudo nano /etc/apache2/sites-enabled/000-default.conf
```
- Add the following line inside the `<VirtualHost *:80>` element, and save the file.
```
        ServerName 52.56.148.216
	ServerAdmin basmaashouu@gmail.com
	WSGIScriptAlias / /var/www/project4/app.wsgi
 
```

- Restart Apache.
```
sudo apache2ctl restart
```

## References
- [Ask Ubuntu](http://askubuntu.com/)
- [PosgreSQL Docs](https://www.postgresql.org/docs/9.5/static/index.html)
- [Apache Docs](https://httpd.apache.org/docs/2.4/)
- [How To Install and Use PostgreSQL on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
- Stackoverflow and the Readme's of other FSND students on Github.
