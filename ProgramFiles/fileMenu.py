import tkinter

class Menu():
    def __init__(self, DWMFrame):
        self.DWM = DWMFrame
        self.BACKGROUND = DWMFrame.BACKGROUND
        self.FOREGROUND = DWMFrame.FOREGROUND
        self.OPTIONS_TO_BUTTONS = {} # Format: "OPTION": {"text": "X", "command": func}
        self.fileMenuFrame = tkinter.Frame(self.DWM, background=self.DWM.BACKGROUND, border=5, borderwidth=5)
        self.fileMenuFrame.grid(row=1, column=0, sticky="NSEW",columnspan=10)
        self.currentKeyInUsage = None
        self.NUM_KEY = 0
        self.CURRENT_SHOWN_MENU = None
        self.CLICK_EVENT_BIND_VAL = None
        self.ALT_L_EVENT_BIND_VAL = None
        self.ALT_R_EVENT_BIND_VAL = None
    def addMenuOption(self, keyName: str):
        self.currentKeyInUsage = keyName
        btn = tkinter.Button(self.fileMenuFrame, background=self.BACKGROUND, foreground=self.FOREGROUND, text=keyName, command=lambda: self.clickEvent(keyName))
        btn.IDENTIFIER = keyName
        btn.grid(row=0, column=self.NUM_KEY)
        subBtnsFrame = tkinter.Frame(self.DWM, background=self.BACKGROUND, width=15, border=5)
        self.OPTIONS_TO_BUTTONS[keyName] = {"mainButton": btn, "subButtons": {}, "mainFrame": subBtnsFrame, "numKey": self.NUM_KEY}
        self.NUM_KEY += 1
    def addSubMenuOption(self, text, command, keyname=False):
        if not keyname: keyname = self.currentKeyInUsage
        pos = len(self.OPTIONS_TO_BUTTONS[keyname]["subButtons"])
        master = self.OPTIONS_TO_BUTTONS[keyname]["mainFrame"]
        btn = tkinter.Button(master, background=self.BACKGROUND, foreground=self.FOREGROUND, text=text, command=command, width=15)
        btn.TEXT = text
        btn.COMMAND = command
        btn.POS = pos
        self.OPTIONS_TO_BUTTONS[keyname]["subButtons"][text] = btn
    def clickEvent(self, keyName, e=None):
        self.CURRENT_SHOWN_MENU = keyName
        self.OPTIONS_TO_BUTTONS[keyName]["mainFrame"].grid(column=self.OPTIONS_TO_BUTTONS[keyName]["numKey"], row=2)
        self.OPTIONS_TO_BUTTONS[keyName]["mainFrame"].lift()
        self.CLICK_EVENT_BIND_VAL = self.DWM.ROOT.bind("<Button-1>", self.hideShownMenu)
        self.ALT_L_EVENT_BIND_VAL = self.DWM.ROOT.bind("<Alt_L>", self.hideShownMenu)
        self.ALT_R_EVENT_BIND_VAL = self.DWM.ROOT.bind("<Alt_R>", self.hideShownMenu)
        for subButton in self.OPTIONS_TO_BUTTONS[keyName]["subButtons"].values():
            subButton.IDENTIFIER = "MenuSubButton"
            subButton.grid(row=subButton.POS, column=0)
    def __hideShownMenu(self, e=None):
        self.OPTIONS_TO_BUTTONS[self.CURRENT_SHOWN_MENU]["mainFrame"].grid_forget()
        self.DWM.ROOT.unbind("<Button-1>", self.CLICK_EVENT_BIND_VAL)
        self.DWM.ROOT.unbind("<Alt_L>", self.ALT_L_EVENT_BIND_VAL)
        self.DWM.ROOT.unbind("<Alt_R>", self.ALT_R_EVENT_BIND_VAL)
        self.CLICK_EVENT_BIND_VAL = None
        self.ALT_R_EVENT_BIND_VAL = None
        self.ALT_L_EVENT_BIND_VAL = None
    def hideShownMenu(self, e=None):
        try:
            btn = self.DWM.ROOT.winfo_containing(e.x_root, e.y_root)
            if btn.IDENTIFIER == "MenuSubButton":
                self.__hideShownMenu()
                btn.COMMAND()
        except: pass
        finally: self.__hideShownMenu()
            
