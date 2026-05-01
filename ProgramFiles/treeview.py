import tkinter
from ProgramFiles import callHost
import shelve
import os
from tkinter.ttk import Scrollbar
import tkinter.ttk as ttk
with shelve.open(os.path.join(callHost.getHostDir(), "Users", callHost.getCurrentUsername(), "USER_CONFIG")) as reader:
    THEME_BG, THEME_FG = reader["THEME"][2], reader["THEME"][1]

OBJECTS = []

class Treeview:
    def __init__(self, master: tkinter.Widget, *args, **kwargs):
        self.THEME_BG = THEME_BG
        self.THEME_FG = THEME_FG
        self.width=30
        self.master = master
        self.BINDS = {}
        self.height=master.winfo_screenwidth()//800
        self.ALL_FRAMEs: dict[str, tkinter.Text]= {}
        self.recentFrameUse = None
        self.CURRENT_SELECTION = None
        if "background" in kwargs.keys(): self.THEME_BG=kwargs["background"]
        if "bg" in kwargs.keys(): self.THEME_BG=kwargs["bg"]
        if "foreground" in kwargs.keys(): self.THEME_FG=kwargs["foreground"]
        if "fg" in kwargs.keys(): self.THEME_FG=kwargs["fg"]
        self.mainFrame = tkinter.Frame(self.master, background=self.THEME_BG)
        self.scrollBar = Scrollbar(self.mainFrame, orient="vertical", command=self.__scrollerHandler, style="TScrollbar")
        self.scrollBar.grid(row=0, column=0, sticky="NS")
        ttk.Style().configure("TScrollbar", background=THEME_BG)
        self._populateColumn("#0")
    def __scrollerHandler(self, *args, **kwargs):
        for i in list(dict(self.ALL_FRAMEs).values()):
            i.yview(*args)
    def __INTERNALS_mouseScroller(self, event, *args, **kwargs): 
        for i in list(dict(self.ALL_FRAMEs).values()):
            i.yview_scroll(int(-1*(event.delta/120)), "units")
    def _populateColumn(self, name,  width=None):
        wd = self.width
        if width != None: wd=width
        self.recentFrameUse = name
        frame = tkinter.Text(self.mainFrame, background=self.THEME_BG, width=wd, height=self.height*10)
        frame.configure(state="disabled")
        frame.WIDTH = wd
        frame.BUTTONS = {}
        frame.grid_propagate(False)
        LBL = tkinter.Label(frame, background=self.THEME_BG, foreground=self.THEME_FG, text=str(name), width=wd, justify="center", anchor="center")
        frame.window_create("0.0", window=LBL)
        frame.NAME = name
        frame.LBL = LBL
        frame.grid(row=0, column=len(self.ALL_FRAMEs.keys()))
        frame.config(yscrollcommand=self.scrollBar.set)
        self.bind("<MouseWheel>", self.__INTERNALS_mouseScroller)
        frame.bind("<MouseWheel>", self.__INTERNALS_mouseScroller)
        self.scrollBar.bind("<MouseWheel>", self.__INTERNALS_mouseScroller)
        self.scrollBar.grid_configure(column=len(self.ALL_FRAMEs.keys())+1)
        
        self.ALL_FRAMEs[name] = frame
    def column(self, name, width=None, **kwargs):
        self.ALL_FRAMEs[name].configure(state="normal")
        self.ALL_FRAMEs[name].configure(width=width//10)
        self.ALL_FRAMEs[name].WIDTH = width//10
        self.ALL_FRAMEs[name].LBL.configure(width=width//10)
        for i in self.get_children(name):
            i.configure(width=width//10)
        self.ALL_FRAMEs[name].configure(state="disabled")
    def __setitem__(self, key, value):
        if key == "column": self._populateColumn(value)
    def heading(self, name, text="<defaultname0>", anchor=tkinter.CENTER):
        self.ALL_FRAMEs[name].LBL.configure(text=text, justify=anchor, anchor=anchor)
    def bind(self, eventName, callback):
        self.BINDS[eventName] = callback
        for frame in dict(self.ALL_FRAMEs).keys():
            for x in self.get_children(frame):
                self._buttonBinder(x)
    def insert(self, parent, index=None, id=None, iid=None, text="<DefaultText>", values=[]):
        button = tkinter.Button(self.ALL_FRAMEs["#0"], background=self.THEME_BG, foreground=self.THEME_FG, text=text, width=self.ALL_FRAMEs["#0"].WIDTH, justify=tkinter.LEFT, anchor="w")
        button.configure(command=lambda bt=button: self._clickAction(bt))
        #button.grid(row=len(self.ALL_FRAMEs["#0"].BUTTONS.keys())+1, column=0)
        #self.ALL_FRAMEs["#0"].window_create(f"{len(self.ALL_FRAMEs["#0"].BUTTONS.keys())+1}.0", window=button)
        self.ALL_FRAMEs["#0"].window_create("end", window=button)
        button.IID = iid
        button.PARENT_COLUMN = "#0"
        button.CHILDREN = []
        self._buttonBinder(button)
        self.ALL_FRAMEs["#0"].configure(state="normal")
        self.ALL_FRAMEs["#0"].BUTTONS[iid] = button
        button.bind("<MouseWheel>", self.__scrollerHandler)
        #self.ALL_FRAMEs["#0"].config(yscrollcommand=self.scrollBar.set)
        for x, i in enumerate(values):
            btn = tkinter.Button(list(dict(self.ALL_FRAMEs).values())[x+1], background=self.THEME_BG, foreground=self.THEME_FG, text=i, width=list(dict(self.ALL_FRAMEs).values())[x+1].WIDTH, justify=tkinter.LEFT, anchor="w")
            btn.configure(command=lambda bt=btn: self._clickAction(bt))
            #btn.grid(row=len(list(dict(self.ALL_FRAMEs).values())[x+1].BUTTONS.keys())+1, column=0)
            #self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].window_create(f"{len(list(dict(self.ALL_FRAMEs).values())[x+1].BUTTONS.keys())+1}.0", window=btn)
            self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].window_create("end", window=btn)
            btn.IID = iid
            btn.PARENT_COLUMN = list(dict(self.ALL_FRAMEs).keys())[x+1]
            btn.PARENT_BUTTON = button
            button.CHILDREN.append(btn)
            self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].configure(state="normal")
            self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].BUTTONS[iid] = btn
            #self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].config(yscrollcommand=self.scrollBar.set)
            self.ALL_FRAMEs[list(dict(self.ALL_FRAMEs).keys())[x+1]].configure(state="disabled")
            btn.bind("<MouseWheel>", self.__scrollerHandler)
            self._buttonBinder(btn)
        self.ALL_FRAMEs["#0"].configure(state="disabled")
        #self.ALL_FRAMEs[list(self.ALL_FRAMEs.keys())[-1]].config(yscrollcommand=self.scrollBar.set)
    def delete(self, button: tkinter.Button):
        #INDEX = list(self.ALL_FRAMEs[button.PARENT_COLUMN].BUTTONS.values()).index(button)
        for i in self.ALL_FRAMEs.keys():
            if i == button.PARENT_COLUMN: continue
            #self.ALL_FRAMEs[i].BUTTONS[list(dict(dict(self.ALL_FRAMEs)[i].BUTTONS).keys())[INDEX]].destroy()
            self.ALL_FRAMEs[i].BUTTONS[button.IID].destroy()
            #del self.ALL_FRAMEs[i].BUTTONS[list(dict(dict(self.ALL_FRAMEs)[i].BUTTONS).keys())[INDEX]]
            del self.ALL_FRAMEs[i].BUTTONS[button.IID]
        button.destroy()
    def _buttonBinder(self, button: tkinter.Button):
        for key in dict(self.BINDS).keys():
            button.bind(key, self.BINDS[key])
    def get_children(self, item="#0"):
        return [button for button in self.ALL_FRAMEs[item].winfo_children() if isinstance(button, tkinter.Button)]
    def _clickAction(self, button):
        #TEMP = str(self.CURRENT_SELECTION.IID)
        try:
            if self.CURRENT_SELECTION:
                try:
                    for child in self.CURRENT_SELECTION.CHILDREN:
                        child.configure(background=self.THEME_BG, foreground=self.THEME_FG)
                except Exception:
                    for child in self.CURRENT_SELECTION.PARENT_BUTTON.CHILDREN:
                        child.configure(background=self.THEME_BG, foreground=self.THEME_FG)
                self.CURRENT_SELECTION.configure(background=self.THEME_BG, foreground=self.THEME_FG)
                self.CURRENT_SELECTION = None
            #if str(button.IID) == TEMP: return
        except: pass
        try:
            for child in button.CHILDREN:
                child.configure(background="#0000ff", foreground="#ffffff")
            
            self.CURRENT_SELECTION = button
        except Exception:
            for child in button.PARENT_BUTTON.CHILDREN:
                child.configure(background="#0000ff", foreground="#ffffff")
            button.PARENT_BUTTON.configure(background="#0000ff", foreground="#ffffff")
            self.CURRENT_SELECTION = button.PARENT_BUTTON
        button.configure(background="#0000ff", foreground="#ffffff")
        self.mainFrame.event_generate("<<TreeviewSelect>>")
    def focus(self, item=None):
        if item:
            if self.CURRENT_SELECTION: self._clickAction(self.CURRENT_SELECTION)
            self._clickAction(item)
        return self.CURRENT_SELECTION
    def focusByIID(self, iid):
        self.focus(self.ALL_FRAMEs["#0"].BUTTONS[iid])
    def item(self, item, options=None,):
        if options == None: return item.cget("text")
        else:
            values = [item.cget("text") for item in item.CHILDREN]
            return values
    def configure(self, *args, **kwargs): pass
    def grid(self, *args, **kwargs): self.mainFrame.grid(*args, **kwargs)
    def pack(self, *args, **kwargs): self.mainFrame.pack(*args, **kwargs)
    def place(self, *args, **kwargs): self.mainFrame.place(*args, **kwargs)