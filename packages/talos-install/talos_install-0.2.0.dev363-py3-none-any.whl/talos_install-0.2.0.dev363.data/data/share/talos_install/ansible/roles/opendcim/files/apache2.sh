#!/bin/bash

sv -w4 check mysqld

. /etc/apache2/envvars
exec chpst -u root apache2ctl -D FOREGROUND 2>&1
