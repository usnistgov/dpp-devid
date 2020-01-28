import sys
import os
import subprocess
from PySide import QtGui
from PySide.QtGui import QWidget, QApplication, QMainWindow, QPushButton, QGridLayout, QDesktopWidget, QIcon, QLineEdit
from PySide.QtCore import QSize
import filecmp
import shutil
import os
from threading import Timer,Thread,Event


class MainWindow(QMainWindow):
    def __init__(self):
        """ Constructor Function
        """
        super(MainWindow, self).__init__()
        self.initGUI()

    def initGUI(self):
        self.setWindowTitle("Enrollee")
        self.setGeometry(200, 400, 200, 200)
        self.center()
        self.setLayout()
        self.show()
        thread = Timer(5,self.checkState)
        thread.start()
       

    def startWpas() :
        os.system("sudo pkill wpa_supplicant")
        cmd = "/usr/local/sbin/wpa_supplicant -c%s/scripts/supplicant/wpa_supplicant.conf  -i%s -Dnl80211,wext -dd -f /tmp/debug.txt" \
                .format(os.environ.get("PROJECT_HOME"),"wlan1")
        os.spawnl(os.P_NOWAIT,cmd)
        os.system("ifconfig %s 0".format("wlan1"))
        cmd = "python supplicant.py --if wlan1 --pkey %s/test/DevID50/DevIDSecrets/IDevID50.key.der --cf ./wpa_supplicant.conf"\
                    .format(os.environ.get("PROJECT_HONE"))
        os.spawnl(os.P_NOWAIT,cmd)
        


    def center(self):
        """ Function to center the application
        """
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        # First move the rectangle
        qRect.moveCenter(centerPoint)
        # move my window to the moved rectangle.
        self.move(qRect.topLeft())
    
    def checkState(self):
        self.checkFiles()
        thread = Timer(5,self.checkState)
        thread.start()
    
    def checkFiles(self):
        if filecmp.cmp ("wpa_supplicant.conf","wpa_supplicant.conf.orig") :
            self.rebootButton.setIcon(self.duckIcon)
        else:
            self.rebootButton.setIcon(self.happyDuckIcon)
        

    
    def reboot(self):
        shutil.copyfile("wpa_supplicant.conf.orig","wpa_supplicant.conf")
        os.system("sudo reboot")


    
    def setLayout(self):
        self.duckIcon = QIcon("duck.jpeg")
        self.happyDuckIcon  = QIcon("happy-duck.jpg")
        qWidget = QWidget()
        gridLayout = QGridLayout(qWidget)
        row = 0
        self.setCentralWidget(qWidget)

        row = row + 1
        self.rebootButton = QPushButton()
        #self.rebootButton.setIcon(QIcon("duck.jpeg"))
        self.rebootButton.setIconSize(QSize(200,200))
        gridLayout.addWidget(self.rebootButton,row,0)
        self.rebootButton.clicked.connect(self.reboot)
        self.checkFiles()
        
        

        
if __name__ == "__main__":
    try:
        # QApplication.setStyle('plastique')
        if not os.path.exits("wpa_supplicant.orig") :
            shutil.copyfile("wpa_supplicant.example", "wpa_supplicant.orig")
        if not os.path.exists("wpa_supplicant.conf") :
            shutil.copyfile("wpa_supplicant.orig", "wpa_supplicant.conf")
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()
        myApp.exec_()
        os.system("sudo sh start-wpas.sh")
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])


