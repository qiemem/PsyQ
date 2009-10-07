#!/usr/bin/env python

import sys
import os
from PyQt4 import QtCore, QtGui
from view import Ui_MainWindow
from instruction_widget import Ui_InstructionForm

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_widget = None

    def clear_display(self):
        if self.current_widget:
            self.ui.displayLayout.removeWidget(self.current_widget)
            
    def set_to_instructions(self, text=None):
        self.clear_display()
        self.current_widget = QtGui.QWidget(self.ui.displayWidget)
        self.ui.displayLayout.addWidget(self.current_widget)
        form = Ui_InstructionForm()
        form.setupUi(self.current_widget)
        if text:
            form.instructionLabel.setText(self.format_instructions(text))
        
    def format_instructions(self, text):
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    instructions = None
    if os.path.isfile("instructions.txt"):
        instructions = open("instructions.txt").read()
    app = QtGui.QApplication(sys.argv)
    myapp = Main()

    if instructions:
        myapp.set_to_instructions(instructions)
    else:
        myapp.set_to_instructions()
    
    myapp.showFullScreen()
    sys.exit(app.exec_())
