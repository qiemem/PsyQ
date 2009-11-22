#!/usr/bin/env python
import sys
import os
import Tkinter
import tkMessageBox
import tkFileDialog
import tkFont
from datetime import datetime
from experiment_dsl import ExperimentProcessor
        
class Main(object):
    """
    The main class of the program. This coordinates activity between the
      various uis, the slides, user interaction, data collection, and
      experiment info processing.
    """
    
    def __init__(self, master, experiment_dirname, parent=None):
        """
        Sets up the ui (starts with no slide and a generic instruction_text).  
        """
        self.exit_status = 0
        self.root = master
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.experiment_dirname = experiment_dirname
        self.data = []
        self.p = ExperimentProcessor(self, self, experiment_dirname)

        self.user_input = ""

        self.create_widgets()
        self.setup_event_bindings()
    def run(self):
        self.p.run_experiment()
        self.root.mainloop()
        return self.exit_status

    def create_widgets(self):
        self.font = tkFont.Font(self.root, 'Lucida 26')
        self.user_input_font = tkFont.Font(self.root, 'Lucida 18')

        self.top_padding = Tkinter.Frame(self.root, height = 300)
        self.top_padding.pack(fill='x')

        self.main_display_label = Tkinter.Label(self.root, 
                                                font = self.font, 
                                                fg="gray30",
                                                wraplength=800)
        self.main_display_label.pack(side = "top", fill="both")

        self.user_input_frame = Tkinter.Frame(self.root,
                                              height = 30)
        self.user_input_entry = Tkinter.Entry(self.user_input_frame, 
                                              font = self.user_input_font)
        self.submit_button = Tkinter.Button(self.user_input_frame,
                                            text = "Submit", 
                                            command = self.submit_input)
        self.user_input_frame.pack(side = "top", pady = 10)

        self.instruction_label = Tkinter.Label(self.root,
                                               font = self.font, 
                                               fg="gray40",
                                               wraplength=800)
        self.instruction_label.pack(side = "top", fill = "x")

        self.bug_label = Tkinter.Label(self.root)
        self.bug_label.pack(side = "bottom", pady=30)


    def get_user_input(self):
        #self.user_input_entry.delete(0, 'end')
        self.user_input_entry.pack(side = "left", anchor="e")
        self.user_input_entry.delete(0, 'end')
        self.user_input_entry.bind("<Return>", 
                                   lambda e : self.submit_button.invoke())
        self.submit_button.pack(side = "right", anchor="w")
        self.user_input_entry.focus_set()

    def submit_input(self):
        self.user_input = self.user_input_entry.get()
        self.user_input_entry.pack_forget()
        self.submit_button.pack_forget()
        self.p.submit_clicked()

    def set_main_text(self, text):
        """
        Set the center text to given text.
        """
        self.main_display_label.configure(text=text)

    def set_instruction_text(self, text):
        """
        Sets the lower text to the given text. Usually used to give simple
        instructions, such as 'Press space to continue'.
        """
        self.instruction_label.configure(text = text)

    def set_bug_text(self, text):
        """
        The bug text is a smaller, more unformatted looking label on the
        bottom. If you wish to display text that looks like it shouldn't
        be displayed.
        """
        self.bug_label.configure(text=text)

    def record(self, new_data):
        """
        Adds new_data to the data to be outputed at the end.
        """
        self.data.append(new_data)

    def export_data(self, filename):
        """
        Stores the data collected during the experiment in filename.
        """
        if len(self.data)>0:
            out_file = open(filename, 'w')
            out_file.write(str(self.data[0]))
            for val in self.data[1:]:
                out_file.write('\n'+str(val))
            out_file.close()
    
    def error_box(self, text):
        """
        Shows a message box with the given text. Seems a little finicky...
        """
        sys.stderr.write(text+'\n')
        self.exit_status = 1
        tkMessageBox.showerror("Error", text)

    def setup_event_bindings(self):
        self.root.bind("<space>", self.on_space)
        self.root.bind("<Escape>", self.close)

    def on_space(self, event):
        self.p.space_pressed()

    def close(self, event):
        filename = os.path.join(self.experiment_dirname,str(datetime.now())+'.txt')
        self.export_data(filename)
        self.root.quit()

if __name__ == "__main__":
    root = Tkinter.Tk()
    experiment_dir = None
    if(len(sys.argv)>=2):
        experiment_dir = sys.argv[1]
    else:
        experiment_dir = tkFileDialog.askdirectory(master=root)
    if experiment_dir == '':
        sys.exit(0)
    myapp = Main(root,experiment_dir)
    sys.exit(myapp.run())
