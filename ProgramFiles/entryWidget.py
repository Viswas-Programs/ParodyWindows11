import tkinter
class Entry(tkinter.Entry):
    def __init__(self, *args, **kwargs):
        tkinter.Entry.__init__(self, *args, **kwargs)
        self.bind("<Button-1>", lambda e=None: self.focus_force())
        self.focus_force()

class Text(tkinter.Text):
    def __init__(self, *args, **kwargs):
        tkinter.Text.__init__(self, *args, **kwargs)
        self.bind("<Button-1>",  lambda e=None: self.focus_force())
        self.focus_force()
