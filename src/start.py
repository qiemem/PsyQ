#!/usr/bin/env python

import sys
import os
from PyQt4 import QtCore, QtGui
from view import Ui_MainWindow
from instruction_widget import Ui_InstructionForm
from question_widget import Ui_QuestionForm

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_widget = None
        self.space_action = None

    def next_slide(self):
        pass

    def load_experiment(self, dirname):
        if not os.path.isdir(dirname):
            self.error_box("The experiment folder must be a directory.")
            self.close()
        ins_filename = os.path.join(dirname, "instructions.txt")
        que_filename = os.path.join(dirname, "questions.txt")
        flow_filename = os.path.join(dirname, "flow.txt")
        if not os.path.isfile(ins_filename):
            self.error_box("The experiment folder is missing instructions.txt.")
            self.close()
        if not os.path.isfile(que_filename):
            self.error_box("The experiment folder is missing questions.txt.")
            self.close()
        if not os.path.isfile(flow_filename):
            self.error_box("The experiment folder is missing flow.txt.")
            self.close()
        self.instructions = open(ins_filename).readlines()
        self.questions = dict()
        que = open(que_filename)
        for i in range(0, len(que), 2):
            self.question[que[i]] = que[i+1]

    def clear_display(self):
        if self.current_widget:
            self.ui.displayLayout.removeWidget(self.current_widget)
        self.current_widget = QtGui.QWidget(self.ui.displayWidget)
        self.ui.displayLayout.addWidget(self.current_widget)

    def set_instruction_label(self, text):
        self.ui.instructionLabel.setText(self.format_text(text))
            
    def set_to_instructions(self, text=None):
        self.clear_display()
        self.set_instruction_label( "Press Space to Continue")
        form = Ui_InstructionForm()
        form.setupUi(self.current_widget)
        if text:
            form.instructionLabel.setText(self.format_text(text))

    def set_to_question(self, question, answer):
        self.clear_display()
        self.set_instruction_label( "Press Space to Answer the Question" )
        form = Ui_QuestionForm()
        form.setupUi(self.current_widget)
        form.questionLabel.setText(self.format_text(text))
        form.ansLineEdit.setVisible(False)        
        
    def format_text(self, text):
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

    def error_box(self, text):
        msg = QtGui.QMessageBox(self)
        msg.setText(text)
        msg.setWindowTitle('Something Bad Happened')
        msg.open()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def showEvent(self, event):
        self.set_to_instructions()
        #self.load_experiment("start.py")


    
if __name__ == "__main__":
    instructions = None
    if os.path.isfile("instructions.txt"):
        instructions = open("instructions.txt").read()
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.showFullScreen()
    sys.exit(app.exec_())
