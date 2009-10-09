# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instruction_widget.ui'
#
# Created: Thu Oct  8 14:12:11 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_InstructionForm(object):
    def setupUi(self, InstructionForm):
        InstructionForm.setObjectName("InstructionForm")
        InstructionForm.resize(497, 294)
        self.gridLayout = QtGui.QGridLayout(InstructionForm)
        self.gridLayout.setObjectName("gridLayout")
        self.instructionLabel = QtGui.QLabel(InstructionForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instructionLabel.sizePolicy().hasHeightForWidth())
        self.instructionLabel.setSizePolicy(sizePolicy)
        self.instructionLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.instructionLabel.setMaximumSize(QtCore.QSize(800, 16777215))
        self.instructionLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.instructionLabel.setTextFormat(QtCore.Qt.RichText)
        self.instructionLabel.setScaledContents(True)
        self.instructionLabel.setWordWrap(True)
        self.instructionLabel.setObjectName("instructionLabel")
        self.gridLayout.addWidget(self.instructionLabel, 0, 0, 1, 1)

        self.retranslateUi(InstructionForm)
        QtCore.QMetaObject.connectSlotsByName(InstructionForm)

    def retranslateUi(self, InstructionForm):
        InstructionForm.setWindowTitle(QtGui.QApplication.translate("InstructionForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.instructionLabel.setText(QtGui.QApplication.translate("InstructionForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; color:#414141;\">Instructions will go here at some point. They will tell the subject what to do throughout the experiment in such a way so as the subject does not actually what is going on. This is very important because all psychology experiments rely on deception.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

