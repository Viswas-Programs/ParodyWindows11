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
