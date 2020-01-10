sudo ifconfig wlan1 0
cp wpa_supplicant.conf.orig wpa_supplicant.conf
sudo python enrollee.py --if wlan1 --pkey $PROJECT_HOME/test/DevID50/DevIDSecrets/IDevID50.key.der --cf ./wpa_supplicant.conf
