sudo pkill wpa_supplicant
sudo /usr/local/sbin/wpa_supplicant  -c$PROJECT_HOME/scripts/configurator/wpa_supplicant.conf -iwlan1 -Dnl80211,wext -dd -f /tmp/debug.txt 
#/usr/local/sbin/wpa_supplicant  -c/home/pi/configurator/wpa_supplicant.conf -iwlan0 -Dnl80211,wext -dd -f /tmp/debug.txt
#/usr/local/sbin/wpa_supplicant  -c/home/pi/configurator/wpa_supplicant.conf -iwlan0  -dd -f /tmp/debug.txt
