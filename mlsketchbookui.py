# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mlsketchbookui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmmain(object):
    def setupUi(self, frmmain):
        frmmain.setObjectName("frmmain")
        frmmain.resize(1260, 822)
        self.image_disp = QtWidgets.QGraphicsView(frmmain)
        self.image_disp.setGeometry(QtCore.QRect(460, 0, 801, 811))
        self.image_disp.setObjectName("image_disp")
        self.lstfilename = QtWidgets.QListWidget(frmmain)
        self.lstfilename.setGeometry(QtCore.QRect(10, 50, 441, 561))
        self.lstfilename.setObjectName("lstfilename")
        self.bttnprev = QtWidgets.QPushButton(frmmain)
        self.bttnprev.setGeometry(QtCore.QRect(10, 620, 211, 61))
        self.bttnprev.setObjectName("bttnprev")
        self.bttnnext = QtWidgets.QPushButton(frmmain)
        self.bttnnext.setGeometry(QtCore.QRect(240, 620, 211, 61))
        self.bttnnext.setObjectName("bttnnext")
        self.bttnsetsrc_fldr = QtWidgets.QPushButton(frmmain)
        self.bttnsetsrc_fldr.setGeometry(QtCore.QRect(10, 0, 221, 51))
        self.bttnsetsrc_fldr.setObjectName("bttnsetsrc_fldr")
        self.bttnsetdest_folder = QtWidgets.QPushButton(frmmain)
        self.bttnsetdest_folder.setGeometry(QtCore.QRect(230, 0, 221, 51))
        self.bttnsetdest_folder.setObjectName("bttnsetdest_folder")
        self.bttnclr = QtWidgets.QPushButton(frmmain)
        self.bttnclr.setGeometry(QtCore.QRect(240, 690, 211, 121))
        self.bttnclr.setObjectName("bttnclr")

        self.retranslateUi(frmmain)
        QtCore.QMetaObject.connectSlotsByName(frmmain)

    def retranslateUi(self, frmmain):
        _translate = QtCore.QCoreApplication.translate
        frmmain.setWindowTitle(_translate("frmmain", "MLSketchbook"))
        self.bttnprev.setText(_translate("frmmain", "<<<<"))
        self.bttnnext.setText(_translate("frmmain", ">>>>"))
        self.bttnsetsrc_fldr.setText(_translate("frmmain", "Set Source Folder..."))
        self.bttnsetdest_folder.setText(_translate("frmmain", "Set Ground Truth Folder..."))
        self.bttnclr.setText(_translate("frmmain", "Clear Drawing"))
