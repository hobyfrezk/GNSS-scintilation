import sys
import os
import Dataset as ds
import datetime
import Algorithm as Ag
from PyQt5 import QtWidgets, QtGui, QtCore
from PageStart import PageStart
from PageSelectDataset import PageSelectDataset
from PageSelectAlgorithm import PageSelectAlgorithm

class Mainframe(QtWidgets.QWizard):
    def __init__(self):
        super(Mainframe, self).__init__(parent=None)
        self.setWizardStyle(1)
        self.setFixedSize(800, 900)
        self.center()
        self.initUI()
        self.PageStart = PageStart()
        self.setPage(1,self.PageStart)
        self.PageSelectDataset = PageSelectDataset()
        self.setPage(2,self.PageSelectDataset)
        self.PageSelectAlgorithm = PageSelectAlgorithm()
        self.PageSelectAlgorithm.setFinalPage(False)
        self.setPage(3,self.PageSelectAlgorithm)        
        self.setOption(QtWidgets.QWizard.HaveHelpButton)
        self.button(QtWidgets.QWizard.CancelButton).clicked.disconnect()
        self.button(QtWidgets.QWizard.CancelButton).clicked.connect(self.cancelRequested)
        self.button(QtWidgets.QWizard.NextButton).clicked.disconnect()
        self.button(QtWidgets.QWizard.NextButton).clicked.connect(self.nextclicked)
        self.button(QtWidgets.QWizard.BackButton).clicked.disconnect()
        self.button(QtWidgets.QWizard.BackButton).clicked.connect(self.backclicked)
        self.button(QtWidgets.QWizard.HelpButton).clicked.disconnect()
        self.button(QtWidgets.QWizard.HelpButton).clicked.connect(self.helpclicked)
        self.setOption(QtWidgets.QWizard.NoBackButtonOnStartPage)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowCloseButtonHint)
        self.helppage = QtWidgets.QLabel()
        self.helppage.setWindowTitle("User-manual")
    def helpclicked(self):
        pic_help = QtGui.QPixmap(str('helppage.jpg'))
        self.helppage.setPixmap(pic_help.scaled(720, 720))
        if not self.helppage.isVisible():
            self.helppage.show()

    def initUI(self):
        self.setStyleSheet("QWizard{background-color:#20B2AA}""QPushButton:hover{background-color:#98FB98;border-radius:4px;font-size:14px;font-weight:bold;font-family:Microsoft YaHei Light;}" \
            "QListWidget{background-color:#DEDEDE;}" \
            "QPushButton{background-color:#DBDBDB;border:0.75px solid black;border-radius:4px;min-width:80;min-height:40;font-size:14px;font-weight:bold;font-family:Microsoft YaHei Light;}" \
            "QMessageBox{background-color:#DEB887;font-size:18px;font-weight:bold;font-family:Microsoft YaHei Light;}" \
            "QListWidget{border:0.75px solid black;border-radius:4px}""QWizardPage{border-radius:5;}" \
            "QLineEdit{font-size:14px;font-weight:bold;font-family:Microsoft YaHei;border:1px solid black;border-radius:2.5px;}" \
            "QListWidget:hover{background-color:#B0E0E6;}")
        self.setWindowTitle('Detection Tool')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def cancelRequested(self, event):
        reply = QtWidgets.QMessageBox()
        r = reply.question(self, 'Warning', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | \
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if r == QtWidgets.QMessageBox.Yes:
            self.reject()
    def nextclicked(self):
        currentpage = self.currentPage()
        if currentpage.settingcomplete == 1:
            if self.currentId()== 2:
                self.PageSelectAlgorithm.passdataset(currentpage.d)
                self.next()
                self.button(QtWidgets.QWizard.NextButton).setDisabled(True)
            else:
                self.next()
        else:
            warning = QtWidgets.QMessageBox()
            warning.setWindowTitle("Can not go to next step")
            warning.setStyleSheet("QMessageBox{background-color:#DEB887;}")
            warning.setText("Incomplete/changed setting"+'\n'+"1) Click select before going to next page"+'\n'+"2) Check if features are added or removed")
            warning.exec_()
            return
    def backclicked(self):
        if self.currentId == 3:
            self.button(QtWidgets.QWizard.NextButton).setDisabled(False)
        self.back()