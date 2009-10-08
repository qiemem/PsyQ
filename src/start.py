#!/usr/bin/env python

import sys
import os
from random import shuffle
from PyQt4 import QtCore, QtGui
from view import Ui_MainWindow
from instruction_widget import Ui_InstructionForm
from question_widget import Ui_QuestionForm

class Slide(QtGui.QWidget):
    def __init__(self, parent_widget, space_action, instruction_text):
        QtGui.QWidget.__init__(self, parent_widget)
        self.space_action = space_action
        self.instruction_text = instruction_text

    def format_text(self, text):
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

class InstructionSlide(Slide):
    def __init__(self, parent_widget, text, next_slide_fn):
        instruction_text = "Press Space to Continue"
        space_action = next_slide_fn
        Slide.__init__(self, parent_widget, space_action, instruction_text)
        ui = Ui_InstructionForm()
        ui.setupUi(self)
        ui.instructionLabel.setText(self.format_text(text))

class QuestionSlide(Slide):
    def __init__(self, parent_widget, question, answer, instruction_text_fn, next_slide_fn):
        self.answer = answer
        instruction_text = "Press Space to Answer the Question"
        space_action = self.open_answer_input
        Slide.__init__(self, parent_widget, space_action, instruction_text)
        self.ui = Ui_QuestionForm()
        self.ui.setupUi(self)
        self.ui.questionLabel.setText(self.format_text(question))
        self.ui.ansLineEdit.hide()
        self.ui.submitAnswerButton.hide()
        self.set_inst_text = instruction_text_fn
        self.next_slide = next_slide_fn

    def open_answer_input(self):
        self.ui.ansLineEdit.show()
        self.ui.submitAnswerButton.show()
        self.ui.ansLineEdit.setFocus()
        self.instruction_text = ""
        self.connect(self.ui.submitAnswerButton, QtCore.SIGNAL('clicked()'), self.submit_answer)
        self.space_action = lambda : None
        self.set_inst_text(self.instruction_text)
        

    def submit_answer(self):
        ans = str(self.ui.ansLineEdit.text()).strip()
        if ans.upper()==self.answer:
            self.set_inst_text("Correct! Press Space to Continue")
            self.ui.questionLabel.destroy()
            self.ui.ansLineEdit.destroy()
            self.ui.submitAnswerButton.destroy()
            self.space_action = self.next_slide
        else:
            self.set_inst_text("'"+ans+"' is Incorrect; Please Try Again")
        
class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_slide = None

    def next_slide(self):
        # flow is a stack of instructions.
        if len(self.flow)==0:
            self.error_box('The experiment is over!')
            self.close()
            return
        cmd = self.flow.pop()
        if cmd[0]=="instruction":
            self.set_to_instructions(self.instructions[cmd[1]])
        elif cmd[0]=="questions":
            q = self.question_list.pop()
            print(q)
            print(self.questions[q])
            self.set_to_question(q, self.questions[q])
            if cmd[1]>1:
                self.flow.append(("questions", cmd[1]-1))

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
        self.instructions = open(ins_filename,'U').readlines()
        self.questions = dict()
        que = open(que_filename,'U').readlines()
        for i in range(0, len(que)-1, 2):
            self.questions[que[i].strip()] = que[i+1].strip().upper()
        self.question_list = self.questions.keys()
        print(self.question_list)
        shuffle(self.question_list)
        flow_raw = open(flow_filename,'U').readlines()
        self.flow = list()
        for l in flow_raw:
            cmd = l.split(" ")
            if len(cmd)==0:
                continue
            if cmd[0] == "instruction":
                self.flow.append(("instruction", int(cmd[1])))
            elif cmd[0] == "questions":
                self.flow.append(("questions", int(cmd[1])))
        # We treat flow as a stack of instructions with the
        # next one at the end. This is just so that we can
        # use pop and append in a natural manner.
        self.flow.reverse()

    def clear_slide(self):
        if self.current_slide:
            self.ui.displayLayout.removeWidget(self.current_slide)
            self.current_slide.close()

    def set_slide(self, slide):
        self.clear_slide()
        self.current_slide = slide
        self.ui.displayLayout.addWidget(slide)
        self.set_instruction_label(slide.instruction_text)

    def set_instruction_label(self, text):
        self.ui.instructionLabel.setText(self.format_text(text))
            
    def set_to_instructions(self, text):
        self.set_slide(InstructionSlide(self.ui.displayWidget, text, self.next_slide))

    def set_to_question(self, question, answer):
        self.set_slide(QuestionSlide(self.ui.displayWidget, question, answer, self.set_instruction_label, self.next_slide))
        
    def error_box(self, text):
        msg = QtGui.QMessageBox(self)
        msg.setText(text)
        msg.setWindowTitle('Something Bad Happened')
        msg.open()

    def format_text(self, text):
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key_Space and self.current_slide:
            self.current_slide.space_action()

    def showEvent(self, event):
        self.load_experiment("test")
        self.next_slide()

    
if __name__ == "__main__":
    instructions = None
    if os.path.isfile("instructions.txt"):\
        instructions = open("instructions.txt").read()
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    myapp.set_to_instructions(instructions)
    myapp.showFullScreen()
    sys.exit(app.exec_())
