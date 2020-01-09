cp wpa_supplicant.conf.orig wpa_supplicant.conf
sudo python enrollee.py --if wlan1 --pkey /home/pi/dpp-devid/test/DevID50/DevIDSecrets/IDevID50.key.der --cf ./wpa_supplicant.conf
