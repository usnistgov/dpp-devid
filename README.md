# dpp-idevid

Scripts to onboard a device with Device certificates. This requires the fork of hostap with support for iDevID which is available here.

    https://github.com/ranganathanm/hostap  

Please clone and build it. This is just the User Interface.

Install zbar-tools (for reading qr codes -- configurator only)

        sudo apt-get install zbar-tools
        sudo apt-get install libzbar-dev

Install the python wrapper for zbar and the python image library to read qr codes (configurator only )

        pip install Pillow
        pip install zbarlight

Install netifaces to read the network interface MAC address

        pip install netifaces

Install pyside (for GUI -- configurator only)

         sudo apt-get install python-pyside

Edit 


