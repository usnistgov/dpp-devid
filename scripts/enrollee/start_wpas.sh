#!/bin/bash
sudo pkill wpa_supplicant
sudo pkill wpa_supplicant
sudo cp wpa_supplicant.conf.orig wpa_supplicant.conf
sudo chown pi wpa_supplicant.conf
sudo /usr/local/sbin/wpa_supplicant  -c`pwd`/wpa_supplicant.conf -iwlan1 -Dnl80211,wext -dd -f /tmp/debug.txt

