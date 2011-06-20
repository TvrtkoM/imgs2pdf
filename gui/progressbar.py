from Tkinter import *
from ttk import *

class ProgressBarDialog(Toplevel):
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.grab_set()
        
    def start(self):
        body = Frame(self)
        pbar = Progressbar(body, length=300, mode='indeterminate')
        pbar.pack(padx=5, pady=5)
        body.pack(padx=5, pady=5)
        pbar.start()
