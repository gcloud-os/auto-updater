#!/bin/bash

# gcloud-updater-simple install script.
# hanfei@g-cloud.com.cn
# 2015-12-29

dir=$(dirname $0)
log_file=${dir}/inst.log
LOG_BANNER="gcloud-updater-simple installer"

cd $dir
if ! /usr/bin/env python setup.py install; then
    echo $LOG_BANNER "setup.py install failed." >> $log_file
    exit -1
fi

install bin/gupdater /usr/bin
mkdir -p /etc/gcloud
mkdir -p /var/log/gupdater
install doc/updater.conf /etc/gcloud/

\cp -r doc/gupdater.service /usr/lib/systemd/system/
systemctl enable gupdater
