import tkinter
class IconButton:
    def __init__(self, master, image=None, foreground="White", background="Black", command=None, doubleClickMode=False, **kwargs):
        self.master=master
        self.image=image
        self.foreground = foreground
        self.background = background
        self.command = command
        self.doubleClickMode=doubleClickMode
        self.BUTTONBIND = None
        self.SEQUENCE = None
        self.BUTTON = tkinter.Label(self.master, background=self.background, foreground=self.foreground, image=self.image, **kwargs)
        self.specialBind(False)
    def specialBind(self, newSequence=False):
        if self.BUTTONBIND: self.BUTTON.unbind(self.SEQUENCE, self.BUTTONBIND)
        if not newSequence:
            if self.doubleClickMode: self.SEQUENCE = "<Double-1>"
            else: self.SEQUENCE = "<Button-1>"
        else:
            self.SEQUENCE = newSequence
        def handlerFunc(ev): self.command()
        self.BUTTON.bind(self.SEQUENCE, handlerFunc)
    def configure(self, **kwargs):
        if "command" in kwargs: 
            self.command=kwargs["command"]
            self.specialBind(False)
        if "clickMode" in kwargs: 
            if kwargs["clickMode"]: self.specialBind("<Double-1>")
            else: self.specialBind("<Button-1>")
    def destroy(self):
        self.BUTTON.destroy()
    def grid(self, **kwargs):
        self.BUTTON.grid(**kwargs)
        