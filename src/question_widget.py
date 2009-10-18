# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'question_widget.ui'
#
# Created: Tue Oct 13 19:31:55 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QuestionForm(object):
    def setupUi(self, QuestionForm):
        QuestionForm.setObjectName("QuestionForm")
        QuestionForm.resize(476, 99)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QuestionForm.sizePolicy().hasHeightForWidth())
        QuestionForm.setSizePolicy(sizePolicy)
        QuestionForm.setMaximumSize(QtCore.QSize(500, 16777215))
        self.gridLayout = QtGui.QGridLayout(QuestionForm)
        self.gridLayout.setObjectName("gridLayout")
        self.questionLabel = QtGui.QLabel(QuestionForm)
        self.questionLabel.setObjectName("questionLabel")
        self.gridLayout.addWidget(self.questionLabel, 0, 0, 1, 2)
        self.ansLineEdit = QtGui.QLineEdit(QuestionForm)
        self.ansLineEdit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ansLineEdit.sizePolicy().hasHeightForWidth())
        self.ansLineEdit.setSizePolicy(sizePolicy)
        self.ansLineEdit.setMaximumSize(QtCore.QSize(700, 16777215))
        self.ansLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ansLineEdit.setObjectName("ansLineEdit")
        self.gridLayout.addWidget(self.ansLineEdit, 2, 0, 1, 1)
        self.submitAnswerButton = QtGui.QPushButton(QuestionForm)
        self.submitAnswerButton.setObjectName("submitAnswerButton")
        self.gridLayout.addWidget(self.submitAnswerButton, 2, 1, 1, 1)

        self.retranslateUi(QuestionForm)
        QtCore.QObject.connect(self.ansLineEdit, QtCore.SIGNAL("returnPressed()"), self.submitAnswerButton.click)
        QtCore.QMetaObject.connectSlotsByName(QuestionForm)

    def retranslateUi(self, QuestionForm):
        QuestionForm.setWindowTitle(QtGui.QApplication.translate("QuestionForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.questionLabel.setText(QtGui.QApplication.translate("QuestionForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; color:#404040;\">Question?</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.submitAnswerButton.setText(QtGui.QApplication.translate("QuestionForm", "Submit", None, QtGui.QApplication.UnicodeUTF8))

