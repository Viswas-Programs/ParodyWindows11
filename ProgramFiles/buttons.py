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
        self.BUTTON.identifier = f"desktopIconBtn-{command}"
        self.specialBind()
    def specialBind(self, newSequence=False):
        print(self.doubleClickMode, newSequence, not newSequence)
        if self.BUTTONBIND: self.BUTTON.unbind(self.SEQUENCE, self.BUTTONBIND)
        if not newSequence:
            if self.doubleClickMode: self.SEQUENCE = "<Double-1>"
            else: self.SEQUENCE = "<Button-1>"
        else:
            self.SEQUENCE = newSequence
        def handlerFunc(ev): self.command()
        self.BUTTONBIND = self.BUTTON.bind(self.SEQUENCE, handlerFunc)
    def configure(self, **kwargs):
        if "command" in kwargs: 
            self.command=kwargs["command"]
            self.specialBind(False)
        if "clickMode" in kwargs: 
            if kwargs["clickMode"]: self.specialBind("<Double-1>")
            else: self.specialBind("<Button-1>")
    def destroy(self): self.BUTTON.destroy()
    def grid(self, **kwargs): self.BUTTON.grid(**kwargs)
    def bind(self, *args, **kwargs): self.BUTTON.bind(args, kwargs)


SIDEBAR_BUTTON_INSTANCES = []

class SidebarButtons:
    def __init__(self, frame: tkinter.Frame, defaultColour="Black", standardizedWidth=15, selectionColour="blue"):
        self.frame = frame
        self.selectionColour = selectionColour
        self.BUTTON_COUNT = 0
        self.buttons: dict[int, tkinter.Button] = {}
        self.currentSelection = None
        self.defaultColour = defaultColour
        self.SELF_ID = len(SIDEBAR_BUTTON_INSTANCES)
        self.WIDTH = standardizedWidth
        SIDEBAR_BUTTON_INSTANCES.append(self)
    def commandWrapper(self, ID, redirectCommand):
        self.currentSelection = ID
        for button in self.buttons.values(): button.configure(background=self.defaultColour)
        self.buttons[ID].configure(background=self.selectionColour)
        redirectCommand()
        return
    def Button(self, *args, **kwargs):
        ID = self.BUTTON_COUNT
        if "ID" in kwargs.keys(): 
            ID= kwargs["ID"]
            del kwargs["ID"]
        button = tkinter.Button(*args, **kwargs)
        oldCommand = kwargs["command"]
        button.configure(command=lambda Id=ID, CMD=oldCommand: self.commandWrapper(Id, CMD), width=self.WIDTH)
        button.destroyFunc = button.destroy
        button.destroy = lambda Id=ID: self.removeWhenButtonDestroy(Id)
        self.buttons[ID]= button
        self.BUTTON_COUNT += 1
        return button
    def removeWhenButtonDestroy(self, ID):
        button = dict(self.buttons)[ID]
        del self.buttons[ID]
        button.destroyFunc()
        return
    def __del__(self):
        SIDEBAR_BUTTON_INSTANCES.remove(SIDEBAR_BUTTON_INSTANCES[self.SELF_ID])

