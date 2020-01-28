# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'object_classifier_test.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import ODv1
import json

class Ui_MainWindow(object):

    def __init__(self):
        self.url = ''
        self.result = None
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(652, 452)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnCapWeb = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapWeb.setGeometry(QtCore.QRect(50, 110, 231, 61))
        self.btnCapWeb.setObjectName("btnCapWeb")
        self.btnRecWeb = QtWidgets.QPushButton(self.centralwidget)
        self.btnRecWeb.setGeometry(QtCore.QRect(50, 200, 231, 61))
        self.btnRecWeb.setObjectName("btnRecWeb")
        self.btnCapIP = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapIP.setGeometry(QtCore.QRect(380, 110, 221, 61))
        self.btnCapIP.setObjectName("btnCapIP")
        self.btnRecIP = QtWidgets.QPushButton(self.centralwidget)
        self.btnRecIP.setGeometry(QtCore.QRect(380, 200, 221, 61))
        self.btnRecIP.setObjectName("btnRecIP")
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(250, 310, 131, 51))
        self.btnExit.setObjectName("btnExit")
        self.lnIp = QtWidgets.QLineEdit(self.centralwidget)
        self.lnIp.setGeometry(QtCore.QRect(240, 30, 371, 41))
        self.lnIp.setObjectName("lnIp")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 36, 131, 31))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 652, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # My Triggers Here
        self.lnIp.editingFinished.connect(self.editUrl)
        self.btnExit.clicked.connect(self.clickExit)
        self.btnCapWeb.clicked.connect(self.clickCamWeb)
        self.btnRecWeb.clicked.connect(self.clickRecWeb)
        self.btnCapIP.clicked.connect(self.clickCamIP)
        self.btnRecIP.clicked.connect(self.clickRecIP)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnCapWeb.setStatusTip(_translate("MainWindow", "Capture an Image using the Webcam"))
        self.btnCapWeb.setText(_translate("MainWindow", "Capture Image From Webcam"))
        self.btnCapWeb.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.btnRecWeb.setStatusTip(_translate("MainWindow", "Capture a Video using the Webcam"))
        self.btnRecWeb.setText(_translate("MainWindow", "Capture Video From Webcam"))
        self.btnRecWeb.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.btnCapIP.setStatusTip(_translate("MainWindow", "Capture an Image using the IP Cam"))
        self.btnCapIP.setText(_translate("MainWindow", "Capture Image From IP Cam"))
        self.btnCapIP.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.btnRecIP.setStatusTip(_translate("MainWindow", "Capture a Video using the IP Cam"))
        self.btnRecIP.setText(_translate("MainWindow", "Cature Video From IP Cam"))
        self.btnRecIP.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.btnExit.setText(_translate("MainWindow", "EXIT"))
        self.btnExit.setStatusTip(_translate("MainWindow", "Exit the program"))
        self.btnExit.setShortcut(_translate("MainWindow", "Esc, Ctrl+Q"))
        self.lnIp.setStatusTip(_translate("MainWindow", "Enter the IP address of IP Cam Server Here"))
        self.label.setText(_translate("MainWindow", "URL of IP Cam"))

    def clickExit(self):
        QtCore.QCoreApplication.instance().quit()
    
    def clickCamWeb(self):
        result = ODv1.getObjectsFromCamera()
        if result:
            print(json.dumps(ODv1.getObjectsNames(), sort_keys=True, indent=4))
        else:
            self.unableToDetectCamera()

    def clickCamIP(self):
        result = ODv1.getObjectsFromCamera(self.url+'/shot.jpg')
        if result:
            print(json.dumps(ODv1.getObjectsNames(), sort_keys=True, indent=4))
        else:
            self.unableToDetectCamera()

    def clickRecWeb(self):
        result = ODv1.getVideoFromCamera()
        if not result:
            self.unableToDetectCamera()

    def clickRecIP(self):
        result = ODv1.getVideoFromCamera(self.url+'/video')
        if not result:
            self.unableToDetectCamera()

    def editUrl(self):
        self.url = self.lnIp.text()
    
    def unableToDetectCamera(self):
        print('No Connection')
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText("Connection Error")
        self.msg.setInformativeText("The Program was unable to get access to the camera")
        self.msg.setWindowTitle("Error Window")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = self.msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

