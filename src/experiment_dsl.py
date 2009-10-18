from PyQt4 import QtCore, QtGui
from random import shuffle
from Queue import Queue
from time import time
import os
import threading

class ScheduableAction:
    def __init__(self, fn, timer_storage=None, *args, **kwgs):
        """
        Creates a new ScheduableAction that can execute the given function.

        INPUTS:

        fn - The function the ScheduableAction can execute. It may take an
        number of parameters.

        timer_storage - Every time after() is called, the resulting QTimer
        will be stored in this list. The primary purpose is for times when
        the QTimer may be eaten by gc before it goes off. For these
        instances, you should guarantee that timer_storage should probably
        exist independently of this class so it doesn't get eaten.
        """
        self.args = args
        self.kwgs = kwgs
        self.timer_storage = timer_storage
        self.fn = fn

    def __call__(self, *args, **kwgs):
        """
        Prepares the function to be called with certain arguments.

        INPUTS:

        *args - The normal, required arguments of the function.

        **kwgs - The optional, keyword arguments.
        """
        if(args):
            self.args = args
        if(kwgs):
            self.kwgs = kwgs
        return self

    def __todo(self):
        """
        Returns this ScheduableAction's function with arguments applied in
        a callable form. Thus, self.__todo()() is equivalent to
        self.fn(*self.args, **self.kwgs)
        """
        self.fn(*self.args, **self.kwgs)

    def after(self, ms):
        """
        Waits the given number of ms and then executes the function with
        the arguments applied.

        INPUTS:

        ms - The number of milliseconds to wait before executing the action.

        OUTPUTS:

        The QTimer object who's timeout() signals the function to be called.
        Thus, if you call t = sa().after(5000) and then t.stop() within 5
        seconds, the function will not be called.
        """
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.connect(timer, QtCore.SIGNAL('timeout()'), self.__todo)
        timer.start(ms)
        if self.timer_storage:
            self.timer_storage.append(timer)
        return timer

    def now(self):
        """
        Calls the function with the given arguments immediately. No scheduling occurs.
        """
        self.__todo()

class ExperimentProcessor(QtCore.QObject):
    def __init__(self, gui_control, data_recorder, dirname):
        QtCore.QObject.__init__(self)
        self.c = gui_control
        #self.qa_map = qa_map
        #self.questions = self.qa_map.keys()
        self.data_recorder = data_recorder
        #shuffle(self.questions)
        self.current_question = None
        self.waiting_for_space = False
        self.waiting_for_input = False
        self.connect(self.c, QtCore.SIGNAL('space_pressed'), self.space_pressed)
        self.connect(self.c.ui.submitButton, QtCore.SIGNAL('clicked()'), self.submit_clicked)
        self.timer_storage = []
        self.experiment_script = os.path.join(dirname,'experiment.py')
        l = {}
        execfile(self.experiment_script, self.default_experiment_globals(), l)
        self.experiment_iter = l['main']()
    
    def run_experiment(self):
        try:
            self.experiment_iter.next()
        except StopIteration:
            self.c.close()
        
    def default_experiment_globals(self):
        return {'show' : self.sched_action(self.c.set_main_text),
                'clear' : self.sched_action(lambda : self.c.set_main_text('')),
                'show_message' : self.sched_action(self.c.set_instruction_text),
                'clear_mesage' : self.sched_action(lambda : self.c.set_instruction_text('')),
                'show_bug' : self.sched_action(self.c.set_bug_text),
                'clear_bug' : self.sched_action(lambda : self.c.set_bug_text('')),
                'pick_question' : self.pick_question,
                'question' : (lambda : self.current_question),
                'answer' : (lambda : self.qa_map[self.current_question]),
                'record' : self.data_recorder.record,
                'for_space' : self.wait_for_space,
                'for_user_input' : self.wait_for_user_input,
                'user_input' : (lambda : self.user_input),
                'start_timer' : self.start_timer,
                'time' : self.get_time}

    def sched_action(self, fn):
        a = ScheduableAction(fn, timer_storage=self.timer_storage)
        return a

    def wait_for_space(self):
        self.waiting_for_space = True

    def wait_for_user_input(self):
        self.c.ui.submitButton.show()
        self.c.ui.userInputLineEdit.show()
        self.c.ui.userInputLineEdit.setFocus()
        self.waiting_for_input = True

    def space_pressed(self):
        if self.waiting_for_space:
            self.waiting_for_space = False
            self.run_experiment()

    def submit_clicked(self):
        if self.waiting_for_input:
            self.waiting_for_input = False
            self.user_input = self.c.ui.userInputLineEdit.text()
            self.c.ui.submitButton.hide()
            self.c.ui.userInputLineEdit.hide()
            self.c.setFocus()
            self.run_experiment()
            
    def pick_question(self):
        self.current_question = questions.pop()
        return self.current_question

    def start_timer(self):
        self.last_time = time()

    def get_time(self):
        return time()-self.last_time

    
        

