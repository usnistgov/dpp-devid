import subprocess
import binascii
import argparse
import os
import sys
import netifaces
import time

def run_cmd(cmd):
    p = subprocess.Popen(cmd,shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res,err = p.communicate()
    return res.split('\n')[1]

def convert_to_hex(priv_key_file):
    with open(priv_key_file, mode="rb") as file:
        fileContent = file.read()

    hex_str = binascii.b2a_hex(fileContent)
    return hex_str

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pkey",help="private key file in DER format",default=None)
    parser.add_argument("--ifc",help="Interface to configure",default=None)
    parser.add_argument("--cf", help="Wpa supplicant configuration file", default = "./wpa_supplicant.conf")
    args = parser.parse_args()

    priv_key = args.pkey
    if priv_key is None:
	print("Please provide private key file in DER format with --pk flag")
        sys.exit()
        os.exit()
    dpp_configurator_key = convert_to_hex(priv_key)
    print("configurator_key " + dpp_configurator_key)
     
    interface = args.ifc
    if interface is None:
        print("Please supply wireless interface with --if flag")
        sys.exit()
        os.exit()

    
    fsz = os.path.getsize(args.cf)

    addrs = netifaces.ifaddresses(interface)
    mac_addr = addrs[netifaces.AF_LINK][0]["addr"]
    print("mac_addr " + mac_addr)
    
    sta_clicmd = ["/usr/local/sbin/wpa_cli", "-p", "/var/run/wpa_supplicant2"]

    dpp_configurator_id = run_cmd( sta_clicmd + ['dpp_configurator_add', 'key=' + dpp_configurator_key, "curve=prime256v1"])
    bootstrapping_info_id = run_cmd( sta_clicmd + ["dpp_bootstrap_gen" , "type=qrcode", "mac=" + mac_addr, "key=" + dpp_configurator_key] )
    print("bootstrapping_info_id " + str(bootstrapping_info_id))
    #Get QR Code of device using the bootstrap info id.
    print("enrollee: get the qr code using the returned bootstrap_info_id\n")

    bootstrapping_uri = "'" + run_cmd(sta_clicmd + ["dpp_bootstrap_get_uri" , str(bootstrapping_info_id)])+ "'"
    print("bootstrapping_uri = " + bootstrapping_uri + "\n")
    bootstrap_info = run_cmd(sta_clicmd + ["dpp_bootstrap_info" , bootstrapping_info_id])
    print("bootstrapping_info = " + bootstrap_info)
    print("enrollee: listen for dpp provisioning request\n")
    retval = run_cmd(sta_clicmd + ["dpp_listen" , str(2437)] )
    print(retval)
    while os.path.getsize(args.cf) == fsz :
        print("Waiting for configuration")
	time.sleep(3)
        
    run_cmd(sta_clicmd + ["save_config"])
    print("Reloading the config file\n")
    run_cmd(sta_clicmd + ["reconfigure"])


