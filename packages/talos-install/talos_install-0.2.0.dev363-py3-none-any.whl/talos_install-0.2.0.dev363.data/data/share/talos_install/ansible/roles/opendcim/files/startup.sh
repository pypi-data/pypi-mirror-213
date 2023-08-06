#!/bin/bash


set -e

#in case Volume are empty
if [ "$(ls -A /var/lib/mysql)" ]; then
    echo "mysql folder with data"
else
    cp -Rp /var/backup/mysql/. /var/lib/mysql/
    chown -R mysql:mysql /var/lib/mysql
fi

if [ "$(ls -A /var/www/dcim/pictures)" ]; then
   echo "pictures folder with data"
else
    cp -Rp /var/backup/pictures/. /var/www/dcim/pictures/
    chown -R www-data:www-data /var/www/dcim/pictures
fi

if [ "$(ls -A /var/www/dcim/drawings)" ]; then
   echo "drawings folder with data"
else
    cp -Rp /var/backup/drawings/. /var/www/dcim/drawings/
    chown -R www-data:www-data /var/www/dcim/drawings
fi

mkdir -p /var/run/mysqld/
chown mysql:mysql -R /var/run/mysqld/ /var/lib/mysql
/etc/init.d/mysql restart
if [[ -f /var/www/dcim/images/logo.png ]]; then rm /var/www/dcim/images/logo.png ; fi

if [ -f /etc/configured ]; then
        echo 'already configured'
else
        #needed to fix problem with ubuntu ... and cron
        update-locale
        date > /etc/configured
fi

if [ -f /sbin/first-run.sh ]; then
    /bin/bash -c /sbin/first-run.sh
    \mv /sbin/first-run.sh /var/backup
fi
