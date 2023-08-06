#!/bin/bash

/etc/init.d/mysql start
/usr/bin/mysqld_safe  & sleep 2s
opendcim_version=21.01

cd /var/www || exit 2
rm -fr /var/www/dcim
mkdir -p /var/www/dcim
wget -q --no-check-certificate http://opendcim.org/packages/openDCIM-${opendcim_version}.tar.gz
tar zxpf openDCIM-${opendcim_version}.tar.gz
mv openDCIM-${opendcim_version}/* dcim
rm openDCIM-${opendcim_version}.tar.gz

mkdir -p /var/www/dcim/pictures /var/www/dcim/drawings /var/www/dcim/reports
rm -fr /var/www/html
chgrp -R www-data /var/www/dcim
chmod g+w /var/www/dcim/pictures \
        /var/www/dcim/drawings \
        /var/www/dcim/vendor/mpdf/mpdf/ttfontdata \
        /var/www/dcim/reports


cd /var/www/dcim || exit 2
cp db.inc.php-dist db.inc.php
mv install.php removed_install.php

#  copy conf of
cat << EOF > /var/www/dcim/.htaccess
AuthType Basic
AuthName "openDCIM"
AuthUserFile /var/www/opendcim.password
Require valid-user
EOF

#Set ServerName and timezone for Apache
echo "ServerName opendcim.local" > /etc/apache2/conf-available/fqdn.conf
ln -s /etc/apache2/conf-available/fqdn.conf /etc/apache2/conf-enabled/fqdn.conf

a2enmod rewrite

/etc/init.d/apache2 restart
/etc/init.d/mysql restart
sleep 5s

#make backup copy for Volume
mkdir -p /var/backup
cp -Rp /var/lib/mysql /var/backup
cp -Rp /var/www/dcim/pictures /var/backup
cp -Rp /var/www/dcim/drawings /var/backup
