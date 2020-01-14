cp hostap-build-config/wpa_supplicant/.config hostap/wpa_supplicant/
cp hostap-build-config/hostapd/.config hostap/hostapd/
cd hostap/wpa_supplicant; sudo make install
