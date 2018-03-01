import sys
import os
import Dataset as ds
import datetime
import Algorithm as Ag
from PyQt5 import QtWidgets, QtGui, QtCore
import Evaluation as ev
class PageSelectAlgorithm(QtWidgets.QWizardPage):
        def __init__(self):
            super(self.__class__, self).__init__()
            self.name = "Algorithm selection window:"
            self.if_setprn = 0
            self.if_setdate = 0
            self.progresscomplete = 0
            self.setdefaultpara()            
            self.algo1para = {}
            self.algo2para = {}
            self.algo3para = {}
            self.algo4para = {}
            self.algo1para = dict(self.algo1paradefault.items()+self.algo1para.items())
            self.algo2para = dict(self.algo2paradefault.items()+self.algo2para.items())
            self.algo3para = dict(self.algo3paradefault.items()+self.algo3para.items())
            self.algo4para = dict(self.algo4paradefault.items()+self.algo4para.items())
            self.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:15px;font-weight:bold;font-family:Microsoft YaHei;}""QMessageBox{background-color:#DEB887;}")
            self.algoSet = Ag.Algorithm('decision tree',self.algo1para)
            self.prnSet = 0
            self.dateSet = 0
            self.initUI()
        def nextId(self):
            return 1
        def passdataset(self,dataset):
            self.dataset = dataset
            self.prnlist =dataset.PRNList.keys()
            self.dt = dataset.DateList.keys()
            self.datelist.clear()
            self.satnumlist.clear()
            for i in range(len(self.prnlist)):
                n = self.prnlist[i]
                self.satnumlist.addItem(str(n))
            for i in range(len(self.dt)):
                d = self.dt[i]
                self.datelist.addItem(str(d))
        def setdefaultpara(self):
            self.algo1paradefault = {'max_depth':2}
            self.algo2paradefault = {'penalty':'l1', 'tol':0.00001, 'C':1.0, 'class_weight':None}
            self.algo3paradefault = {'n_estimators':20, 'max_features':'auto', 'min_samples_leaf':300, 'max_depth':5}
            self.algo4paradefault = {'base_estimator':'decision tree', 'n_estimators':60,'learning_rate':1,'algorithm':'SAMME'}
        def initUI(self):
            self.labeltitle = QtWidgets.QLabel()
            self.labeltitle.setText("Algorithm chosen---evaluation---comparision plot Step")
            self.labeltitle.setStyleSheet("font-size:20px;font-weight:bold;font-family:Microsoft YaHei;")
            font = QtGui.QFont("Microsoft YaHei",11,1)
            font2 = QtGui.QFont("Microsoft YaHei",10,1)
            self.mainlayout = QtWidgets.QVBoxLayout()
            self.h_box1 = QtWidgets.QHBoxLayout()
            self.h2_box1 = QtWidgets.QHBoxLayout()
            self.h3_box1 = QtWidgets.QHBoxLayout()
            self.v4_box1 = QtWidgets.QVBoxLayout()
            self.v_box1 = QtWidgets.QVBoxLayout()
            self.v1_box1 = QtWidgets.QVBoxLayout()
            self.v2_box1 = QtWidgets.QVBoxLayout()
            self.v3_box1 = QtWidgets.QVBoxLayout()
            self.v4_box1 = QtWidgets.QVBoxLayout()
            self.v5_box1 = QtWidgets.QVBoxLayout()
            self.label1 = QtWidgets.QLabel()
            self.label1.setText("Algorithm List")
            self.label2 = QtWidgets.QLabel()
            self.label2.setText("Parameter List")
            self.label3 = QtWidgets.QLabel()
            self.label3.setText("Information Box")
            self.label4 = QtWidgets.QLabel()
            self.label4.setText("SatNum List")
            self.label5 = QtWidgets.QLabel()
            self.label5.setText("Date List")
            self.Algochooselist = QtWidgets.QListWidget()
            self.Algochooselist.setCurrentRow(0)
            self.paralist = QtWidgets.QListWidget()
            self.paralist.setSortingEnabled(True)
            self.paralist.setFont(font2)
            self.satnumlist = QtWidgets.QListWidget()
            self.satnumlist.clicked.connect(self.setprn)
            self.datelist = QtWidgets.QListWidget()
            self.datelist.clicked.connect(self.setdate)
            #self.satnumlist.setSortingEnabled(True)
            self.infoconsole = QtWidgets.QListWidget()
            self.infoconsole.setFixedHeight(270)
            self.infoconsole.setFont(font2)
            self.Algochooselist.clicked.connect(self.getalgopara)
            self.Algochooselist.itemSelectionChanged.connect(self.getalgopara)
            self.paralist.clicked.connect(self.parasetting)
            module1 = Algodisplaymodule("decision tree")
            module2 = Algodisplaymodule("support vector machine")
            module3 = Algodisplaymodule("random forest")
            module4 = Algodisplaymodule("adaboost")
            self.item1 = QtWidgets.QListWidgetItem()
            self.item2 = QtWidgets.QListWidgetItem()
            self.item3 = QtWidgets.QListWidgetItem()
            self.item4 = QtWidgets.QListWidgetItem()
            self.buttonplot = QtWidgets.QPushButton("Plot")
            self.buttonplot.setFixedSize(80,73)
            self.buttonplot.setDisabled(True)
            self.buttonplot.clicked.connect(self.buttonplotclicked)
            self.lockPlot = True
            self.buttonreset = QtWidgets.QPushButton("Reset")
            self.buttonset =QtWidgets.QPushButton("Set")
            self.buttonset.setDisabled(True)
            self.lockSet = False
            self.buttonreset.setFixedSize(80,73)
            self.buttonset.setFixedSize(80,73)
            self.buttonreset.clicked.connect(self.buttonresetclicked)
            self.buttonset.clicked.connect(self.buttonsetclicked)
            self.buttonevaluate = QtWidgets.QPushButton("Evaluate")
            self.buttonevaluate.clicked.connect(self.buttonevaluateclicked) 
            self.buttonevaluate.setDisabled(True)
            self.buttonevaluate.setFixedSize(80,73)
            self.item1.setSizeHint(module1.sizeHint())
            self.item1.setText("   decision tree")
            self.item2.setSizeHint(module2.sizeHint())
            self.item2.setText("   support vector machine")
            self.item3.setSizeHint(module3.sizeHint())
            self.item3.setText("   random forest")
            self.item4.setSizeHint(module4.sizeHint())
            self.item4.setText("   adaboost")
            self.Algochooselist.addItem(self.item1)
            self.Algochooselist.setItemWidget(self.item1,Algodisplaymodule("   "+"decision tree"))
            self.Algochooselist.addItem(self.item2)
            self.Algochooselist.setItemWidget(self.item2,Algodisplaymodule("   "+"support vector machine"))
            self.Algochooselist.addItem(self.item3)
            self.Algochooselist.setItemWidget(self.item3,Algodisplaymodule("   "+"random forest"))
            self.Algochooselist.addItem(self.item4)
            self.Algochooselist.setItemWidget(self.item4,Algodisplaymodule("   "+"adaboost"))
            self.v1_box1.addWidget(self.label1)
            self.v1_box1.addWidget(self.Algochooselist)
            self.v2_box1.addWidget(self.label2)
            self.v2_box1.addWidget(self.paralist)
            self.v2_box1.addWidget(self.label4)
            self.v2_box1.addWidget(self.satnumlist)
            self.v3_box1.addWidget(self.label5)
            self.v3_box1.addWidget(self.datelist)
            self.h2_box1.addLayout(self.v3_box1)
            self.v5_box1.addSpacing(24)
            self.v5_box1.addWidget(self.buttonplot)
            self.h2_box1.addLayout(self.v5_box1)
            self.v_box1.addSpacing(24)
            self.v_box1.addWidget(self.buttonreset)
            self.v_box1.addSpacing(6)
            self.v_box1.addWidget(self.buttonset)
            self.v_box1.addSpacing(6)
            self.v_box1.addWidget(self.buttonevaluate)
            self.h_box1.addLayout(self.v1_box1)
            self.h3_box1.addLayout(self.v2_box1)
            self.h3_box1.addLayout(self.v_box1)
            self.v4_box1.addLayout(self.h3_box1)
            self.v4_box1.addLayout(self.h2_box1)
            self.h_box1.addLayout(self.v4_box1)
            self.mainlayout.addWidget(self.labeltitle)
            self.mainlayout.addLayout(self.h_box1)
            self.mainlayout.addWidget(self.label3)
            self.mainlayout.addWidget(self.infoconsole)
            self.Algochooselist.repaint()
            self.setLayout(self.mainlayout)

        def getalgopara(self):
            currentalgo = self.Algochooselist.currentItem()
            if currentalgo.text()=="   " + "decision tree":
                self.paralist.clear()
                p = self.algo1para
                self.paralist.addItem("max_depth"+"="+str(p['max_depth']))
            elif currentalgo.text()=="   " + "support vector machine":
                self.paralist.clear()
                p = self.algo2para
                self.paralist.addItem("penalty"+"="+str(p['penalty']))
                self.paralist.addItem("tol"+"="+str(p['tol']))
                self.paralist.addItem("C"+"="+str(p['C']))
                self.paralist.addItem("class_weight"+"="+str(p['class_weight']))
            elif currentalgo.text()=="   " + "random forest":
                #(n_estimators=20, max_features='auto', min_samples_leaf=300, max_depth=5)
                self.paralist.clear()
                p = self.algo3para
                self.paralist.addItem("n_estimators"+"="+str(p['n_estimators']))
                self.paralist.addItem("max_features"+"="+str(p['max_features']))
                self.paralist.addItem("min_samples_leaf"+"="+str(p['min_samples_leaf']))
                self.paralist.addItem("max_depth"+"="+str(p['max_depth']))
            elif currentalgo.text()=="   " + "adaboost":
                #(base_estimator=DecisionTreeClassifier(max_depth=2), n_estimators=60,learning_rate=1,algorithm='SAMME')
                self.paralist.clear()
                p = self.algo4para
                self.paralist.addItem("base_estimator"+"="+str(p['base_estimator']))
                self.paralist.addItem("n_estimators"+"="+str(p['n_estimators']))
                self.paralist.addItem("learning_rate"+"="+str(p['learning_rate']))
                self.paralist.addItem("algorithm"+"="+str(p['algorithm']))
            self.paralist.update()
            self.buttonset.setDisabled(False)
            self.buttonevaluate.setDisabled(True)

        def setprn(self):
            c = self.satnumlist.currentItem()
            self.prn = int(c.text())
            if c.text()==str(self.prnSet):
                print "prn not changed"
            else:
                print "prn changed"
            self.if_setprn = 1
            self.if_plot()


            
        def setdate(self):
            d = self.datelist.currentItem()
            self.if_Setdate = 1
            self.date = int(d.text())
            if d.text()==str(self.dateSet):
                print "date not changed"
            else:
                print "date changed"
            self.if_setdate = 1
            self.if_plot()

        def buttonevaluateclicked(self):
            self.lockSet = True
            self.buttonset.setDisabled(True)
            self.progresscomplete = 0
            self.buttonevaluate.setDisabled(True)
            self.thread = EvaluationThread(self.dataset,self.algoSet,self.prnSet)
            self.thread.finishsignal.connect(self.evaluationcomplete)
            self.thread.start()
            self.infoconsole.addItem("Evaluation in progress--------------------------------------------------------------")

        def evaluationcomplete(self):
            self.progresscomplete = 1
            self.lockSet = False
            self.infoconsole.clear()
            self.infoconsole.addItem("Evaluation score:")
            self.infoconsole.addItem(str(self.thread.score))
            self.infoconsole.addItem("Score mean:")
            self.infoconsole.addItem(str(self.thread.meanscore))
            self.infoconsole.update()
            self.if_plot()
            return

        def if_plot(self):
            if self.progresscomplete + self.if_setdate + self.if_setprn == 3:
                self.buttonplot.setDisabled(False)

        def buttonsetclicked(self):
            self.buttonset.setDisabled(True)
            c = self.Algochooselist.currentItem()
            if c.text()==("   "+ self.algoSet.algorithm):
                print "algorithm not changed"
            else:
                print "algorithm changed"
                self.buttonplot.setDisabled(True)
            if c.text()=="   " + "decision tree":
                print self.algo1para
                self.infoconsole.clear()
                self.algo1 = Ag.Algorithm('decision tree',self.algo1para)
                self.algoSet = self.algo1
                self.infoconsole.addItem("Decision tree algorithm set"+"      "+str(datetime.datetime.now()))
                self.infoconsole.addItem(str(self.algo1para))
                self.infoconsole.repaint()
            elif c.text()=="   " + "support vector machine":
                print self.algo2para
                self.infoconsole.clear()
                self.algo2 = Ag.Algorithm('support vector machine',self.algo2para)
                self.algoSet = self.algo2
                self.infoconsole.addItem("support vector machine set"+"      "+str(datetime.datetime.now()))
                self.infoconsole.addItem(str(self.algo2para))
                self.infoconsole.repaint()
            elif c.text()=="   " + "random forest":
                print self.algo3para
                self.infoconsole.clear()
                self.algo3 = Ag.Algorithm('random forest',self.algo3para)
                self.algoSet = self.algo3
                self.infoconsole.addItem("random forest set"+"      "+str(datetime.datetime.now()))
                self.infoconsole.addItem(str(self.algo3para))
                self.infoconsole.repaint()
            elif c.text()=="   " + "adaboost":
                print self.algo4para
                self.infoconsole.clear()
                self.algo4 = Ag.Algorithm('adaboost',self.algo4para)
                self.algoSet = self.algo4
                self.infoconsole.addItem("adaboost set"+"      "+str(datetime.datetime.now()))
                self.infoconsole.addItem(str(self.algo4para))
                self.infoconsole.repaint()
            self.infoconsole.addItem("Selected Satellite No = "+str(self.prnSet))
            self.infoconsole.addItem("Selected date = " + str(self.dateSet))
            self.buttonevaluate.setDisabled(False)

        def parasetting(self):
            text, ok = QtWidgets.QInputDialog.getText(self,"Setting","parameter")
            i = self.paralist.currentItem()
            if (ok)and(text.strip()):
                self.value = text
                p = i.text().split("=")
                self.paralist.takeItem(self.paralist.currentRow())
                self.paralist.addItem(p[0]+"="+text)
                self.paralist.repaint()
            else:
                return
            c = self.Algochooselist.currentItem()
            if c.text()=="   " + "decision tree":                
                self.algo1para[p[0]] = int(self.value)   
                print self.algo1para
            elif c.text()=="   " + "support vector machine":
                if (p[0] == "tol")or(p[0] == "C"):
                    self.algo2para[p[0]] = float(self.value)   
                else:
                    self.algo2para[p[0]] = self.value
                print self.algo2para
            elif c.text()=="   " + "random forest":
                if (p[0] == "n_estimators")or(p[0] == "min_samples_leaf")or(p[0] == "max_depth"):
                    self.algo3para[p[0]] = int(self.value)   
                else:
                    self.algo3para[p[0]] = self.value 
                print self.algo3para
            elif c.text()=="   " + "adaboost":
                if (p[0] == "n_estimators")or(p[0] == "learning_rate"):
                    self.algo4para[p[0]] = int(self.value)   
                else:
                    self.algo4para[p[0]] = self.value   
                print self.algo4para 
            print self.algo1paradefault
            self.buttonset.setDisabled(False)

        def buttonresetclicked(self):
            c = self.Algochooselist.currentItem()
            if c.text()=="   " + "decision tree":
                self.algo1para = {}
                self.algo1para = dict(self.algo1paradefault.items()+self.algo1para.items())
                
            elif c.text()=="   " + "support vector machine":
                self.algo2para.clear()
                self.algo2para = dict(self.algo2paradefault.items()+self.algo2para.items())
                print self.algo2para
            elif c.text()=="   " + "random forest":
                self.algo3para.clear()
                self.algo3para = dict(self.algo3paradefault.items()+self.algo3para.items())
                print self.algo3paradefault
                print self.algo3para
            elif c.text()=="   " + "adaboost":
                self.algo4para.clear()
                self.algo4para = dict(self.algo4paradefault.items()+self.algo4para.items())
            self.getalgopara()

        def isFinalPage(self):
            return False
            
        def buttonplotclicked(self):
            self.infoconsole.addItem("Plot prn = "+str(self.prn)+" date = "+str(self.date))
            eva =  self.thread.e
            eva.plot_PRN_Date(self.prn, ['S4','C/N0','Elevation'], self.date)
                

class EvaluationThread(QtCore.QThread):
    finishsignal = QtCore.pyqtSignal()
    def __init__(self,dataset,algo,prn):
        super(EvaluationThread,self).__init__()
        self.algo = algo
        self.dataset = dataset
        self.prn = prn
    def run(self):
        self.e =ev.Evaluation(self.dataset,self.algo)
        self.score = self.e.getCrossValScores()
        self.meanscore = self.e.mean_scores_K_fold
        self.finishsignal.emit()        

class Algodisplaymodule(QtWidgets.QWidget):
        def __init__(self,name):
             super(self.__class__, self).__init__()
             self.name = name
             self.initUI()
        def initUI(self):
            self.label1 = QtWidgets.QLabel()
            self.label1.setText(str(self.name))
            self.h_box = QtWidgets.QHBoxLayout()
            self.mainlayout = QtWidgets.QVBoxLayout()
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.label1.setStyleSheet("QLabel:hover{background-color:#CD6839;border:3px black;border-radius:10px;}""QLabel{background-color:#C4C4C4;border-radius:10px;}")
            self.label1.setAutoFillBackground(True)
            self.h_box.addWidget(self.label1)
            self.mainlayout.addLayout(self.h_box)
            self.setLayout(self.mainlayout)
        def sizeHint(self):
            return QtCore.QSize(200,65)

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PageSelectAlgorithm()
    w.show()
    sys.exit(app.exec_())