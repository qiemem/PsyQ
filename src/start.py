#!/usr/bin/env python

import sys
import os
from random import shuffle
from time import time
from datetime import datetime
from PyQt4 import QtCore, QtGui
from view import Ui_MainWindow
from experiment_dsl import ExperimentProcessor
        
class Main(QtGui.QMainWindow):
    """
    The main class of the program. This coordinates activity between the
      various uis, the slides, user interaction, data collection, and
      experiment info processing.
    """
    
    def __init__(self, experiment_dirname, parent=None):
        """
        Sets up the ui (starts with no slide and a generic instruction_text).
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.bugLabel.setText('')
        self.data = []
        self.ui.userInputLineEdit.hide()
        self.ui.submitButton.hide()
        self.experiment_dirname = experiment_dirname
        self.p = ExperimentProcessor(self, self, experiment_dirname)

    def set_main_text(self, text):
        """
        Set the center text to given text.
        """
        self.ui.mainDisplayLabel.setText(self.format_text(text))

    def set_instruction_text(self, text):
        """
        Sets the lower text to the given text. Usually used to give simple
        instructions, such as 'Press space to continue'.
        """
        self.ui.instructionLabel.setText(self.format_text(text))

    def set_bug_text(self, text):
        """
        The bug text is a smaller, more unformatted looking label on the
        bottom. If you wish to display text that looks like it shouldn't
        be displayed.
        """
        self.ui.bugLabel.setText(text)

    def record(self, new_data):
        """
        Adds new_data to the data to be outputed at the end.
        """
        self.data.append(new_data)

    def export_data(self, filename):
        """
        Stores the data collected during the experiment in filename.
        """
        out_file = open(filename, 'w')
        for val in self.data:
            out_file.write('\n'+str(val))
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
        if event.key() == QtCore.Qt.Key_Space:
            self.emit(QtCore.SIGNAL('space_pressed'))

    def showEvent(self, event):
        """
        A qt event called when the main window is displayed. Runs the
        the experiment.
        """
        self.p.run_experiment()
        #pass
    def closeEvent(self, event):
        """
        A qt event called when the main window is closed. Saves all
        collected data.
        """
        filename = os.path.join(self.experiment_dirname,str(datetime.now()))
        self.export_data(filename)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Main(sys.argv[1])
    myapp.showFullScreen()
    sys.exit(app.exec_())
