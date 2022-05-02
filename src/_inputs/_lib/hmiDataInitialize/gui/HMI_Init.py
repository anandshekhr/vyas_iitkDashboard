from http import client
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_HMIWindow(object):
    def setupUi(self, HMIWindow):
        if not HMIWindow.objectName():
            HMIWindow.setObjectName(u"HMIWindow")
        HMIWindow.resize(707, 442)
        self.centralwidget = QWidget(HMIWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.horizontalLayout.addWidget(self.tableView)
        HMIWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(HMIWindow)
        self.statusbar.setObjectName(u"statusbar")
        HMIWindow.setStatusBar(self.statusbar)
        self.retranslateUi(HMIWindow)
        QMetaObject.connectSlotsByName(HMIWindow)
    # setupUi

    def retranslateUi(self, HMIWindow):
        HMIWindow.setWindowTitle(QCoreApplication.translate("HMIWindow", u"HMI Data", None))


