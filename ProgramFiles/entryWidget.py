import tkinter
class Entry(tkinter.Entry):
    def __init__(self, *args, **kwargs):
        tkinter.Entry.__init__(self, *args, **kwargs)
        self.bind("<Button-1>", self.giveFocus)
        self.giveFocus()
        THEME_TEXT_BG = "Black"
        THEME_TEXT_FG = "White"
        try: 
            THEME_TEXT_BG = kwargs["background"]
            THEME_TEXT_FG = kwargs["foreground"]
        except: pass
        self.configure(insertbackground=THEME_TEXT_FG, selectbackground=THEME_TEXT_FG, selectforeground=THEME_TEXT_BG)
        self.giveFocus()
    def giveFocus(self, *args):
        self.focus_force()
        self.update()
        self.update_idletasks()
        self.focus_force()


class Text(tkinter.Text):
    def __init__(self, *args, **kwargs):
        tkinter.Text.__init__(self, *args, **kwargs)
        self.bind("<Button-1>",  self.giveFocus)
        self.giveFocus()
        THEME_TEXT_BG = "Black"
        THEME_TEXT_FG = "White"
        try: 
            THEME_TEXT_BG = kwargs["background"]
            THEME_TEXT_FG = kwargs["foreground"]
        except: pass
        self.configure(insertbackground=THEME_TEXT_FG, selectbackground=THEME_TEXT_FG, selectforeground=THEME_TEXT_BG)
        self.giveFocus()
    def giveFocus(self, *args):
        self.focus_force()
        self.update()
        self.update_idletasks()
        self.focus_force()

class LabelledEntryBox():
    """ Used to create labels alongside the entryboxes
    Important note: It's recommended to not place the entry widget manually by yourself, and call any place change configurations on this class instead
    If you want to change the label text, call the configureLabel method, since normal configure method will be routed to the frame widget
    If you want to change any aspects of the entry widget, use the configureEntry method
    :param master: The master param is to specify parent widget/window (obvious)
    :param label: Label param is for the description label text that goes alongside the entrybox
    :param kwargs: Options for the entry widget
      """
    def __init__(self, master, label: str, **kwargs):
        bg="Black"
        fg="White"
        try: 
            if kwargs.get("background"): bg = kwargs.get("background")
            if kwargs.get("foreground"): fg = kwargs.get("foreground")
        except Exception: pass
        self.FRAME = tkinter.Frame(master, background=bg)
        self.label = tkinter.Label(self.FRAME, background=bg, foreground=fg, text=label)
        self.label.grid(row=0, column=0)
        self.entryBox = Entry(self.FRAME, **kwargs)
        self.entryBox.grid(row=0, column=1)
        self.update()
        self.update_idletasks()
    def grid(self, *args, **kwargs): self.FRAME.grid(*args, **kwargs)
    def pack(self, *args, **kwargs): self.FRAME.pack(*args, **kwargs)
    def place(self, *args, **kwargs): self.FRAME.place(*args, **kwargs)
    def configureEntry(self, *args, **kwargs): self.entryBox.configure(*args, **kwargs)
    def configureLabel(self, *args, **kwargs): self.label.configure(*args, **kwargs)
    def configure(self, *args, **kwargs): self.FRAME.configure(*args, **kwargs)
    def update(self): self.FRAME.update(); self.entryBox.update(); self.label.update()
    def update_idletasks(self): self.FRAME.update_idletasks(); self.entryBox.update_idletasks(); self.label.update_idletasks()

