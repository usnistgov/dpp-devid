#!/bin/bash
if [ -z ${PROJECT_HOME+x} ]; then
        echo "PROJECT_HOME is unset"; exit
else
        echo "PROJECT_HOME is set to '$PROJECT_HOME'"
fi
if [ -z ${PROJECT_HOME+x} ]; then
        echo "PROJECT_HOME is unset"; exit
else
        echo "PROJECT_HOME is set to '$PROJECT_HOME'"
fi

sudo iwconfig wlan1 channel 6
sudo pkill wpa_supplicant
sudo cp wpa_supplicant.conf.orig wpa_supplicant.conf
sudo chown pi wpa_supplicant.conf
sudo nohup /usr/local/sbin/wpa_supplicant  -c$PROJECT_HOME/scripts/supplicant/wpa_supplicant.conf -iwlan1 -Dnl80211,wext -dd -f /tmp/debug.txt > /tmp/wpas.log 2>&1 &
sleep 15 

pid=`pgrep wpa_supplicant`
if [ -z ${pid+x} ]; then
        echo "wpa_supplicant not started. Start it with start_wpas.sh"; exit
else
	echo "wpa_supplicant is running pid is '$pid'"
fi
sudo ifconfig wlan1 0
sudo -E python supplicant-gui.py &
sudo -E python supplicant.py --if wlan1 --pkey $PROJECT_HOME/test/DevID50/DevIDSecrets/IDevID50.key.der --cf ./wpa_supplicant.conf
#sudo python supplicant.py --if wlan1 --pkey $PROJECT_HOME/test/test-devid/iDevID/private/DevID.key.der --cf ./wpa_supplicant.conf
