   
import subprocess
import os
import time
import argparse
import binascii
import argparse
import sys
import json
import requests



def run_cmd(cmd):
    p = subprocess.Popen(cmd,shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res,err = p.communicate()
    return str(res.split('\n')[1])

def onboard(ssid_txt,passwd,cacertpath,bootstrapping_uri, mudserver_host):
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
    #print("Configurator: Self sign the configurator object\n")
    cmd = cli_cmd  +  ["dpp_configurator_sign", "conf=sta-psk", "psk="+psk, "ssid="+ssid, "configurator=" + str(dpp_configurator_id)]
    retval = run_cmd(cmd)
    print(retval)
    cmd  = cli_cmd + ["dpp_qr_code" , bootstrapping_uri]
    bootstrapping_info_id = run_cmd(cmd)
    print("bootstrapping_info_id " + str(bootstrapping_info_id))
    cmd = cli_cmd + ['dpp_auth_init', "peer={} conf=sta-psk ssid={} psk={} configurator={} cacert={}".format(bootstrapping_info_id,ssid,psk, dpp_configurator_id ,cacertpath)]
    retval = run_cmd(cmd)
    time.sleep(3)
    cmd = cli_cmd + ["dpp_config_status", "id={}".format(str(dpp_configurator_id))]
    retval = run_cmd(cmd)
    mud_url = None
    idevid = None
    try:
    	print(retval)
    	jsonval = json.loads(retval)
    	mud_url = jsonval["config_status"]["mud_url"]
    	idevid = jsonval["config_status"]["idevid"]
    	f = open("iDevId.pem","w")
    	f.write(idevid)
    	f.close()
    except:
        print("Onboarding status info not found")

    cmd = cli_cmd + ["dpp_configurator_remove", str(dpp_configurator_id)]
    retval = run_cmd(cmd)
   
    # Send information out to the MUD server. This should be protected with
    # Two factor authentication from the MUD server.
    if mud_url is not None and idevid is not None and mudserver_host is not None:
        # Note this should be a https connection but for test purposes we use http.
        # This is test code -- works with NIST-MUD only.
        url = "http://" + mudserver_host + ":8181/restconf/config/nist-mud-device-association:mapping"
        pieces = bootstrapping_uri.split(";")
        mac_addr = pieces[0][len("DPP:M:"):]
        print("mac_addr = " , mac_addr)
        device_association = {}
        device_id=[mac_addr]
        device_association["device-id"] = device_id
        device_association["mud-url"] = mud_url
        mapping = {}
        mapping["mapping"] = device_association
        r = json.dumps(mapping) 
        print(r)       
        headers= {"Content-Type":"application/json"}
        r = requests.put(url, data=json.dumps(mapping), headers=headers , auth=('admin', 'admin'))
	print("status code = " + str(r.status_code))
    else:
        print("onboarding failed ")

	
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ca",help="Path to CA certificate chain", default=None)
    parser.add_argument("--ssid", help="SSID for the network", default=None)
    parser.add_argument("--passwd", help="Password for the network (text)", default=None)
    parser.add_argument("--bootstrapping-uri", help="The DPP bootstrapping URI ", default=None)
    parser.add_argument("--mudserver-host", help="The MUD server host", default=None)
    args = parser.parse_args()
    

    bootstrapping_uri = args.bootstrapping_uri
    ssid_txt = args.ssid
    cacertpath = args.ca
    passwd = args.passwd
    mudserver = args.mudserver_host
    onboard(ssid_txt,passwd,cacertpath,bootstrapping_uri,mudserver)

    


