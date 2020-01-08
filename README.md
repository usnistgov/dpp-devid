# dpp-idevid

Scripts to onboard a device with Device certificates. This requires the fork of hostap with support for iDevID which is available here.

    https://github.com/ranganathanm/hostap  

Please clone and build it. This is just the User Interface.

Install zbar-tools (for reading qr codes)

        sudo apt-get install zbar-tools
        sudo apt-get install libzbar-dev

Install the python wrapper for zbar and the python image library

        pip install Pillow
        pip install zbarlight

Install pyside 

         sudo apt-get install python-pyside


