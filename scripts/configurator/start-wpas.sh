#!/bin/bash
if [ -z ${PROJECT_HOME+x} ]; then 
	echo "PROJECT_HOME is unset"; exit
else
	echo "PROJECT_HOME is set to '$PROJECT_HOME'"
fi
sudo pkill wpa_supplicant
echo "Starting wpa_supplicant"
sudo /usr/local/sbin/wpa_supplicant  -c$PROJECT_HOME/scripts/configurator/wpa_supplicant.conf -iwlan1 -Dnl80211,wext -dd -f /tmp/debug.txt
