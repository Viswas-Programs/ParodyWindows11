import tkinter
import shelve
from ProgramFiles import callHost
import os

with shelve.open(os.path.join(callHost.getHostDir(), "Users", callHost.getCurrentUsername(), "USER_CONFIG")) as reader:
    THEME_BG, THEME_FG = reader["THEME"][2], reader["THEME"][1]

class Combobox:
    def __init__(self, master: tkinter.Widget, values=[], background=THEME_BG, foreground=THEME_FG):
        self.THEME_BG = background
        self.THEME_FG = foreground
        self.master= master
        self.values=  values
    
    def __setitem__(self, key, value):
        if key == "values": self.values = value
    
    