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
        Executes self.fn(*self.args, **self.kwgs) so that the function of
        this ScheduableAction can be passed around with its arguments in
        place.
        """
        a = self.args
        k = self.kwgs
        return (lambda : self.fn(*a,**k))

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
        timer.connect(timer, QtCore.SIGNAL('timeout()'), self.__todo())
        timer.start(ms)
        if self.timer_storage != None:
            self.timer_storage.append(timer)
        return timer

    def now(self):
        """
        Calls the function with the given arguments immediately. No scheduling occurs.
        """
        self.__todo()()

class ExperimentProcessor(QtCore.QObject):
    """
    Processes and runs the experiment script. This class is the
    link between the experiment script and the gui.
    """
    def __init__(self, gui_control, data_recorder, dirname):
        """
        Prepares the experiment to be run. Qt signals are hooked up (expects)
        gui_control to send 'space_pressed' when space is pressed). Executes
        experiment.py in order to setup user defined functions (especially the
        main function); however, if the user has defined things to be run at
        the top level of the script, that will be executed immediately). Finally,
        reads in the questions file.
        """
        QtCore.QObject.__init__(self)
        self.c = gui_control
        if not self.verify_dir(dirname):
            self.c.close()
        self.__qt_connections()
        #self.qa_map = qa_map
        #self.questions = self.qa_map.keys()
        self.data_recorder = data_recorder
        #shuffle(self.questions)
        self.current_question = None
        self.waiting_for_space = False
        self.waiting_for_input = False
        self.timer_storage = []
        question_fn = os.path.join(dirname,'questions.txt')
        self.extract_questions(question_fn)
        self.experiment_script = os.path.join(dirname,'experiment.py')
        l = {}
        execfile(self.experiment_script, self.default_experiment_globals(), l)
        self.experiment_iter = l['main']()

    def __qt_connections(self):
        """
        Sets up the needed qt connections so that this class can listen for
        space being pressed and submit button being clicked.
        """
        self.connect(self.c, QtCore.SIGNAL('space_pressed'), self.space_pressed)
        self.connect(self.c.ui.submitButton, QtCore.SIGNAL('clicked()'), self.submit_clicked)

    def verify_dir(self, dirname):
        """
        Ensures that the given directory name actually exists and that it
        contains the necessary files to run the experiment.
        """
        if not os.path.isdir(dirname):
            self.c.error_box('The directory '+dirname+' does not exist.')
            return False
        elif not os.path.isfile(os.path.join(dirname, 'experiment.py')):
            self.c.error_box('There is no experiment.py in that directory.')
            return False
        elif not os.path.isfile(os.path.join(dirname, 'questions.txt')):
            self.c.error_box('There is no questions.txt in that directory.')
            return False
        return True

    def extract_questions(self, filename):
        """
        Reads the given file, parsing it for questions. Questions and answers
        must be separated by a blank line. Questions can take up any number of
        lines as long as they contain no blank lines. Answers can only take up
        one line.
        """
        self.questions = []
        self.qtoa = {}
        infile = open(filename, 'r') 
        l = infile.readline()
        while l!='':
            self.questions.append('')
            while l.strip()!='':
                self.questions[-1]+=l+'<br/>' 
                l = infile.readline()
            self.questions[-1].strip()
            l = infile.readline()
            self.qtoa[self.questions[-1]] = l.strip()
            infile.readline()
            l = infile.readline()
        shuffle(self.questions)
        return self.questions

    def run_experiment(self):
        """
        Runs the experiment script until its next yield statement (or until its
        termination). If the script terminates, this function closes the main
        window.
        """
        try:
            self.experiment_iter.next()
        except StopIteration:
            self.c.close()
        
    def default_experiment_globals(self):
        """
        Returns a dictionary experiment script functions names to actual
        functions. This essentially defines the experiment DSL.
        """
        return {'show' : self.sched_action(self.c.set_main_text),
                'clear' : self.sched_action(lambda : self.c.set_main_text('')),
                'show_message' : self.sched_action(self.c.set_instruction_text),
                'clear_message' : self.sched_action(lambda : self.c.set_instruction_text('')),
                'show_bug' : self.sched_action(self.c.set_bug_text),
                'clear_bug' : self.sched_action(lambda : self.c.set_bug_text('')),
                'pick_question' : self.pick_question,
                'question' : (lambda : self.current_question),
                'answer' : (lambda : self.qtoa[self.current_question]),
                'record' : self.data_recorder.record,
                'for_space' : self.wait_for_space,
                'for_user_input' : self.wait_for_user_input,
                'user_input' : (lambda : self.user_input),
                'start_timer' : self.start_timer,
                'is_correct' : self.is_correct,
                'time' : self.get_time}

    def sched_action(self, fn):
        """
        Creates a ScheduableAction to execute the given function. The
        ScheduableAction is created so that any timer it makes will be
        stored by this class. Thus, the timers will not die before this 
        class does. This prevents the timers from dieing prematurely.
        """
        a = ScheduableAction(fn, timer_storage=self.timer_storage)
        return a

    def is_correct(self, guess):
        return guess.strip().upper() == self.qtoa[self.current_question].strip().upper()

    def wait_for_space(self):
        """
        Lets this object know its waiting for a space.
        """
        self.waiting_for_space = True

    def wait_for_user_input(self):
        """
        Enables the showing of submitButton and userInputLineEdit in
        self.c.ui, preparing the line edit to accept new input. Also,
        let's this object know its waiting for the submit button to be
        pressed.
        """
        self.c.ui.submitButton.show()
        self.c.ui.userInputLineEdit.show()
        self.c.ui.userInputLineEdit.setText('')
        self.c.ui.userInputLineEdit.setFocus()
        self.waiting_for_input = True

    def space_pressed(self):
        """
        Should be called when space is pressed (a qt connection should
        have been setup when this object was initialized). If this object
        was waiting for space to be pressed, this function will tell it
        that it no longer has to wait and to keep running the experiment.
        """
        if self.waiting_for_space:
            self.waiting_for_space = False
            self.run_experiment()

    def submit_clicked(self):
        """
        Should be called when self.c.ui.submitButton is clicked (a qt
        connection should have been setup when this object was
        initialized). Stores the text from self.c.ui.userInputLineEdit.
        Hides both the submit button and the line edit. Gives focus
        back to the main window.
        """
        if self.waiting_for_input:
            self.waiting_for_input = False
            self.user_input = str(self.c.ui.userInputLineEdit.text()).strip()
            self.c.ui.submitButton.hide()
            self.c.ui.userInputLineEdit.hide()
            self.c.setFocus()
            self.run_experiment()
            
    def pick_question(self):
        """
        Sets the current_question to the next question on the list of
        questions. The question is removed from the list so that it will
        not be asked again.
        """
        self.current_question = self.questions.pop()
        return self.current_question

    def start_timer(self):
        """
        Records the current time. Calls to get_time() will give the time
        since start_timer() was last called.
        """
        self.last_time = time()

    def get_time(self):
        """
        Returns the amount of time since start_timer() was last called.
        """
        return time()-self.last_time

    
        

