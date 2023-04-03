from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(430, 247)
        Dialog.setMinimumSize(QtCore.QSize(280, 200))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.startBtn = QtGui.QPushButton(Dialog)
        self.startBtn.setObjectName(_fromUtf8("startBtn"))
        self.verticalLayout.addWidget(self.startBtn)
        self.rxList = QtGui.QListWidget(Dialog)
        self.rxList.setObjectName(_fromUtf8("rxList"))
        self.verticalLayout.addWidget(self.rxList)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.passBtn = QtGui.QPushButton(Dialog)
        self.passBtn.setObjectName(_fromUtf8("passBtn"))
        self.horizontalLayout.addWidget(self.passBtn)
        self.failBtn = QtGui.QPushButton(Dialog)
        self.failBtn.setObjectName(_fromUtf8("failBtn"))
        self.horizontalLayout.addWidget(self.failBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Websocket Server (Fake)", None))
        self.startBtn.setText(_translate("Dialog", "Start Server", None))
        self.passBtn.setText(_translate("Dialog", "Pass", None))
        self.failBtn.setText(_translate("Dialog", "Fail", None))