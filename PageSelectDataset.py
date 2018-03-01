import sys
import Dataset as ds
import datetime, time
from PyQt5 import QtWidgets, QtGui, QtCore
class PageSelectDataset(QtWidgets.QWizardPage):
        def __init__(self):
            super(self.__class__, self).__init__()
            self.name = "Processing Window"
            self.settingcomplete = 0;
            self.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}""QMessageBox{background-color:#DEB887;}" \
                "QListWidgetItem:{font-size:10px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.initUI()

        def initUI(self):
            
            self.mainlayout = QtWidgets.QVBoxLayout()
            self.h_layout1 = QtWidgets.QHBoxLayout()
            self.h_layout2 = QtWidgets.QHBoxLayout()
            self.h_layout3 = QtWidgets.QHBoxLayout()
            self.v_layout = QtWidgets.QVBoxLayout()
            self.v1_layout = QtWidgets.QVBoxLayout()
            self.v2_layout = QtWidgets.QVBoxLayout()
            self.labeltitle = QtWidgets.QLabel()
            self.labeltitle.setText("Dataset Preprocessing Step")
            self.labeltitle.setStyleSheet("font-size:22px;font-weight:bold;font-family:Microsoft YaHei;")
            self.label1 = QtWidgets.QLabel()
            self.label2 = QtWidgets.QLabel()
            self.label3 = QtWidgets.QLabel()
            self.label1.setText("Dataset Features")
            self.label2.setText("Added Features")
            self.label3.setText("Information box")
            self.file_lb = QtWidgets.QLabel()
            self.file_lb.setText("Choose input file:")
            self.file_lb.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.file_loc_le = QtWidgets.QLineEdit()
            self.file_loc_le.setMinimumHeight(40)
            self.dirbutton = QtWidgets.QPushButton("Dir.")
            self.dirbutton.clicked.connect(self.openDir)
            self.openbutton = QtWidgets.QPushButton("Open")
            self.openbutton.clicked.connect(self.opendataset)
            self.addAllfeaturebutton = QtWidgets.QPushButton("Add all")
            self.addAllfeaturebutton.setFixedSize(150,50)
            self.addAllfeaturebutton.clicked.connect(self.addAll)
            self.resetAllfeatruebutton = QtWidgets.QPushButton("Reset all")
            self.resetAllfeatruebutton.setFixedSize(150,50)
            self.resetAllfeatruebutton.clicked.connect(self.resetAll)
            self.correlationbutton = QtWidgets.QPushButton("Correlation")
            self.correlationbutton.setFixedSize(150,50)
            self.correlationbutton.setDisabled(True)
            self.correlationbutton.clicked.connect(self.generatecorrelation)
            self.selectbutton = QtWidgets.QPushButton("Select")
            self.selectbutton.setDisabled(True)
            self.selectbutton.setFixedSize(150,50)
            self.selectbutton.clicked.connect(self.selectfeatures)
            self.listWidget = QtWidgets.QListWidget()
            font = QtGui.QFont("Microsoft YaHei",11,1)
            font2 = QtGui.QFont("Microsoft YaHei",10,1)
            self.listWidget.setFont(font)
            self.listWidget2 = QtWidgets.QListWidget()
            self.listWidget2.setFont(font)
            self.info = QtWidgets.QListWidget()
            self.info.setFont(font2)
            self.info.setFixedHeight(300)
            self.h_layout3.addWidget(self.info)
            self.listWidget.setSortingEnabled(True)
            self.listWidget2.setSortingEnabled(True)
            self.listWidget.itemClicked.connect(self.addFeature)
            self.listWidget2.itemClicked.connect(self.removeFeature)
            self.h_layout1.addWidget(self.file_lb)
            self.h_layout1.addWidget(self.file_loc_le)
            self.h_layout1.addWidget(self.dirbutton)
            self.h_layout1.addWidget(self.openbutton)
            self.v_layout.addSpacing(30)
            self.v_layout.addWidget(self.correlationbutton)
            self.v_layout.addWidget(self.addAllfeaturebutton)
            self.v_layout.addWidget(self.resetAllfeatruebutton)
            self.v_layout.addWidget(self.selectbutton)
            self.v1_layout.addWidget(self.label1)
            self.v1_layout.addWidget(self.listWidget)
            self.v2_layout.addWidget(self.label2)
            self.v2_layout.addWidget(self.listWidget2)
            self.h_layout2.addLayout(self.v1_layout)
            self.h_layout2.addLayout(self.v_layout)
            self.h_layout2.addLayout(self.v2_layout)
            self.mainlayout.addWidget(self.labeltitle)
            self.mainlayout.addSpacing(5)
            self.mainlayout.addLayout(self.h_layout1)
            self.mainlayout.addSpacing(5)
            self.mainlayout.addLayout(self.h_layout2)
            self.mainlayout.addWidget(self.label3)
            self.mainlayout.addLayout(self.h_layout3)
            self.setLayout(self.mainlayout)
        def selectfeatures(self):
            featurelist = [];
            if self.listWidget2.count()==0:
                warning = QtWidgets.QMessageBox()
                warning.setWindowTitle("Selection not allowed")
                warning.setStyleSheet("QMessageBox{background-color:#DEB887;}")
                warning.setText("There is no feature selected, add at lesat one to the list")
                warning.exec_()
                return
            for i in range(self.listWidget2.count()):
                r = self.listWidget2.item(i)
                featurelist.append(r.text())
            self.d.selectFeatures(featurelist)
            self.info.clear()
            self.info.addItem("Features selected successfully as")
            self.info.addItem(str(featurelist))
            self.info.addItem(str(datetime.datetime.now()))
            self.settingcomplete = 1;
            self.selectbutton.setDisabled(True)

        def addAll(self):
            if self.listWidget.count()==0:
                return
            for row in range(self.listWidget.count()):
                self.listWidget.setCurrentItem(self.listWidget.item(0))
                self.addFeature()
            self.settingcomplete = 0
            self.selectbutton.setDisabled(False)

        def resetAll(self):
            if self.listWidget2.count()==0:
                return
            for row in range(self.listWidget2.count()):
                self.listWidget2.setCurrentItem(self.listWidget2.item(0))
                self.removeFeature()
            self.settingcomplete = 0
            self.selectbutton.setDisabled(False)

        def openDir(self):
            dialog = QtWidgets.QFileDialog()
            self.file = dialog.getOpenFileName(self, 'Open file', '', "dataset files (*.csv)")
            self.file_loc_le.clear()
            self.file_loc_le.insert(self.file[0])

        def opendataset(self):
            if self.file_loc_le.text() == '':
                print 'No file is chosen.'
                return -1
            self.settingcomplete = 0
            self.getDataset()
            self.listWidget.clear()
            self.listWidget2.clear()
            self.correlationbutton.setDisabled(False)
            self.listWidget.clear()
            self.listWidget.addItems(self.getFeatures())
            self.listWidget.repaint()
            print 'The file \"'+ self.file[0] + '\" is open.'
            print 0

        def getDataset(self):
            self.d = ds.Dataset(self.file[0])
            self.info.clear()
            info = "Import dataset with rows & columns = "+str(self.d.nRows)+" x "+str(self.d.nColumns)
            info2 = "Filepath = "+str(self.d.filepath)
            info3 = "Filetype = "+str(self.d.type)
            info4 = "Datasettype = "+str(self.d.datasetType)
            info6 = "Filename = "+str(self.d.filename)
            self.info.addItem(info)
            self.info.addItem(info2)
            self.info.addItem(info3)
            self.info.addItem(info4)
            if self.d.hasPRN:
                info5 = "Has PRN number = "+str(len(self.d.PRNList))
                self.info.addItem(info5)
            self.info.addItem(info6)
            self.info.scrollToBottom()
            self.info.repaint()

        def getFeatures(self):
            item_init = list(self.d.featuresWithoutScintillation)
            return item_init

        def generatecorrelation(self):
            self.correlationbutton.setDisabled(True)
            self.correlationbutton.repaint()
            self.d.getCorrelationMatrix()
            time.sleep(3)
            self.correlationbutton.setDisabled(False)
            self.correlationbutton.repaint()

        def addFeature(self):
            if self.listWidget.count()==0:
                return
            f = self.listWidget.currentItem()
            r = self.listWidget.currentRow()
            self.listWidget.takeItem(r)
            self.listWidget2.addItem(f.text())
            self.listWidget.update()
            self.listWidget2.update()
            self.resetFeatures()
            new_info = "Add new feature "+str(f.text())+"     "+str(datetime.datetime.now())
            if self.info.count()>15:
                self.info.takeItem(0)
            self.info.addItem(new_info)
            self.info.scrollToBottom()
            self.info.repaint()
            self.settingcomplete = 0
            self.selectbutton.setDisabled(False)


        def removeFeature(self):
            if self.listWidget2.count()==0:
                return
            f = self.listWidget2.currentItem()
            r = self.listWidget2.currentRow()
            self.listWidget.addItem(f.text())
            self.listWidget2.takeItem(r)
            self.listWidget.update()
            self.listWidget2.update()
            self.resetFeatures()
            new_info = "Remove feature "+str(f.text())+"   "+str(datetime.datetime.now())
            if self.info.count()>15:
                self.info.takeItem(0)
            self.info.addItem(new_info)
            self.info.scrollToBottom()
            self.info.repaint()
            self.settingcomplete = 0
            self.selectbutton.setDisabled(False)

        def resetFeatures(self):
            item2 = list()
            for r in range(self.listWidget2.count()):
                i = self.listWidget2.item(r)
                featurename = i.text()
                item2.append(featurename)
            self.d.selectFeatures(item2)