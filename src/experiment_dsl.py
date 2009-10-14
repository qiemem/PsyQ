from PyQt4 import QtCore, QtGui
from random import shuffle
import os
import threading

class ScheduableAction:
    def __init__(self, fn, *args, **kwgs):
        """
        Creates a new ScheduableAction that can execute the given function.

        INPUTS:

        fn - The function the ScheduableAction can execute. It may take an
        number of parameters.
        """
        self.args = args
        self.kwgs = kwgs
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
        return lambda : self.fn(*self.args, **self.kwgs)

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
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), self.__todo())
        timer.start(ms)
        return timer

    def now(self):
        """
        Calls the function with the given arguments immediately. No scheduling occurs.
        """
        self.__todo()()

class ExperimentProcessor(QtCore.QObject):
    def __init__(self, gui_control, data_recorder, dirname):
        QtCore.QObject.__init__(self)
        self.c = gui_control
        #self.qa_map = qa_map
        #self.questions = self.qa_map.keys()
        self.data_recorder = data_recorder
        #shuffle(self.questions)
        self.current_question = None
        self.experiment_globals = self.default_experiment_globals()
        self.paused = False
        self.space_event = threading.Event()
        self.input_event = threading.Event()
        self.user_input = ''
        self.experiment_script = os.path.join(dirname,'experiment.py')
        self.experiment_thread = threading.Thread(target = self.__exec_script)
        self.connect(gui_control, QtCore.SIGNAL('space_pressed'), self.space_event.set)
        self.connect(gui_control.ui.submitButton, QtCore.SIGNAL('clicked()'), self.on_submit)
        print(self.space_event)

    
    def run_experiment(self):
        print("Running exp")
        self.experiment_thread.start()
        print("exp is running")

    def __exec_script(self):
        print('called')
        print(self.space_event)
        execfile(self.experiment_script, self.default_experiment_globals())
        
    def default_experiment_globals(self):
        return {'show' : ScheduableAction(self.c.set_main_text),
                'clear' : ScheduableAction(lambda : self.c.set_main_text('')),
                'show_message' : ScheduableAction(self.c.set_instruction_text),
                'clear_mesage' : ScheduableAction(lambda : self.c.set_instruction_text('')),
                'show_bug' : ScheduableAction(self.c.set_bug_text),
                'clear_bug' : ScheduableAction(lambda : self.c.set_bug_text('')),
                'pick_question' : self.pick_question,
                'question' : (lambda : self.current_question),
                'answer' : (lambda : self.qa_map[self.current_question]),
                'record' : self.data_recorder.record,
                'wait_for_space' : self.wait_for_space,
                'get_user_input' : self.get_user_input}

    def wait_for_space(self):
        print('waiting for space')
        self.space_event.clear()
        self.space_event.wait()
        print('space received')

    def get_user_input(self):
        print('changing stuff')
        self.c.ui.submitButton.show()
        self.c.ui.userInputLineEdit.show()
        print('waiting for user input')
        self.input_event.clear()
        self.input_event.wait()
        print('input received')
        return self.user_input

    def on_submit(self):
        print('submit')
        self.user_input = self.c.ui.userInputLineEdit.text()
        self.c.ui.submitButton.hide()
        self.c.ui.userInputLineEdit.hide()
        self.input_event.set()
    
    def pick_question(self):
        self.current_question = questions.pop()
        return self.current_question

    
        

