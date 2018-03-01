import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class PageStart(QtWidgets.QWizardPage):
        def __init__(self):
            super(self.__class__, self).__init__()
            self.name = "Start"
            self.settingcomplete = 1
            self.initUI()
        def initUI(self):
            self.tooltitle = QtWidgets.QLabel()
            self.tooltitle.setText('Scintillation Detection Tool')
            self.tooltitle.setMinimumSize(150, 100)
            self.tooltitle.setAlignment(QtCore.Qt.AlignCenter)
            self.tooltitle.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:25px;font-weight:bold;font-family:Microsoft YaHei;}")
            pic_icon = QtGui.QPixmap(str('icon.png'))
            self.main_v_box = QtWidgets.QVBoxLayout()
            self.label1 = QtWidgets.QLabel()
            self.label1.setPixmap(pic_icon.scaled(120, 120))
            self.label1.setAlignment(QtCore.Qt.AlignCenter)
            self.label1.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.label2 = QtWidgets.QLabel()
            self.label2.setMinimumSize(250, 150)
            self.label2.setText("------------------------------------  Author  ------------------------------------")
            self.label2.setAlignment(QtCore.Qt.AlignCenter)
            self.label2.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.label3 = QtWidgets.QLabel()
            self.label3.setText("GROUP B")
            self.label3.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.label3.setAlignment(QtCore.Qt.AlignCenter)
            self.label4 = QtWidgets.QLabel()
            self.label4.setText("            Yejia Xu | Qizhen Lu | Minghao Liu | Chongshun Wang | Ayub Yimer Endris")
            self.label4.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.label5 = QtWidgets.QLabel()
            self.label5.setText("Professors: Fabio Dovis | Nicola Linty | Alfredo Favenza | Alessandro Farasin")
            self.label5.setStyleSheet("QLabel{color:rgb(96,96,96,255);font-size:18px;font-weight:bold;font-family:Microsoft YaHei;}")
            self.label5.setAlignment(QtCore.Qt.AlignCenter)
            self.main_v_box.addWidget(self.tooltitle)
            self.main_v_box.addWidget(self.label1)
            self.main_v_box.addWidget(self.label2)
            self.main_v_box.addWidget(self.label3)
            self.main_v_box.addWidget(self.label4)
            self.main_v_box.addWidget(self.label5)
            self.main_h_box = QtWidgets.QHBoxLayout()
            self.main_v_box.addLayout(self.main_h_box)
            self.setLayout(self.main_v_box)

        def getCurrentPagename(self):
            return self.name
        def readyfornext(self):
            print "Nextbutton clicked and go to next page"


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PageStart()
    w.show()
    sys.exit(app.exec_())

    