import sys
import os
import subprocess
from PySide import QtGui
from PySide.QtGui import QWidget, QApplication, QMainWindow, QPushButton, QGridLayout, QDesktopWidget, QIcon, QLineEdit, QStatusBar
from PySide.QtCore import QSize, Signal, Slot
from PySide import QtCore
import filecmp
import shutil
import os
import time
import subprocess
from threading import Timer,Thread,Event

class FooConnection(QtCore.QObject):
       foosignal = Signal(str)


class MainWindow(QMainWindow):
    def __init__(self):
        """ Constructor Function
        """
        super(MainWindow, self).__init__()
        self.initGUI()
        self.mysignal = FooConnection()
        self.mysignal.foosignal.connect(self.updateGui)

    def initGUI(self):
        self.setWindowTitle("Enrollee")
        self.setGeometry(200, 400, 200, 200)
        self.center()
        self.setLayout()
        self.show()
       

    def center(self):
        """ Function to center the application
        """
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        # First move the rectangle
        qRect.moveCenter(centerPoint)
        # move my window to the moved rectangle.
        self.move(qRect.topLeft())

    @Slot()
    def updateGui(self):
        interface = "wlan1"
        self.rebootButton.setIcon(self.happyDuckIcon)
        self.myStatusBar.showMessage("Waiting for DHCP address.")
        p = subprocess.Popen(["/sbin/dhclient", interface],shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res,err = p.communicate()
        self.myStatusBar.showMessage("Done!")

    

    def run_cmd(self, cmd):
        p = subprocess.Popen(cmd,shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res,err = p.communicate()
        return res.split('\n')[1]
    
    def checkFiles(self):
        print("checking")
        if not filecmp.cmp ("wpa_supplicant.conf","wpa_supplicant.conf.orig") :
            self.mysignal.foosignal.emit("onboarded")
        else:
       	    self.thread = Timer(5,self.checkFiles)
            self.thread.start()

   
        
    
    def reboot(self):
        shutil.copyfile("wpa_supplicant.conf.orig","wpa_supplicant.conf")
        os.system("sudo reboot")


    
    def setLayout(self):
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)

        self.duckIcon = QIcon("duck.jpeg")
        self.happyDuckIcon  = QIcon("happy-duck.jpeg")
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
     

        if filecmp.cmp ("wpa_supplicant.conf","wpa_supplicant.conf.orig") :
            self.myStatusBar.showMessage("Waiting to onboard.")
            self.rebootButton.setIcon(self.duckIcon)
       	    self.thread = Timer(5,self.checkFiles)
            self.thread.start()
        else:
            self.rebootButton.setIcon(self.happyDuckIcon)
            self.myStatusBar.showMessage("waiting for DHCP address")
            interface = "wlan1"
            p = subprocess.Popen(["/sbin/dhclient", interface],shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            res,err = p.communicate()
        
        

        
if __name__ == "__main__":
    try:
        # QApplication.setStyle('plastique')
        if not os.path.exists("wpa_supplicant.conf.orig") :
            shutil.copyfile("wpa_supplicant.conf.example", "wpa_supplicant.conf.orig")
        if not os.path.exists("wpa_supplicant.conf") :
            shutil.copyfile("wpa_supplicant.conf.orig", "wpa_supplicant.conf")
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()
        myApp.exec_()
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])


