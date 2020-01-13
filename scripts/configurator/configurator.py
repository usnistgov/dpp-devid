   
import subprocess
import os
import time
import argparse
import binascii
import argparse
import sys


def run_cmd(cmd):
    p = subprocess.Popen(cmd,shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res,err = p.communicate()
    return str(res.split('\n')[1])

def onboard(ssid_txt,passwd,cacertpath,bootstrapping_uri):
    if bootstrapping_uri is None or ssid_txt is None or \
       cacertpath is None or passwd is None:
       print("missing parameters -- can't run script exit.")
       sys.exit()
       os.exit()


    # This should be obtained from wpa supplicant config file.
    cmd = ["wpa_passphrase", ssid_txt, passwd]
    ssid = ssid_txt.encode('hex')
    print("ssid " + ssid)
    p = subprocess.Popen(cmd,shell=False, stdin= subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res,err = p.communicate()
    print(res)
    lines = str(res).split("\n")

    for line in lines:
        if "psk" in line:
            start = line.strip().find("psk=")
            if start == 0:
                psk=line[5:]

    print("Psk = " + psk + "\n")


    cli_cmd = ["/usr/local/sbin/wpa_cli", "-p", "/var/run/wpa_supplicant1"]

    cmd = cli_cmd+ ["get_capability","dpp"]
    dpp_version = run_cmd(cmd)
    print("dpp_version is " + dpp_version)
    if dpp_version != "DPP=2":
	print >> sys.stderr, "dpp_version is " + dpp_version
        sys.exit()

    print("Configurator: add a configurator object\n")
    cmd = cli_cmd + [ 'dpp_configurator_add']
    dpp_configurator_id = run_cmd(cmd)
    print ("Configurator ID = " + dpp_configurator_id)
    print("Configurator: Self sign the configurator object\n")
    cmd = cli_cmd  +  ["dpp_configurator_sign", "conf=sta-psk", "psk="+psk, "ssid="+ssid, "configurator=" + str(dpp_configurator_id)]
    retval = run_cmd(cmd)
    print(retval)
    cmd  = cli_cmd + ["dpp_qr_code" , bootstrapping_uri]
    bootstrapping_info_id = run_cmd(cmd)
    print("bootstrapping_info_id " + str(bootstrapping_info_id))
    cmd = cli_cmd + ['dpp_auth_init', "peer={} conf=sta-psk ssid={} psk={} configurator={} cacert={}".format(bootstrapping_info_id,ssid,psk, dpp_configurator_id ,cacertpath)]
    retval = run_cmd(cmd)
    print (retval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ca",help="Path to CA certificate chain", default=None)
    parser.add_argument("--ssid", help="SSID for the network", default=None)
    parser.add_argument("--passwd", help="Password for the network (text)", default=None)
    parser.add_argument("--bootstrapping-uri", help="The DPP bootstrapping URI ", default=None)
    args = parser.parse_args()
    
    #bootstrapping_uri = 'DPP:M:00:13:ef:20:1d:6b;K:MDkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDIgADiD1AnX/e2cvUgAmR1hXk9Vn8zAs0fWr/Vh/177YP2Us=;;'
    #cwd = os.path.realpath(os.getcwd())
    #cacertpath="{}/DevID50/CredentialChain/ca-chain.cert.pem".format(cwd)
    #ssid_txt="0024A5AFF6CF"
    #passwd="xubr6cx9i8424"

    bootstrapping_uri = args.bootstrapping_uri
    ssid_txt = args.ssid
    cacertpath = args.ca
    passwd = args.passwd
    onboard(ssid_txt,passwd,cacertpath,bootstrapping_uri)

    


