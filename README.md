# dpp-devid

This repository publishes a user interface, certificates and scripts to test out DPP with device iD support.

Important: This is a proposed extension to wifi-easyconnect (AKA DPP) but it is not part of the standard.

This project requires the fork of hostap with support for iDevID and 802.1AR cert generation scripts. 
Following are the submodules included:

   https://github.com/ranganathanm/hostap
   
   
   https://github.com/MonikaSinghNIST/iDevIDCerts


The following is a summary of the interactions exercised by the script (via wpa\_supplicant):

As in standard DPP, the DPP url contains the public key of the device
certificate (not the full certificate). The IOT device (supplicant)
publishes this as a QR code.  This is scanned by Configurator which does
an authentication of the supplicant.  The authentication is based on
the public key of the certificate (not the full certificate).  (The DPP
url itself only contains the raw public key. ) Thus far it is standard
DPP behavior.

After authentication, the supplicant sends a configuration request,
requesting network credentials.

The following enhancement was added to DPP in the hostap submodule. 
(NOTE: This is not part of the standard DPP 1.0 protocol.)

The configuration request sent by the supplicant has the IDevID
certificate. The verification step (performed by the Configurator during
processing of the configuration request) checks the certificate to see if
the public key of the DPP url matches the public key of the certificate
and also verifies the certificate chain based on the CA certificate. If
the presented iDevID certificate verifies, the configurator sends network credentials
information to the supplicant, thereby onboarding the supplicant.

The assumptions are :

* The device certificate is assumed be shipped with the device.
* The device has the private key in a tamper proof store and uses this to complete the authentication with the configurator.
  This is the same key that was used to generate the device certificate.
* The configurator has the CA certificate from the manufacturer.

# Hardware requirements

You need two Raspberry Pi's with USB wireless cards to try this out.
One of the raspberry Pi's is called the "configurator". This is the application that will onboard the second
Raspberry Pi (the supplicant).

# Procedure

On each raspberry Pi :


Please clone this repository using to fetch the necessary submodules.

         git clone --recurse-submodules

Copy the config files for building and build wpa-supplicant / hostapd and build them. This is done using the build.sh script.
   
       sh build.sh

Configurator: Install zbar-tools (for reading qr codes -- configurator only). An example qr code
png file is provided for test purposes.

        sudo apt-get install zbar-tools
        sudo apt-get install libzbar-dev

COnfigurator: Install the python wrapper for zbar and the python image library to read qr codes (configurator only )

        pip install Pillow
        pip install zbarlight

Configurator and supplicant: Install pyside (for demonstration GUI)

         sudo apt-get install python-pyside

Configurator and Supplicant: Install netifaces to read the network interface MAC address

        pip install netifaces

Set the PROJECT_HOME enviornment variable to the place where you installed this repository.

Enrollee: copy wpa_supplicant.example into wpa_supplicant.orig, Edit wpa_supplicant.orig 
and point it at the DevId certificate.  This is done for you in the start_wpas.sh script.
Start the enrolle as follows. 

         cd scripts/supplicant 
         # Start the supplicant
         ./start-supplicant

Configurator: start wpa supplicant

        cd scripts/configurator
        ./start_wpas.sh

Configurator:  start the configurator.
         
        sudo -E python configurator-gui.py

Select the qr code and click on Onboard. You should see the supplicant duck find it's mother :-)
The supplicant will issue a dhclient request and join the network.

# Known bugs

The onboarding is not 100 % reliable. If it fails, reboot the supplicant. 


# Limitations



* The DPP scanning code is not reliable. You can scan the QR codes from a png file on the configurator.
* There is no feedback on the configurator indicating success of certificate verification.



## Notes ##

If you are using a raspberry Pi3 to test this out, please use a USB wireless card. The on board wireless 
card does not support DPP (the device driver needs to support action frames -- which it does not).


## Copyrights and Disclaimers ##

The following disclaimer applies to all code that was written by employees
of the National Institute of Standards and Technology.

This software was developed by employees of the National Institute of
Standards and Technology (NIST), an agency of the Federal Government
and is being made available as a public service. Pursuant to title 17
United States Code Section 105, works of NIST employees are not subject
to copyright protection in the United States.  This software may be
subject to foreign copyright.  Permission in the United States and in
foreign countries, to the extent that NIST may hold copyright, to use,
copy, modify, create derivative works, and distribute this software
and its documentation without fee is hereby granted on a non-exclusive
basis, provided that this notice and disclaimer of warranty appears in
all copies.

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND,
EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED
TO, ANY WARRANTY THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
AND FREEDOM FROM INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION
WILL CONFORM TO THE SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL
BE ERROR FREE.  IN NO EVENT SHALL NIST BE LIABLE FOR ANY DAMAGES,
INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL
DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY CONNECTED WITH
THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR
OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY
OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT
OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.

[See official statements here](https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software)


Specific copyrights for code that has been re-used from other open 
source projects are noted in the source files as appropriate.
Please acknowledge our work if you re-use this code or design.

