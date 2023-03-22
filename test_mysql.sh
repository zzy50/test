#!/bin/bash

# mysql uninstall
sudo apt-get remove --purge mysql* -y
sudo apt-get autoremove -y
sudo apt-get autoclean -y
echo "Uninstalling Done"

# mysql install
sudo apt-get update
sudo apt-get install mysql-server-8.0 -y
sudo ufw allow mysql
echo "Installing Done"
# mysql auto start setting
sudo systemctl start mysql
sudo systemctl enable mysql

sudo mysql -u root -e '
ALTER USER root@LOCALHOST IDENTIFIED WITH mysql_native_password BY "password";
flush privileges;
CREATE DATABASE AVC_DB;
use AVC_DB;
CREATE TABLE AVC_TABLE 
(`Index` int NOT NULL AUTO_INCREMENT, 
`RECORD_TIME` datetime(3) NOT NULL, 
`YEAR` int(11)  NOT NULL, 
`MONTH` int(11)  NOT NULL, 
`DATE` int(11)  NOT NULL, 
`TIME` time(3) NOT NULL, 
`CLASS` tinyint(4) NOT NULL, 
`LANE` tinyint(4) NOT NULL, 
`DIRECTION` char(2) NOT null, 
`Speed` int(11) NOT NULL, 
`LENGTH` int(11) NOT null, 
`OCCUPANCY` int(11) NOT NULL, 
PRIMARY KEY (`Index`), 
UNIQUE KEY Index_UNIQUE (`Index`));
'
echo "ALL DONE"