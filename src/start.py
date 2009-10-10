#!/usr/bin/env python

import sys
import os
from random import shuffle
from time import time
from datetime import datetime
from PyQt4 import QtCore, QtGui
from view import Ui_MainWindow
from instruction_widget import Ui_InstructionForm
from question_widget import Ui_QuestionForm

class Slide(QtGui.QWidget):
    """
    Slides are widgets that get to define what happens when space
    is pressed and what instruction text appears (e.g. Press space
    to Go to Next Slide). This class on its own does nothing; all
    the interesting stuff happens in its subclasses.

    FIELDS:

    space_action = The action to perform when space is pressed if
      this slide is current. You have to track when space is pressed
      and call this function; this just says what this slide would
      like to have happen.

    instruction_text - A small instruction on what to do next
      (e.g. Press Space to Continue). Again, you must display this
      text.
    """
    def __init__(self, parent_widget, space_action, instruction_text):
        """
        Creates a new Slide.

        INPUTS:

        parent_widget - The widget that this slide should appear in.
        space_action - What to do when action is pressed. That is
          to respect this slides wishes, you should call space_action()
          when space is pressed.
        instruction_text - The text to appear informing the user what
          to do (to operate the program).
        """
        QtGui.QWidget.__init__(self, parent_widget)
        self.space_action = space_action
        self.instruction_text = instruction_text

    def format_text(self, text):
        """
        Places text in html that makes it big and look nice.
        """
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

class InstructionSlide(Slide):
    """
    A slide containing a block of text.

    INPUTS:

    parent_widget - The widget in which this slide should appear.

    text - The text this slide will display. The slide will do
      general formatting. The string can contain html for custom
      formatting.

    next_slide_fn - Whatever function goes to the next slide. This
      helps define this slide space_action.
    """
    def __init__(self, parent_widget, text, next_slide_fn):
        instruction_text = "Press Space to Continue"
        space_action = next_slide_fn
        Slide.__init__(self, parent_widget, space_action, instruction_text)
        ui = Ui_InstructionForm()
        ui.setupUi(self)
        ui.instructionLabel.setText(self.format_text(text))

class QuestionSlide(Slide):
    """
    This slide displays a question. When space_action is called,it
      then presents an input box and button for the user to answer the
      question. If they get it wrong, instruction_text will be changed
      to say so and they will get to reenter their answer. If they
      get it right, it will say so. Then, space_action will go to next
      slide.
    """
    
    def __init__(self, parent_widget, question, answer, bug_delay, bug_label, instruction_text_fn, next_slide_fn, return_data_fn):
        """
        Creates a QuestionSlide.

        parent_widget - The widget to display this slide in.
        question - The question this slide will ask.
        answer - The answer to the question. This slide will ignore
          case and leading/trailing whitespace.
        bug_delay - Unless space is pressed beforehand, this slide
          will display the answer after this number of seconds. Can
          be a float. If less than 0, the answer will not be displayed
        bug_label - The label on which to display the answer.
        instruction_text_fn - A function which change instruction text.
          Thus, you don't have to actually watch instruction_text to
          see when it changes; this class will update your display for
          using this function.
        next_slide_fn - A function which goes to the next slide.
        return_data_fn - This slide will pass the following argument
          to this function upond completion:
          ['question text', time until space, time from space to first submit,
            time from first submit to second, ..., time from nth submit to
            correct submit]
          This passing in this function allows you to collect data.
        """
        self.answer = answer
        self.bug_label = bug_label
        self.return_data = return_data_fn
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
        self.bug_label.hide()
        self.bug_label.setText(answer)
        self.data = [question]
        self.last_time = time()
        if(bug_delay>=0):
            QtCore.QTimer.singleShot(bug_delay, self.show_bug)
        
    def open_answer_input(self):
        """
        Removes the instruction text and open a line edit and button so
          the user can submit an answer. Also, stops the bug label from
          showing. This, is the first space_action. The next space_action
          does nothing since the user has to submit the right answer first.
        """
        cur_time = time()
        elapsed_time = cur_time-self.last_time
        self.data.append(elapsed_time)
        self.last_time = time()
        self.ui.ansLineEdit.show()
        self.ui.submitAnswerButton.show()
        self.ui.ansLineEdit.setFocus()
        self.instruction_text = ' '
        self.bug_label.hide()
        self.bug_label.setText(' ')
        self.connect(self.ui.submitAnswerButton, QtCore.SIGNAL('clicked()'), self.submit_answer)
        self.space_action = lambda : None
        self.set_inst_text(self.instruction_text)
        
    def submit_answer(self):
        """
        Called when the user presses submit. Checks their answer and
          acts accordingly. If correct, space_action becomes next_slide
          and the display is changed to reflect their correctness.
          If wrong, simply changes the instruction text to say so.
          Also, if correct, this function calls return_data() with
          question and timing information.
        """
        cur_time = time()
        elapsed_time = cur_time-self.last_time
        self.data.append(elapsed_time)
        self.last_time = time()
        ans = str(self.ui.ansLineEdit.text()).strip()
        if ans.upper()==self.answer:
            self.set_inst_text("Correct! Press Space to Continue")
            self.ui.questionLabel.destroy()
            self.ui.ansLineEdit.destroy()
            self.ui.submitAnswerButton.destroy()
            self.space_action = self.next_slide
            self.return_data(self.data)
        else:
            self.set_inst_text("'"+ans+"' is Incorrect; Please Try Again")

    def show_bug(self):
        """
        Displays the answer to the problem. If space has already been
          pressed, then the bug_label has been made blank, and so will
          display nothing.
        """
        self.bug_label.show()
        
class Main(QtGui.QMainWindow):
    """
    The main class of the program. This coordinates activity between the
      various uis, the slides, user interaction, data collection, and
      experiment info processing.
    """
    
    def __init__(self, parent=None):
        """
        Sets up the ui (starts with no slide and a generic instruction_text).
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.bugLabel.hide()
        self.current_slide = None
        self.data = []

    def next_slide(self):
        """
        Looks at the flow stack to see what slide to display next. See
          load_experiment() for info on how this class represents the experiment.

        When the experiment completes, the collected data will appear in a file
          in the experiment directory with date and time of the completion of
          the experiment as its name.
        """
        # flow is a stack of instructions.
        if len(self.flow)==0:
            self.export_data(os.path.join(self.experiment_dir, str(datetime.now())+".txt"))
            self.error_box('The experiment is over!')
            self.close()
            return
        cmd = self.flow.pop()
        if cmd[0]=="instruction":
            self.set_to_instructions(self.instructions[cmd[1]])
        elif cmd[0]=="questions":
            q = self.question_list.pop()
            self.set_to_question(q, self.questions[q],cmd[2])
            if cmd[1]>1:
                self.flow.append(("questions", cmd[1]-1, cmd[2]))

    def load_experiment(self, dirname):
        """
        Experiment data should be contained a directory. The directory must contain
          three files: instructions.txt, questions.txt, and flow.txt. Each non-blank
          line of instructions.txt is turned into a instruction slide. These slides
          are numbered sequentially, starting with 0. questions.txt should contain
          a question on one line, the answer on the next, and so forth. A question
          will only be asked once (even if it appears twice in the file). The order
          of the questions is random. flow.txt contains information about what order
          to display the slides in. There are two possibilities for what may appear
          on a line:
          instruction <the number of the instruction>
          questions <the number of questions to ask> <the number of seconds before
            the bug occurs>
          The number of seconds before the bug occurs can have decimals (0.5 is
          half a second). If the number of seconds is less than 0 or absent, the
          bug will not occur.
          For example:
          instruction 0
          instruction 1
          questions 10 15
          instruction 2
          questions 5
          instruction 3
          Will display the first instruction slide followed by the second. It will
          then ask 10 random questions, displaying the answer to each after 15
          seconds. Then, the third instruction slide will be display. Then, 5
          more questions will be asked for which the answer will not be not
          displayed. Then, the fourth instruction slide will show. Finally, the
          program will exit.
          
          Internally, the instructions from flow.txt are represented as a stack.
        """
        sys.stderr.write("Loading experiment "+dirname+"\n")
        if not os.path.isdir(dirname):
            self.error_box("The experiment folder must be a directory.")
            self.close()
        ins_filename = os.path.join(dirname, "instructions.txt")
        que_filename = os.path.join(dirname, "questions.txt")
        flow_filename = os.path.join(dirname, "flow.txt")
        if not os.path.isfile(ins_filename):
            self.error_box("The experiment folder ("+dirname+") is missing instructions.txt.")
            self.close()
        if not os.path.isfile(que_filename):
            self.error_box("The experiment folder ("+dirname+") is missing questions.txt.")
            self.close()
        if not os.path.isfile(flow_filename):
            self.error_box("The experiment folder ("+dirname+") is missing flow.txt.")
            self.close()
        self.instructions = open(ins_filename,'U').readlines()
        self.questions = dict()
        que = open(que_filename,'U').readlines()
        que = filter( len, map(lambda s : s.strip(), que))
        for i in range(0, len(que)-1, 2):
            self.questions[que[i]] = que[i+1].upper()
        self.question_list = self.questions.keys()
        shuffle(self.question_list)
        flow_raw = open(flow_filename,'U').readlines()
        flow_raw = filter( len, map( lambda s : s.strip(), flow_raw))
        self.flow = list()
        for l in flow_raw:
            cmd = l.split(" ")
            try:
                if len(cmd)==0:
                    continue
                if cmd[0] == "instruction":
                    self.flow.append(("instruction", int(cmd[1])))
                elif cmd[0] == "questions":
                    bug_delay = int(cmd[2])*1000 if len(cmd)>=3 else -1
                    self.flow.append(("questions", int(cmd[1]), bug_delay))
            except:
                self.error_box("There was a problem in flow.txt with the line: "+l)
                self.close()
        # We treat flow as a stack of instructions with the
        # next one at the end. This is just so that we can
        # use pop and append in a natural manner.
        self.flow.reverse()
        self.experiment_dir = dirname

    def clear_slide(self):
        """
        Removes the current slide from display.
        """
        if self.current_slide:
            self.ui.displayLayout.removeWidget(self.current_slide)
            self.current_slide.close()

    def set_slide(self, slide):
        """
        Sets the current slide to the one given. Removes the last slide first.
        """
        self.clear_slide()
        self.current_slide = slide
        self.ui.displayLayout.addWidget(slide)
        self.set_instruction_label(slide.instruction_text)

    def set_instruction_label(self, text):
        """
        Sets the short instruction label on the bottom to the given text.
        """
        self.ui.instructionLabel.setText(self.format_text(text))
            
    def set_to_instructions(self, text):
        """
        Creates an instruction label with the given text and sets it to current.
        """
        self.set_slide(InstructionSlide(self.ui.displayWidget, text, self.next_slide))

    def set_to_question(self, question, answer, bug_delay):
        """
        Creates a question slide from with the given question, answer, and delay
          before showing the answer.
        """
        self.set_slide(QuestionSlide(self.ui.displayWidget, question, answer, bug_delay,
                                     self.ui.bugLabel, self.set_instruction_label, self.next_slide,
                                     self.store_data))

    def store_data(self, new_data):
        """
        Adds new_data to the data to be outputed at the end.
        """
        self.data+=new_data

    def export_data(self, filename):
        """
        Stores the data collected during the experiment in filename.
        """
        out_file = open(filename, 'w')
        for val in self.data:
            if type(val)==str:
                out_file.write('\n'+val)
            else:
                out_file.write('\t'+str(val))
        out_file.close()
    
    def error_box(self, text):
        """
        Shows a message box with the given text. Seems a little finicky...
        """
        sys.stderr.write(text+'\n')
        msg = QtGui.QMessageBox(self)
        msg.setText(text)
        msg.setWindowTitle('Something Bad Happened')
        msg.open()

    def format_text(self, text):
        """
        Places text in html that makes it big and look nice.
        """
        head = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;"><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; color:#404040;">'
        foot = '</span></p></body></html>'
        return head+text+foot

    def keyPressEvent(self, event):
        """
        Qt thing. Called when a key is a pressed. This handles space bar
        stuff, and closing when escape is pressed.
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key_Space and self.current_slide:
            self.current_slide.space_action()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Main()
    if len(sys.argv) == 1:
        myapp.set_to_instructions("You must provide an experiment folder.")
    else:
        myapp.load_experiment(sys.argv[1])
        myapp.next_slide()
    myapp.showFullScreen()
    sys.exit(app.exec_())
